from flask import Flask, request, jsonify
from PIL import Image
import cv2
import numpy as np
import os

app = Flask(__name__)

recog_weights_path = "./models/recog.weights"
recog_cfg_path = "./models/recog.cfg"
recog_classes_path = "./models/recog.txt"
recog_net = cv2.dnn.readNet(recog_weights_path, recog_cfg_path)

UPLOAD_PATH = 'uploads/'

with open(recog_classes_path, 'r') as f:
    recog_classes = [line.strip() for line in f.readlines()]

# function to get the output layer names
# in the architecture
def get_output_layers(net):
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    return output_layers
def process_recog(image):
    scale = 0.00392
    # read pre-trained model and config file
    # create input blob

    blob = cv2.dnn.blobFromImage(image, scale, (300, 100), (0, 0, 0), True, crop=False)

    # set input blob for the network
    recog_net.setInput(blob)

    # run inference through the network
    # and gather predictions from output layers
    outs = recog_net.forward(get_output_layers(recog_net))

    # initialization
    class_ids = []
    confidences = []
    boxes = []
    center_X = []
    conf_threshold = 0.3
    nms_threshold = 0.2

    # for each detetion from each output layer
    # get the confidence, class id, bounding box params
    # and ignore weak detections (confidence < 0.5)
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.3:
                center_x = int(detection[0] * image.shape[1])
                center_y = int(detection[1] * image.shape[0])
                w = int(detection[2] * image.shape[1])
                h = int(detection[3] * image.shape[0])
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])
                center_X.append(center_x)

    # apply non-max suppression
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    # go through the detections remaining
    # after nms and draw bounding box

    result = ''
    valid_boxes = []
    valid_classids = []
    valid_centerX = []
    valid_centerY = []
    valid_centerH = []

    lineFlag = False
    average_heightY = 0
    for i in indices:
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]

        valid_boxes.append(box)
        valid_classids.append(class_ids[i])
        valid_centerX.append(round(x))
        valid_centerY.append(round(y))
        valid_centerH.append(round(w))
        average_heightY = average_heightY + round(y + h / 2)

    if (len(valid_centerY) > 0):
        average_heightY = average_heightY / len(valid_centerY)

    for i in range(0, len(valid_centerX)):
        if (valid_centerY[i] > average_heightY):
            lineFlag = True
            break
    if (lineFlag == False):
        for i in range(0, len(valid_centerX)):
            for j in range(i + 1, len(valid_centerX)):
                if valid_centerX[i] > valid_centerX[j]:
                    temp = valid_centerX[i]
                    valid_centerX[i] = valid_centerX[j]
                    valid_centerX[j] = temp

                    tem = valid_classids[i]
                    valid_classids[i] = valid_classids[j]
                    valid_classids[j] = tem
        for i in range(0, len(valid_classids)):
            result += recog_classes[valid_classids[i]]
    else:
        first_valid_centerX = []
        first_valid_classids = []
        second_valid_centerX = []
        second_valid_classids = []
        for i in range(0, len(valid_centerX)):
            if (round(valid_centerY[i] + valid_centerH[i] / 2) < average_heightY):
                first_valid_centerX.append(valid_centerX[i])
                first_valid_classids.append(valid_classids[i])
            else:
                second_valid_centerX.append(valid_centerX[i])
                second_valid_classids.append(valid_classids[i])

        for i in range(0, len(first_valid_centerX)):
            for j in range(i + 1, len(first_valid_centerX)):
                if first_valid_centerX[i] > first_valid_centerX[j]:
                    temp = first_valid_centerX[i]
                    first_valid_centerX[i] = first_valid_centerX[j]
                    first_valid_centerX[j] = temp

                    tem = first_valid_classids[i]
                    first_valid_classids[i] = first_valid_classids[j]
                    first_valid_classids[j] = tem
        for i in range(0, len(first_valid_classids)):
            result += recog_classes[first_valid_classids[i]]

        for i in range(0, len(second_valid_centerX)):
            for j in range(i + 1, len(second_valid_centerX)):
                if second_valid_centerX[i] > second_valid_centerX[j]:
                    temp = second_valid_centerX[i]
                    second_valid_centerX[i] = second_valid_centerX[j]
                    second_valid_centerX[j] = temp

                    tem = second_valid_classids[i]
                    second_valid_classids[i] = second_valid_classids[j]
                    second_valid_classids[j] = tem
        for i in range(0, len(second_valid_classids)):
            result += recog_classes[second_valid_classids[i]]

    return result

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
       return jsonify({'error': 'No image part'})

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    file_name = file.filename
    type = file.content_type.lower().split('/')[1]

    if type != 'png' and type != 'bmp' and type != 'jpg':
        return jsonify({'file type error': 'Invalid file type'})

    file.save(os.path.join(UPLOAD_PATH, file_name))

    if file:
        try:
            img = cv2.imread(os.path.join(UPLOAD_PATH, file.filename))
            if img is not None:
                try:
                    text = process_recog(img)
                except Exception as e:
                    print(f"An error occurred while trying to detect captcha: {str(e)}")

                if text:
                    return jsonify({'Detected captcha': text})
                else:
                    return jsonify({'Detection Error': "Please try with another image file."})
            else:
                try:
                    cv_gif = cv2.VideoCapture(os.path.join(UPLOAD_PATH, file.filename))
                except Exception as e:
                    print(f"An error occurred while trying to load the image with VideoCapture: {str(e)}")

                success, img = cv_gif.read()
                try:
                    text = process_recog(img)
                except Exception as e:
                    print(f"An error occurred while trying to detect captcha: {str(e)}")
                if text:
                    return jsonify({'Detected captcha': text})
                else:
                    return jsonify({'Detection Error': "Please try with another image file."})

        except Exception as e:
            print(f"An error occurred while trying to load the image: {str(e)}")



if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # # parser.add_argument("--image", '-i',  help='image path')
    # args = parser.parse_args()
    app.run(debug=True)
