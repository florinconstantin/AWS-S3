#!/bin/bash

aws s3 mb s3://fpmchal1
echo "This is from the challange" >> ~/Desktop/s3/lil3.txt
aws s3 sync ~/Desktop/s3 s3://fpmchal1
aws s3 ls s3://fpmchal1

