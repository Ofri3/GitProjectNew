#!/usr/bin/env python

import sys
import subprocess

def get_current_branch():
    try:
        return subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).strip().decode('utf-8')
    except subprocess.CalledProcessError:
        return None

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    branch = get_current_branch()

    # Check if branch is not main, exit without performing AWS credentials check
    if branch != "main":
        print("Skipping AWS credentials check on branch:", branch)
        sys.exit(0)

    aws_access_key = "AWS_ACCESS_KEY_ID"
    aws_secret_key = "AWS_SECRET_ACCESS_KEY"

    aws_credentials_found = False

    for file_path in argv:
        print("Checking file:", file_path)
        with open(file_path, 'r') as f:
            content = f.read()
        # Skip the block_aws_commits.py file
        if file_path in ["block_aws_commits.py", "init.sh", "README.md"]:
            continue

        if aws_access_key in content or aws_secret_key in content:
            print("AWS credentials found in file:", file_path)
            aws_credentials_found = True

    if aws_credentials_found:
        print("Commit blocked: AWS credentials detected.")
        sys.exit(1)
    else:
        print("No AWS credentials found in any files.")
        sys.exit(0)

if __name__ == '__main__':
    sys.exit(main())
