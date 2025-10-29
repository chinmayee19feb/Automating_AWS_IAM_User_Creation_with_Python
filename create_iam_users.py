#!/usr/bin/env python3
import csv
import pathlib
import secrets
import string
import sys
from datetime import datetime

import boto3
from botocore.exceptions import ClientError

session = boto3.Session()  # uses credentials in ~/.aws/credentials
iam = session.client("iam")

def gen_password(length: int = 16) -> str:
    alphabet = string.ascii_letters + string.digits + string.punctuation
    while True:                                    # enforce at least one of each
        pwd = "".join(secrets.choice(alphabet) for _ in range(length))
        if (any(c.islower() for c in pwd) and
            any(c.isupper() for c in pwd) and
            any(c.isdigit() for c in pwd) and
            any(c in string.punctuation for c in pwd)):
            return pwd

POLICY_ARN = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"

def create_user(username: str, password: str) -> None:
    try:
        iam.create_user(UserName=username)
        print(f"✅  User {username} created")

        iam.create_login_profile(
            UserName=username,
            Password=password,
            PasswordResetRequired=True,
        )
        print(f"🔑  Login profile set")

        iam.attach_user_policy(UserName=username, PolicyArn=POLICY_ARN)
        print(f"📜  Policy attached\n")

    except ClientError as e:
        print(f"⚠️  Skipped {username}: {e.response['Error']['Message']}")

INPUT_CSV = pathlib.Path("employees.csv")
OUTPUT_CSV = pathlib.Path("credentials.csv")

def main() -> None:
    if not INPUT_CSV.exists():
        sys.exit("employees.csv not found - aborting.")

    first_run = not OUTPUT_CSV.exists()
    with open(INPUT_CSV, newline="") as infile, \
         open(OUTPUT_CSV, "a", newline="") as outfile:

        reader = csv.DictReader(infile)
        writer = csv.writer(outfile)

        if first_run:
            writer.writerow(["username", "password", "created_at"])

        for row in reader:
            username = f"{row['first_name'].lower()}.{row['last_name'].lower()}"
            password = gen_password()

            create_user(username, password)
            writer.writerow([username, password, datetime.utcnow().isoformat()])

if __name__ == "__main__":
    main()

