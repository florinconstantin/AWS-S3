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


def main():
    """entry point"""
    access = os.getenv(ACCESS_KEY)
    secret = os.getenv(SECRET_KEY)
    s3 = boto3.resource('s3', aws_access_key_id=access, aws_secret_access_key=secret)

    upload_file(PRI_BUCKET_NAME, DIR, F1, s3)
    upload_file(PRI_BUCKET_NAME, DIR, F2, s3)
    upload_file(PRI_BUCKET_NAME, DIR, F3, s3)

    download_file(PRI_BUCKET_NAME, DOWN_DIR, F3, F3, s3)

    delete_files(PRI_BUCKET_NAME, [F1, F2, F3], s3)


def create_bucket(name, s3):
    try:
        bucket = s3.create_bucket(Bucket=name)
    except ClientError as ce:
        print('error', ce)


if __name__ == '__main__':
    main()
