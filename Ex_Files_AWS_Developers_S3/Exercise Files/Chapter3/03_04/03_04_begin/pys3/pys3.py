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


def main():
    """entry point"""
    access = os.getenv(ACCESS_KEY)
    secret = os.getenv(SECRET_KEY)
    s3 = boto3.resource('s3', aws_access_key_id=access, aws_secret_access_key=secret)

    create_bucket(TRANSIENT_BUCKET_NAME, s3)


def create_bucket(name, s3):
    try:
        bucket = s3.create_bucket(Bucket=name)
    except ClientError as ce:
        print('error', ce)


if __name__ == '__main__':
    main()
