#!/bin/bash

# adapted from https://github.com/chenr2/AWS-SAM-Tutorial/blob/master/deploy.sh

STAGE=dev
PROJECT=s3-transform-2
AWS_PROFILE=sam
BUCKET=lambda-artifact-temp-expertcoder
#Please pick unique bucket name

# make the deployment bucket in case it doesn't exist
aws s3 mb s3://$BUCKET --profile $AWS_PROFILE

# Need to first "package" the template. This will upload files to S3 which are needed
# the URLs in the template will be substituted for the new URLS.

# generate next stage yml file
aws cloudformation package                         \
    --template-file template.yml                   \
    --output-template-file sam_build/template.yml  \
    --s3-bucket $BUCKET                            \
    --profile $AWS_PROFILE

# the actual deployment step
aws cloudformation deploy                       \
    --template-file sam_build/template.yml      \
    --stack-name $PROJECT                       \
    --capabilities CAPABILITY_IAM               \
    --parameter-overrides Environment=$STAGE    \
    --profile $AWS_PROFILE


