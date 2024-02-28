#!/usr/bin/env python

import re
import sys

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    aws_key_pattern = re.compile(r'AKIA[0-9A-Z]{16}', re.IGNORECASE)
    aws_secret_pattern = re.compile(r'[0-9a-zA-Z/+]{40}', re.IGNORECASE)

    aws_credentials_found = False

    for file_path in argv:
        with open(file_path, 'r') as f:
            content = f.read()

        if aws_key_pattern.search(content) or aws_secret_pattern.search(content):
            print("AWS credentials found in file:", file_path)
            aws_credentials_found = True

    if aws_credentials_found:
        print("Commit blocked: AWS credentials detected.")
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == '__main__':
    sys.exit(main())
