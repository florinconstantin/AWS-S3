#!/usr/bin/env python3

# -*-coding:utf-8 -*-

"""A python script for working with amazon S3"""
import os

import boto3
from botocore.exceptions import ClientError

ACCESS_KEY = 'AWS_ACCESS_KEY_ID'
SECRET_KEY = 'AWS_SECRET_ACCESS_KEY'
PRI_BUCKET_NAME = 'fpmlil'
TRANSIENT_BUCKET_NAME = 'fpmlil2'
F1 = "lil1.txt"
F2 = "lil2.txt"
F3 = "lil3.txt"
DIR = "/Users/fpmoles/Desktop/s3"
DOWN_DIR = "/Users/fpmoles/Desktop/s3alt"


def upload_file(bucket, directory, file, s3, s3path=None):
    file_path = directory + '/' + file
    remote_path = s3path
    if remote_path is None:
        remote_path = file
    try:
        s3.Bucket(bucket).upload_file(file_path, remote_path)
    except ClientError as ce:
        print('error', ce)


def download_file(bucket, directory, local_name, key_name, s3):
    file_path = directory + '/' + local_name
    try:
        s3.Bucket(bucket).download_file(key_name, file_path)
    except ClientError as ce:
        print('error', ce)


def delete_files(bucket, keys, s3):
    objects = []
    for key in keys:
        objects.append({'Key': key})
    try:
        s3.Bucket(bucket).delete_objects(Delete={'Objects': objects})
    except ClientError as ce:
        print('error', ce)


def list_objects(bucket, s3):
    try:
        response = s3.meta.client.list_objects(Bucket=bucket)
        objects = []
        for content in response['Contents']:
            objects.append(content['Key'])
        print(bucket, 'contains', len(objects), 'files')
        return objects
    except ClientError as ce:
        print('error', ce)


def copy_file(source_bucket, destination_bucket, source_key, destination_key, s3):
    try:
        source = {
            'Bucket': source_bucket,
            'Key': source_key
        }
        s3.Bucket(destination_bucket).copy(source, destination_key)
    except ClientError as ce:
        print('error', ce)


def prevent_public_access(bucket, s3):
    try:
        s3.meta.client.put_public_access_block(Bucket=bucket,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True
            })
    except ClientError as ce:
        print('error', ce)


def create_bucket(name, s3, secure=False):
    try:
        s3.create_bucket(Bucket=name)
        if secure:
            prevent_public_access(name, s3)
    except ClientError as ce:
        print('error', ce)


def generate_download_link(bucket, key, expiration_seconds, s3):
    try:
        response = s3.meta.client.generate_presigned_url('get_object', Params={
            'Bucket': bucket,
            'Key': key
        }, ExpiresIn=expiration_seconds)
        print(response)
    except ClientError as ce:
        print('error', ce)


def delete_bucket(bucket, s3):
    try:
        s3.Bucket(bucket).delete()
    except ClientError as ce:
        print('error', ce)


def main():
    """entry point"""
    access = os.getenv(ACCESS_KEY)
    secret = os.getenv(SECRET_KEY)
    s3 = boto3.resource('s3', aws_access_key_id=access, aws_secret_access_key=secret)

    create_bucket(TRANSIENT_BUCKET_NAME, s3)
    upload_file(TRANSIENT_BUCKET_NAME, DIR, F1, s3)
    copy_file(PRI_BUCKET_NAME, TRANSIENT_BUCKET_NAME, F3, F3, s3)
    files = list_objects(TRANSIENT_BUCKET_NAME, s3)
    print('files currently in the transient bucket are:')
    for file in files:
        print(file)
    download_file(PRI_BUCKET_NAME, DOWN_DIR, F2, F2, s3)
    generate_download_link(PRI_BUCKET_NAME, F1, 300, s3)
    delete_files(TRANSIENT_BUCKET_NAME, files, s3)
    delete_bucket(TRANSIENT_BUCKET_NAME, s3)


if __name__ == '__main__':
    main()
