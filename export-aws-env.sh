#!/bin/bash

PROFILE=${1:-default}

export AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id --profile "$PROFILE")
export AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key --profile "$PROFILE")
export AWS_SESSION_TOKEN=$(aws configure get aws_session_token --profile "$PROFILE")
export AWS_DEFAULT_REGION=$(aws configure get region --profile "$PROFILE")

echo "AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID"
echo "AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY"
echo "AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN"
echo "AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION"

