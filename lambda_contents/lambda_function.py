import sys
import io
import boto3
import yaml
import os
import uuid
from PIL import Image

def lambda_handler(event, context):

    object_key = event['Records'][0]['s3']['object']['key']
    bucket_name = event['Records'][0]['s3']['bucket']['name']

    print ('Object Key:' + object_key)
    print ('Bucket Name:' + bucket_name)

    unique_filename = download_s3_object(bucket_name, object_key)

    for transformation_key, transformation in get_settings()['transformations'].items():
        print ('Processing ' + transformation_key)
        resized_image_stream = io.BytesIO()
        im = Image.open(unique_filename)
        size = (transformation['width'], transformation['height'])
        im.thumbnail(size)
        im.save(resized_image_stream, "JPEG")

        # send resized image back to s3
        object_key_prefix_strip = object_key[len(os.environ['TRANSFORMATION_KEY_PREFIX']):]
        destination_key = transformation_key + '/' + object_key_prefix_strip
        client = boto3.client('s3')
        client.put_object(Body=resized_image_stream.getvalue(), Bucket=bucket_name, Key=destination_key)
        im.close()

    os.remove(unique_filename)

    return 'DONE'


def download_s3_object(bucket_name, object_key):
    # store file on lambda with unique name to prevent any mishaps with lambda instance re-use
    unique_filename = '/tmp/' + str(uuid.uuid4())
    s3 = boto3.resource('s3')
    s3.Bucket(bucket_name).download_file(object_key, unique_filename)

    return unique_filename

def get_settings():
    with open("settings.yml", 'r') as stream:
        try:
            return yaml.load(stream)
        except:
            print('failed to open settings.yml')
            sys.exit(1)


