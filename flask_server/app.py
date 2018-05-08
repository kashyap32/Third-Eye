
from keras.applications import VGG19
import PIL

from keras.applications import imagenet_utils
from keras.preprocessing.image import img_to_array
import numpy as np
import argparse,urllib
from PIL import Image, ImageOps
import requests
from keras import backend as K
K.set_image_dim_ordering('tf')
import tensorflow as tf
graph = tf.get_default_graph()
# from werkzeug.utils import secure_filename
import os
from StringIO import StringIO

from flask import Flask, request, redirect, url_for,make_response,jsonify
app=Flask(__name__)




inputShape = (224, 224)
preprocess = imagenet_utils.preprocess_input

# if we are using the InceptionV3 or Xception networks, then we
# need to set the input shape to (299x299) [rather than (224x224)]
# and use a different image processing function
def load_img(path, grayscale=False, target_size=None):


    response = requests.get(path)

    img = Image.open(StringIO(response.content)).resize((224,224))
    print img
    if grayscale:
        if img.mode != 'L':
            img = img.convert('L')
    else:
        if img.mode != 'RGB':
            img = img.convert('RGB')
    if target_size:
        wh_tuple = (target_size[1], target_size[0])
        if img.size != wh_tuple:
            img = img.resize(wh_tuple)
    return img
def predict(image):
    Network = VGG19
    model = Network(weights="imagenet")
    # image1 = image.resize((224,224))
    image1 = image
    image1 = img_to_array(image1)



    image1 = np.expand_dims(image1, axis=0)

    # pre-process the image using the appropriate function based on the
    # model that has been loaded (i.e., mean subtraction, scaling, etc.)
    image1 = preprocess(image1)
    # classify the image
    preds = model.predict(image1)
    P = imagenet_utils.decode_predictions(preds)
    for (i, (imagenetID, label, prob)) in enumerate(P[0]):
                print("{}. {}: {:.2f}%".format(i + 1, label, prob * 100))
    (imagenetID, label, prob) = P[0][0]

    return label
def read_image_from_url(url):
    response = requests.get(url, stream=True)

    img = Image.open(StringIO(response.content))
    img=img.resize((224,224), PIL.Image.ANTIALIAS).convert('RGB')
    print img

    return img
def read_image_from_ioreader(image_request):
    img = Image.open(BytesIO(image_request.read())).convert('RGB')
    return img
@app.route('/api/v1/classify_image', methods=['POST'])
def classify_image():
    if 'image' in request.files:
        print("Image request")
        image_request = request.files['image']
        img = read_image_from_url(image_request)
    elif 'url' in request.json:
        print("JSON request: ", request.json)
        image_url = request.json['url']
        print image_url
        img = read_image_from_url(image_url)

    else:
        abort(BAD_REQUEST)
    resp = predict(img)
    return make_response(jsonify({'message': resp}), 200)

if __name__ == '__main__':
	app.run(debug=True,port=5432)
