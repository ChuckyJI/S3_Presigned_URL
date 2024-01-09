import boto3
from config import AWS_ACCESS_KEY_ID, AWS_ACCESS_KEY_SECRET, AWS_BUCKET_NAME, AWS_BUCKET_KEY
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

EXPIRESIN = 600


def generate_presigned_post(FILE_ROUTE, EXPIRESIN):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_ACCESS_KEY_SECRET,
    )

    response = s3_client.generate_presigned_url(
        'put_object',
        Params={"Bucket": AWS_BUCKET_NAME,
                "Key": AWS_BUCKET_KEY + FILE_ROUTE,
                'ContentType': 'video/mp4', },
        ExpiresIn=EXPIRESIN,
        HttpMethod='PUT'
    )

    return response


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    file_name = request.get_json()
    getResponse = generate_presigned_post(file_name['fileName'], EXPIRESIN)
    return jsonify(data=getResponse)


if __name__ == '__main__':
    app.run(debug=True)
