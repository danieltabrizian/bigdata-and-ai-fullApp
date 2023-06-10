from flask import Flask, render_template, jsonify, send_from_directory, request, send_file
import os
import json
import cv2
import collections, numpy
from ultralytics import YOLO
from glob import glob
from PIL import Image
import zipfile
import shutil

app = Flask(__name__)


model = YOLO("SCDModelV1.pt")
# model.export(format='onnx')
IMAGE_DIRECTORY = r"pictures"  # Path to the folder containing images
OUTPUT_DIRECTORY = r"output"  # Path to the folder where you want to save the predicted images


def create_json_object(results, class_labels, title):
    new_object = {}

    for result in results:
        counter = collections.Counter(result.boxes.cls.numpy())
        for key in counter:
            new_object[class_labels[key]] = counter[key]
            print(class_labels[key], '->', counter[key])

    return new_object

def runModelOnImages(title):
    # Create the output folder if it doesn't exist
    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

    image_directory = os.path.join(IMAGE_DIRECTORY, title)

    # Get a list of image files in the folder
    image_files = glob(os.path.join(image_directory, "*.jpg"))  # Modify the file extension if necessary

    print("IMAGE DIR: " + image_directory)
    print("IMAGE DIR: " + image_directory)
    print("IMAGE DIR: " + image_directory)
    print("IMAGE DIR: " + image_directory)

    parsed_data = {}
    # Go through the acquired images and add their details to JSON object by calling show_amount function
    for image_file in image_files:
        # Load the image
        image = Image.open(image_file)
        image_title = os.path.splitext(os.path.basename(image_file))[0]

        # Make predictions on the image
        results = model.predict(image, save=True, show=False, project="./output", name=title)  # Predict on the image
        parsed_data[image_title] = create_json_object(results, model.names, image_title)

    json_data = json.dumps(parsed_data)
    file_path = os.path.join(OUTPUT_DIRECTORY, title, 'output.json')
    output_directory = os.path.dirname(file_path)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Open the file in write mode ('w+') to create if it doesn't exist
    with open(file_path, 'w+') as file:
        file.write(json_data)

    return "Images were processed successfully. ", 200

def extract_zip_file(file):
    save_directory = "pictures"  # Name of the folder to save the files

    # Save the zip file
    zip_filepath = os.path.join(save_directory, file.filename)
    file.save(zip_filepath)

    # Extract the contents of the zip file
    folder_name = os.path.splitext(file.filename)[0]
    extract_directory = os.path.join(save_directory, folder_name)

    if not os.path.exists(extract_directory):
        os.makedirs(extract_directory)

    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        zip_ref.extractall(extract_directory)

    # Remove the zip file
    os.remove(zip_filepath)

    return "Files extracted and stored successfully."

@app.route('/upload', methods=['POST'])
def upload_images():
    if 'file' not in request.files:
        return "No file found in the request.", 400

    file = request.files['file']

    if file.filename == '':
        return "No file selected.", 400

    save_directory = "pictures"  # Name of the folder to save the files
    folder_name = os.path.splitext(file.filename)[0]

    print("FOLDER NAME::" + folder_name)
    print("FOLDER NAME::" + folder_name)
    print("FOLDER NAME::" + folder_name)
    print("FOLDER NAME::" + folder_name)

    extract_directory = os.path.join(save_directory, folder_name)

    if os.path.exists(extract_directory):
        return "Folder already exists.", 400

    extraction_result = extract_zip_file(file)

    if extraction_result != "Files extracted and stored successfully.":
        return extraction_result, 400

    result = runModelOnImages(folder_name)

    return result

@app.route('/delete/<title>', methods=['DELETE'])
def delete_folders(title):
    pictures_directory = f'pictures/{title}'
    output_directory = f'output/{title}'

    try:
        # Delete the pictures directory and its contents
        shutil.rmtree(pictures_directory)

        # Delete the output directory and its contents
        shutil.rmtree(output_directory)

        return f"Folders '{pictures_directory}' and '{output_directory}' deleted successfully.", 200
    except OSError as e:
        return f"Error deleting folders: {str(e)}", 500
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:filename>')
def public_files(filename):
    public_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    return send_from_directory(public_folder, filename)


@app.route('/datasets', methods=['GET'])
def directory_info():
    directories = []
    for dir_name in os.listdir(OUTPUT_DIRECTORY):
        dir_path = os.path.join(OUTPUT_DIRECTORY, dir_name)
        if os.path.isdir(dir_path):
            file_count = len(os.listdir(dir_path))
            directories.append({
                'directory_name': dir_name,
                'file_count': file_count
            })

    return jsonify(directories)

@app.route('/image/<dataset>/<filename>')
def get_image(dataset,filename):
    return send_file(os.path.join(OUTPUT_DIRECTORY, dataset,filename+".jpg"))

@app.route('/load/<dirname>')
def get_output(dirname):
    return send_file(os.path.join(OUTPUT_DIRECTORY, dirname,"output.json"))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=False)