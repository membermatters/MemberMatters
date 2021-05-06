#!/usr/bin/env bash

# Configure for the environment

# Input env variables
# ENV: environment, e.g. `dev`, `stage`, `demo`, `prod`

if [ -z "$ENV" ]; then
   echo "error: Environment var ENV not set" >&2
fi

# Organization that the app runs under, e.g. company or project
export ORG=gctechspace
# Application, group of services
export APP=membermatters
# Creator of resources, e.g. "ops" or a developer
export OWNER=gctechspace

# Per org + environment
export AWS_PROFILE="$ORG-$ENV"
# Per app + environment
# export AWS_PROFILE="$APP-$ENV"

# Default region
# Location where Packer will build AMI
export AWS_REGION="${AWS_REGION:-ap-southeast-2}"
export AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-ap-southeast-2}"

#####################################################
# Terraform

# EC2 keypair used when creating instances
export TF_VAR_keypair_name=$ORG-$ENV
# export TF_VAR_keypair_name=$APP-$ENV

# Set Terraform vars matching the env vars
export TF_VAR_env=$ENV
# export TF_VAR_org=$ORG
export TF_VAR_app_name=$APP
# Create versions of app name with different conventions
# Default name is expected to be hyphen
export TF_VAR_app_name_hyphen=$APP
# export TF_VAR_app_name_underscore=$(echo "$APP" | tr '-' '_')
# export TF_VAR_app_name_alpha=$(echo "$APP" | tr -d -c '[a-zA-Z0-9]')
export TF_VAR_owner=$OWNER

# Name and location of Terraform state tracking bucket
export TF_VAR_remote_state_s3_bucket_name="${ORG}-${TF_VAR_app_name_hyphen}-${ENV}-tfstate"
export TF_VAR_remote_state_s3_bucket_name_prefix="${ORG}-${TF_VAR_app_name_hyphen}"
export TF_VAR_remote_state_s3_key_prefix="${ENV}/"

# Keep the Terraform state in a single place, no matter where the resources are.
export TF_VAR_remote_state_s3_bucket_region=us-east-1
