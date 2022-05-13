import tensorflow as tf
import numpy as np
import cv2
import pandas

from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

PATH_TO_CKPT = 'frozen_inference_graph.pb'
PATH_TO_LABELS = 'label_map.pbtxt'
NUM_CLASSES = 4

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                            use_display_name=True)
category_index = label_map_util.create_category_index(categories)

DETECTION_GRAPH = None
SESS = None

def setup():
    global SESS, DETECTION_GRAPH
    DETECTION_GRAPH = tf.Graph()
    with DETECTION_GRAPH.as_default():
        od_graph_def = tf.compat.v1.GraphDef()
        with tf.compat.v1.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.compat.v1.import_graph_def(od_graph_def, name='')
        config = tf.compat.v1.ConfigProto()
        config.gpu_options.allow_growth = True
        SESS = tf.compat.v1.Session(graph=DETECTION_GRAPH, config=config)

def detect(image):
    image_np = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
    image_np_expanded = np.expand_dims(image_np, axis=0)
    image_tensor = DETECTION_GRAPH.get_tensor_by_name('image_tensor:0')
    boxes = DETECTION_GRAPH.get_tensor_by_name('detection_boxes:0')
    scores = DETECTION_GRAPH.get_tensor_by_name('detection_scores:0')
    classes = DETECTION_GRAPH.get_tensor_by_name('detection_classes:0')
    num_detections = DETECTION_GRAPH.get_tensor_by_name('num_detections:0')

    (boxes, scores, classes, num_detections) = SESS.run(
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

    return (image_np, {'boxes': boxes[0], 'scores': scores[0], 'classes': classes[0]})