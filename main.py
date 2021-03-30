import base64
import re

import boto3


def create_presigned_url(bucket_name: str, obj_name: str, expiration: int):
    client = boto3.client('s3')
    response = client.generate_presigned_url('get_object',
                                             Params={'Bucket': bucket_name,
                                                     'Key': obj_name},
                                             ExpiresIn=expiration)
    return response


def b64_encode(image_uri: str) -> str:
    with open(image_uri, 'rb') as file:
        encoded_str = base64.b64encode(file.read())
    return encoded_str.decode('utf-8')


def s3_upload_b64(image_b64: str, bucket_name: str, s3_filename: str):
    s3 = boto3.resource('s3')
    obj = s3.Object(bucket_name, s3_filename)
    file_ext = re.findall("[^.]+$", s3_filename)[0]
    response = obj.put(Body=base64.b64decode(image_b64), ContentType=f'image/{file_ext}')
    return response


if __name__ == "__main__":
    _bucket_name = ''
    _image_uri = ''
    b64 = b64_encode(image_uri=_image_uri)
    upload_resp = s3_upload_b64(image_b64=b64, bucket_name=_bucket_name, s3_filename=_image_uri)
    url = create_presigned_url(_bucket_name, _image_uri, expiration=300)
    print(f'presigned_url: {url}')
