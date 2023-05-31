from flask import Flask, render_template, jsonify, send_from_directory
import os
import json
import cv2
import collections, numpy
from ultralytics import YOLO
from glob import glob
from PIL import Image

app = Flask(__name__)

parsed_data = {}
model = YOLO("detect/detect/train9/weights/SCDModelV1.pt")  # build a new model from scratch
# model.export(format='onnx')
image_folder = r"pictures"  # Path to the folder containing images
output_folder = r"output"  # Path to the folder where you want to save the predicted images


def create_json_object(results, class_labels, title):
    new_object = {"title": title}

    for result in results:
        counter = collections.Counter(result.boxes.cls.numpy())
        for key in counter:
            new_object[class_labels[key]] = counter[key]
            print(class_labels[key], '->', counter[key])

    parsed_data[len(parsed_data) + 1] = new_object


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<path:filename>')
def public_files(filename):
    public_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    return send_from_directory(public_folder, filename)

@app.route('/endpoint1')
def endpoint1():
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Get a list of image files in the folder
    image_files = glob(os.path.join(image_folder, "*.jpg"))  # Modify the file extension if necessary

    # Go through the acquired images and add their details to JSON object by calling show_amount function
    for image_file in image_files:
        # Load the image
        image = Image.open(image_file)
        image_title = os.path.splitext(os.path.basename(image_file))[0]

        # Make predictions on the image
        results = model.predict(image, save=True, show=False)  # Predict on the image
        create_json_object(results, model.names, image_title)

    json_data = json.dumps(parsed_data)
    file_path = "output\output.json"

    with open(file_path, 'w') as file:
        file.write(json_data)

    cv2.waitKey(0)
    return jsonify(json_data)

@app.route('/endpoint2')
def endpoint2():
    data = {'message': 'Hello from endpoint2'}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)