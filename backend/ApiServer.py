from flask import Flask, jsonify, request
import requests
from PIL import Image


import os

app = Flask(__name__)
folderPath = './images'
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
    image = Image.open(f'{folderPath}/{img}')
    imgData = {'format': image.format, 'size': image.size, 'mode': image.mode}
        
    return jsonify(imgData)



if __name__ == '__main__':
    print('API server is starting')
    app.run(debug=True)
    
#Running...make sure you are in the backend folder in the terminal. Then type
#python ApiServer.py to start the server. Otherwise the image folder wont be pathed correctly. 