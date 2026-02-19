from flask import Flask, jsonify, request, send_file
import requests
from PIL import Image
import os


app = Flask(__name__)
server_root = os.path.dirname(os.path.abspath(__file__))
folderPath = os.path.join(server_root, "images")
@app.route('/', methods=['GET']) 
def homepage():
    
    return 'New Flask App!'

# I do not understand Part A a...Do we need a function to populate \backend\images? Or manually load the folder with images from part1????#

#Retrieve all images from the folder defined in folderPath and return the file names as a JSON payload
@app.route('/allImages', methods=['GET'])
def get_all_images():
    #Utilizing os and the function listdir while passing folderpath as an argument to capture all the 
    #files within the specified folder and forms a list
    allMembers = os.listdir(folderPath) 
    return jsonify(allMembers)

#The path param <img> is captured in the URL. img being the name of the image the user selects
#This value is then concatinated in an arg for Image.open with folderPath.
@app.route('/oneImage/<img>', methods=['GET'])
def get_one_image(img):
    img_path = os.path.join(folderPath, img)
    image = Image.open(img_path)
    imgData = {'format': image.format, 'size': image.size, 'mode': image.mode}
        
    return send_file(img_path, mimetype=f'image/{image.format.lower()}')


#Works tested in postman go to body/ form-data radiobutton/ key = image, File in dropdown, value = selecting img from local machine. 
@app.route('/upload', methods=['POST'])
def upload_image(): 
    #Checks if the image was actually sent, if image is absent from the http req this message will be displayed. 
    if "image" not in request.files:
        return jsonify({"error": "No image sent in request!"})
    
    #assigning image to file, image is passed in via the HTTP request object its and its catergory is "files"
    file = request.files['image']
    image = Image.open(file)
    
    #concatetanating the folder path and the image name then passing savepath as an argument to file.save() which will save it.
    save_filename = os.path.splitext(file.filename)[0] + ".png"
    savepath = os.path.join(folderPath, save_filename)
    image.save(savepath, format="PNG")
    
    return jsonify({"message": "Image is successfully saved!"})




#Tested with postman it works! Similar to retrieving a single image except using os to remove the file send
#via the path param.
@app.route('/delete/<img>', methods=['DELETE'])
def delete_img(img):
    os.remove(f'{folderPath}/{img}')
    return f'{img} has been deleted'
    

if __name__ == '__main__':
    print('API server is starting')
    app.run(debug=True)
    
#Running...make sure you are in the backend folder in the terminal. Then type
#python ApiServer.py to start the server. Otherwise the image folder wont be pathed correctly. 