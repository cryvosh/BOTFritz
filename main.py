import tensorflow as tf
import numpy as np
import pyautogui
import time
import cv2

from mss import mss
from utils import label_map_util
from utils import visualization_utils as vis_util

PATH_TO_CKPT = 'frozen_inference_graph.pb'
PATH_TO_LABELS = 'label_map.pbtxt'
NUM_CLASSES = 4
radius = 500
scale = 2.5

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

    monitor = {'top': pyautogui.size()[1] // 2 - radius // 2,
               'left': pyautogui.size()[0] // 2 - radius // 2,
               'width': radius, 'height': radius}
    sct = mss()

    with detection_graph.as_default():
        with tf.Session(graph=detection_graph) as sess:
            while True:
                print('dt = {} seconds'.format(time.time() - last_time))
                last_time = time.time()

                image_np = np.array(sct.grab(monitor))
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

                i = dx = dy = 0

                if scores[0][0] >= 0.5:
                    dx = (((boxes[0][0][1] + boxes[0][0][3]) / 2) * radius) - (radius / 2)
                    dy = (((boxes[0][0][0] + boxes[0][0][2]) / 2) * radius) - (radius / 2)

                for class_ in classes[0][:3]:
                    if class_ == 2.0 or class_ == 4.0:
                        if scores[0][i] >= 0.4:
                            dx = (((boxes[0][i][1] + boxes[0][i][3]) / 2) * radius) - (radius / 2)
                            dy = (((boxes[0][i][0] + boxes[0][i][2]) / 2) * radius) - (radius / 2)
                            break
                    i += 1

                dx *= scale
                dy *= scale

                pyautogui.dragRel(dx, dy, 0.0)

                cv2.imshow('BOT Fritz', image_np)
                if cv2.waitKey(1) & 0xFF == ord('p'):
                    cv2.destroyAllWindows()
                    break

if __name__ == '__main__':
    main()