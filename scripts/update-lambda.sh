#! /bin/bash

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
LAMBDA_FUNCTION="${1:-arn:aws:lambda:us-east-1:....}"
AWS_REGION="us-east-1"

echo "Installing lambda deploy dependencies"
apt-get update && apt-get install zip -y

echo "Remove previous lambda.zip if exists"
rm -fr lambda.zip

echo "Building lambda zip..."
cd $DIR/..
zip -r lambda index.py amos_skill/*

echo "Updating lambda function..."
aws lambda update-function-code --function-name $LAMBDA_FUNCTION --zip-file fileb://lambda.zip --region $AWS_REGION

echo "Done."