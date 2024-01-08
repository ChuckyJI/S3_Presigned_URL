import unittest
import requests
import time
from config import AWS_ACCESS_KEY_ID, AWS_BUCKET_NAME, AWS_BUCKET_KEY
from backend import generate_presigned_post

EXPIRESIN = 600
SLEEPING_TIME = 5


class TestUploading(unittest.TestCase):

    #  test whether the essencial information are all in the response which are the key elements when generating the temporary url
    def test_generate_the_url(self):
        #  The response shoule be like this: https://<bucket name>.s3.amazonaws.com/<bucket key>/<file name>.mp4?AWSAccessKeyId=<ID name>&Signature=XXX%3D&content-type=video%2Fmp4&Expires=1704695244
        response = generate_presigned_post('test.mp4', EXPIRESIN)
        responseList = response.split('&')
        prefix = responseList[0]
        signature = responseList[1]
        contentType = responseList[2]
        expiresIn = responseList[3]

        prefixRefer = "https://" + AWS_BUCKET_NAME + ".s3.amazonaws.com/" + \
            AWS_BUCKET_KEY + "test.mp4?AWSAccessKeyId=" + AWS_ACCESS_KEY_ID
        self.assertEqual(prefix, prefixRefer)
        self.assertIn('Signature=', signature)
        self.assertEqual(contentType, 'content-type=video%2Fmp4')
        self.assertIn('Expires=', expiresIn)

    # test whether the file can be uploaded to s3 with the temporary url
    def test_normal_upload(self):
        temporaryUrl = generate_presigned_post('test.mp4', EXPIRESIN)
        file_path = 'templates/test.mp4'

        with open(file_path, 'rb') as file:
            headers = {'Content-Type': 'video/mp4'}
            response = requests.put(temporaryUrl, files={
                                    'file': (file.name, file)}, headers=headers)
            self.assertEqual(response.status_code, 200)

    # test whether the file can be uploaded to s3 with the temporary url but exceed the time limit
    def test_timeout_upload(self):
        temporaryUrl = generate_presigned_post('test.mp4', SLEEPING_TIME)
        file_path = 'templates/test.mp4'

        time.sleep(SLEEPING_TIME)

        with open(file_path, 'rb') as file:
            headers = {'Content-Type': 'video/mp4'}
            response = requests.put(temporaryUrl, files={
                                    'file': (file.name, file)}, headers=headers)
            self.assertEqual(response.status_code, 403)


if __name__ == '__main__':
    unittest.main()
