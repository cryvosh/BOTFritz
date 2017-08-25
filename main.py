import tensorflow as tf
import multiprocessing
import numpy as np
import screenshot
import pyautogui
import win32api
import logic
import time
import cv2

from utils import label_map_util
from utils import visualization_utils as vis_util

PATH_TO_CKPT = 'frozen_inference_graph.pb'
PATH_TO_LABELS = 'label_map.pbtxt'
NUM_CLASSES = 4

visionRadius = 500
scale = 3.5

def main():
    last_time = time.time()

    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                                use_display_name=True)
    category_index = label_map_util.create_category_index(categories)

    region = {'top': pyautogui.size()[1] // 2 - visionRadius // 2,
               'left': pyautogui.size()[0] // 2 - visionRadius // 2,
               'width': visionRadius, 'height': visionRadius}

    boxRay = multiprocessing.Array('d', 20, lock=False)
    scoreRay = multiprocessing.Array('d', 5, lock=False)
    classRay = multiprocessing.Array('d', 5, lock=False)

    logicProcess = multiprocessing.Process(target=logic.play, args=(boxRay, scoreRay, classRay,
                                                                    scale, visionRadius))
    logicProcess.start()

    with detection_graph.as_default():
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        with tf.Session(graph=detection_graph, config=config) as sess:
            while True:
                print('FPS: {}'.format(1 / (time.time() - last_time)))
                last_time = time.time()

                image_np = np.array(screenshot.grab(region))
                image_np = cv2.cvtColor(image_np, cv2.COLOR_RGBA2RGB)
                image_np_expanded = np.expand_dims(image_np, axis=0)
                image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
                boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
                scores = detection_graph.get_tensor_by_name('detection_scores:0')
                classes = detection_graph.get_tensor_by_name('detection_classes:0')
                num_detections = detection_graph.get_tensor_by_name('num_detections:0')

                (boxes, scores, classes, num_detections) = sess.run(
                    [boxes, scores, classes, num_detections],
                    feed_dict={image_tensor: image_np_expanded})

                vis_util.visualize_boxes_and_labels_on_image_array(
                    image_np,
                    np.squeeze(boxes),
                    np.squeeze(classes).astype(np.int32),
                    np.squeeze(scores),
                    category_index,
                    use_normalized_coordinates=True,
                    line_thickness=8)

                boxRay[:] = np.asarray(boxes[0][:5]).flatten()
                scoreRay[:] = np.asarray(scores[0][:5]).flatten()
                classRay[:] = np.asarray(classes[0][:5]).flatten()

                cv2.imshow('BOT Fritz', image_np)

                # BACKSPACE key pressed
                if cv2.waitKey(1) & win32api.GetAsyncKeyState(0x08):
                    logicProcess.terminate()
                    cv2.destroyAllWindows()
                    break

if __name__ == '__main__':
    main()