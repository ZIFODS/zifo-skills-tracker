#!/bin/bash

AWS_ACCOUNT_ID="233044492909"
AWS_REGION="eu-west-2"

# Frontend
ECR_REPO_NAME_FRONTEND="skills-tracker-frontend"
ECR_REPO_URI_FRONTEND="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO_NAME_FRONTEND"

docker build -t "$ECR_REPO_URI_FRONTEND:latest" -f docker/frontend/Dockerfile .

# API
ECR_REPO_NAME_API="skills-tracker-api"
ECR_REPO_URI_API="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO_NAME_API"

docker build -t "$ECR_REPO_URI_API:latest" -f docker/api/Dockerfile .
