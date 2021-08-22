from google.cloud import storage
import os
import tensorflow as tf
import numpy as np

model = None

def download_blob(bucket_name, source_blob_name, destination_prefix, model_version):
    directory = destination_prefix+'models/+'1'+'/variables'
    if not os.path.exists(directory):
        os.makedirs(directory)
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=source_blob_name+model_version)  # Get list of files
    for blob in blobs:
        blob.download_to_filename(destination_prefix + blob.name) # Download
    print('Blob {} downloaded to {}.'.format(
        source_blob_name,
        directory))

def handler(request):
    global model

    # Model load which only happens during cold starts
    if model is None:
        download_blob(bucket_name='tensorflow-ml-course-blob', source_blob_name='models/', destination_prefix = '/tmp/',  model_version='1')
        model = tf.keras.models.load_model('/tmp/models/1')
    request_json = request.get_json()
    input_np = request_json['instances']
    predictions = model.predict(input_np)
    output_string = ', '.join(str(i) for i in predictions).replace('[','').replace(']','') # Export all predictions as a flat string
    return output_string