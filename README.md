![Freelance Banner](https://s3.eu-central-1.amazonaws.com/static.expertcoder.io/github-banner/banner.png)

## Serverless Transformations

###### Image resizing with S3 and AWS Lambda

### Why?
* uploads can be made directly to S3 to avoid load on your server
(Using Presigned URL can provide temp access to users)
* Very high scalability
* Less dependencies installed on main server

### How?

`template.yml` is a CloudFormation template (SAM Template) which creates an S3 bucket
and relevant Lambda Function and and permissions.

Actual resizing is performed via Python code and Pillow Library. PIP packages will need to
be prepared, since Pillow packages has binaries, this should be performed on an Lambda compatible
instance. see [Lambda compiler Repo](https://github.com/expertcoder/aws-lambda-php-compiler)

When uploading images to the created S3 bucket, simply prefix the object key with `_/`.

Resizing options can be set in `settings.yml`

#### Folders

*lamdba_contents:* the contents of the actual lambda function

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
