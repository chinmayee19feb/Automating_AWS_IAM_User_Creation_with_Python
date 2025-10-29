#!/usr/bin/env python3
import csv
import boto3

iam = boto3.client("iam")
POLICY_ARN = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"

with open("credentials.csv") as f:
    next(f)  # skip header
    for line in f:
        username = line.split(",")[0]

        try:
            iam.delete_login_profile(UserName=username)
            iam.detach_user_policy(UserName=username, PolicyArn=POLICY_ARN)
            iam.delete_user(UserName=username)
            print(f"🗑️  Deleted {username}")
        except iam.exceptions.NoSuchEntityException:
            print(f"⚠️  {username} already gone")
