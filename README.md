## Serverless Transformations

######Image resizing with S3 and AWS Lambda



#### Folders

*lamdba_contents:* the contents of the actual lambda function

*pip_build:* Some python packages built specifically for AWS Lambda
(been stored here for the moment in the absence of a better build process)

*sam_build:* AWS SAM needs to generate a temp template with AWS references substituted


#### My Cheat Sheet

**Follow lambda logs**

awslogs get /aws/lambda/s3-transform-2-TransformFunction-16CL269YV02MF --profile sam --watch


**Upload image to S3** 

aws s3 cp ./wollongong.jpg s3://my-unique-bucket-name-298043/_/wollongong1.jpg --profile sam


**Building PIP packages**

ssh -i builder-instance.pem ec2-user@18.196.34.175

/usr/bin/pip-3.6 install <package-name> --target=./pip-packages

tar -zcvf pip-packages.tar.gz pip-packages

scp -i builder-instance.pem ec2-user@18.196.34.175:/home/ec2-user/pip-packages.tar.gz .
