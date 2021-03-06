from flask import Flask, render_template, request
import boto3
from botocore.errorfactory import ClientError
from werkzeug.utils import secure_filename
import logging
app = Flask(__name__)
import aws_key as keys
import requests

id = '0';
s3 = boto3.client('s3',
                    aws_access_key_id=keys.ACCESS_KEY_ID,
                    aws_secret_access_key= keys.ACCESS_SECRET_KEY,
                    aws_session_token=keys.AWS_SESSION_TOKEN
                     )
BUCKET_NAME='studentimage'

@app.route('/')  
def home():
    return render_template("checkImgID.html")

@app.route('/checkImg', methods=['post'])
def checkImg():
    id = request.form['id']
    try: 
        if s3.head_object(Bucket = BUCKET_NAME, Key = id):
            msg = 'You already have an image, don\'t need to upload anymore'
            # params={'key': id}
            # URL='https://3853o61h68.execute-api.us-east-1.amazonaws.com/v1/s3?key=studentimage/0'
            # r = requests.request("GET", URL, params=params)
            # print(r)
            # return doMath.html will be implemented later
            return render_template('uploadImg.html', msg=msg)
    except ClientError as e:
        logging.error(e) 
        msg = 'You do not have any images yet. Please upload one!'
        return render_template('uploadImg.html', msg=msg)



@app.route('/upload',methods=['post'])
def upload():
    id = request.form['id']
    if request.method == 'POST':
        image = request.files['image']
        if image.filename == "":
            return "Please select a file"
        if image:
            filename = secure_filename(image.filename)
            image.save(filename)
            s3.upload_file(
                Bucket = BUCKET_NAME,
                Filename=filename,
                Key = id,
            )
            msg = "Upload Done ! "

    return render_template("uploadImg.html",msg =msg)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
    # app.run(debug=True)