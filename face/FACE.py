import cv2
import numpy as np
from keras.models import model_from_json
import base64
import face.CNN_MODEL as cnn
import sys
import time
import tensorflow as tf

import face.label_map_util as label_map_util
import face.visualization_utils_color as vis_util

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = 'face/frozen_inference_graph_face.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = 'face/face_label_map.pbtxt'

NUM_CLASSES = 2

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

class TensoflowFaceDector(object):
    def __init__(self, PATH_TO_CKPT):
        """Tensorflow detector
        """

        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')


        with self.detection_graph.as_default():
            config = tf.ConfigProto()
            config.gpu_options.allow_growth = True
            with tf.Session(graph=self.detection_graph, config=config) as self.sess:

                self.windowNotSet = True


    def run(self, image):
        """image: bgr image
        return (boxes, scores, classes, num_detections)
        """

        image_np = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # the array based representation of the image will be used later in order to prepare the
        # result image with boxes and labels on it.
        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(image_np, axis=0)
        image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
        # Each box represents a part of the image where a particular object was detected.
        boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
        # Each score represent how level of confidence for each of the objects.
        # Score is shown on the result image, together with the class label.
        scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
        classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
        num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')
        # Actual detection.
        start_time = time.time()
        (boxes, scores, classes, num_detections) = self.sess.run(
            [boxes, scores, classes, num_detections],
            feed_dict={image_tensor: image_np_expanded})
        elapsed_time = time.time() - start_time
        #print('inference time cost: {}'.format(elapsed_time))

        return (boxes, scores, classes, num_detections)


def predict_emotion(face_image_gray,sess):
    resized_img = cv2.resize(face_image_gray, (48,48), interpolation = cv2.INTER_AREA)
    pixel = np.zeros((48,48))
    for i in range(48):
        for j in range(48):
            pixel[i][j] = resized_img[i][j]
    list = cnn.Predict(pixel,sess)
    
    return list[0]

def get_emotion(strr):
    sess = cnn.Initialize()
    data = base64.b64decode(strr)
    dataStr =  np.fromstring(data, np.uint8)
    image = cv2.imdecode(dataStr,cv2.IMREAD_COLOR)
    (height, width) = image.shape[:2]
    tDetector = TensoflowFaceDector(PATH_TO_CKPT)
    (boxes, scores, classes, num_detections) = tDetector.run(image)
    boxes = np.squeeze(boxes)
    scores = np.squeeze(scores)

    box = np.zeros(4)
    if scores[0] < 0.1:
        for i in range(6):
            if boxes[i][2] - boxes[i][0] > 0.1 and boxes[i][2] - boxes[i][0] < 0.5:
                box = boxes[i]
                break
    else:
        box = boxes[0]

    (ymin, xmin, ymax, xmax) = (int(box[0]*height), int(box[1]*width), int(box[2]*height), int(box[3]*width))
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_image_gray = img_gray[ymin:ymax, xmin:xmax]

    #cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
    #cv2.imwrite(str(ymin)+".png", image)

    list= predict_emotion(face_image_gray,sess)
    ret = []
    ret += [(int)(list[3]+list[5]-list[0]-list[1]-list[2]-list[4])]
    sess.close()
    return ret


'''
def get_emotion(str,faceCascade,sess):
    data =base64.b64decode(str)
    dataStr =  np.fromstring(data, np.uint8)
    frame = cv2.imdecode(dataStr,cv2.IMREAD_COLOR)
    cv2.imwrite("save.png", frame)
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("savegray.png", img_gray)

    faces = faceCascade.detectMultiScale(
        img_gray,
        scaleFactor=1.1,
        minNeighbors=3,
        minSize=(48, 48),
        flags= cv2.CASCADE_SCALE_IMAGE
    )
    ret = []
    for (x, y, w, h) in faces:
        face_image_gray = img_gray[y:y+h, x:x+w]
        #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        list= predict_emotion(face_image_gray,sess)
        # list = ["angry","disgust","fear","happy","sad","surprise","neutral"]
        ret += [(int)(list[3]+list[5]-list[0]-list[1]-list[2]-list[4])]
    return ret
'''