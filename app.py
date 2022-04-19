from flask import Flask, render_template, request
import boto3
from botocore.errorfactory import ClientError
import logging
app = Flask(__name__)
import aws_key as keys

id = 0;
s3 = boto3.client('s3',
                    aws_access_key_id=keys.ACCESS_KEY_ID,
                    aws_secret_access_key= keys.ACCESS_SECRET_KEY,
                    aws_session_token=keys.AWS_SESSION_TOKEN
                     )
BUCKET_NAME='studentimage'

@app.route('/')  
def home():
    return render_template("checkIMGID.html")

@app.route('/checkImg', methods=['post'])
def checkImg():
    id = request.form['id']
    try: 
        if s3.head_object(Bucket = BUCKET_NAME, Key = id):
            # return doMath.html will be implemented later
            return render_template('uploadImg.html')
    except ClientError as e:
        logging.error(e) 
        return render_template('uploadImg.html')



@app.route('/upload',methods=['post'])
def upload():
    
    if request.method == 'POST':
        image = request.files['image']
        if image.filename == "":
            return "Please select a file"
        if image:
                s3.upload_file(
                    Bucket = BUCKET_NAME,
                    Filename = image,
                    Key = id,
                )
                msg = "Upload Done ! "

    return render_template("uploadImg.html",msg =msg)

if __name__ == "__main__":
    
    app.run(debug=True)