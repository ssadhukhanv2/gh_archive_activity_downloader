import os
from datetime import datetime, timedelta

import boto3
from botocore.errorfactory import ClientError


def get_client():
    environ = os.environ.get('ENVIRON')
    profile = os.environ.get('PROFILE')
    print(f'Profile configured: {profile}')
    print(f'Running in {environ} environment')
    if environ == 'DEV':
        s3_session = boto3.Session(profile_name=profile)
        s3_client = s3_session.client('s3')
    else:
        s3_client = boto3.client('s3')
    return s3_client


def get_prev_file_name(bucket, file_prefix, bookmark_file, baseline_file):
    s3_client = get_client()
    try:
        bookmark_file = s3_client.get_object(
            Bucket=bucket,
            Key=f'{file_prefix}/{bookmark_file}'
        )
        prev_file = bookmark_file['Body'].read().decode('utf-8')
        print(f"Setting previous file to contents in the Bookmark: {prev_file}")
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            prev_file = baseline_file
            print(f"Bookmark not available, setting previous file to baseline value: {baseline_file}")
        else:
            raise
    return prev_file


# Sample filename for prev_file 2022-11-08-0.json.gz
def get_next_file_name(prev_file):
    date_part_prev_file_str = prev_file.split('.')[0]
    prev_file_datetime = datetime.strptime(date_part_prev_file_str, '%Y-%M-%d-%H')
    next_file_datetime = prev_file_datetime + timedelta(hours=1)
    environ = os.environ.get('ENVIRON')
    print(f'Running in {environ} environment')
    if environ == 'DEV':
        date_part_next_file_str = datetime.strftime(next_file_datetime, '%Y-%M-%d-%#H')
    else:
        date_part_next_file_str = datetime.strftime(next_file_datetime, '%Y-%M-%d-%-H')
    next_file = f"{date_part_next_file_str}.json.gz"
    return next_file
