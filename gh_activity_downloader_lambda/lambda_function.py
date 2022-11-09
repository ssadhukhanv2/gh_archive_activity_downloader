import time

import util
import json
import os
import downloader
import uploader


def lambda_handler(event, context):
    profile = os.environ.get('PROFILE')
    environ = os.environ.get('ENVIRON')
    bucket_name = os.environ.get('BUCKET_NAME')
    bookmark_file = os.environ.get('BOOKMARK_FILE')
    baseline_file = os.environ.get('BASELINE_FILE')
    file_prefix = os.environ.get('FILE_PREFIX')

    print(f'Profile configured: {profile}')
    print(f'Running in {environ} environment')
    print(f'Bucket Name: {bucket_name}')
    print(f'Bookmark File Name: {bookmark_file}')
    print(f'Baseline File Name: {baseline_file}')
    print(f'File Prefix: {file_prefix}')

    while True:

        prev_file = util.get_prev_file_name(bucket_name, file_prefix, bookmark_file, baseline_file)
        next_file = util.get_next_file_name(prev_file)
        print(f"Previous file: {prev_file}")
        print(f"Next file: {next_file}")

        start_time = time.time()
        download_res = downloader.download_file_from_gh_archive(next_file)
        end_time = time.time()
        print(f"{next_file} downloaded in {end_time - start_time}")

        if download_res.status_code != 200:
            print(f"Invalid file name {next_file}. Downloaded till {prev_file}")
            break

        start_time = time.time()
        upload_res = uploader.upload_to_s3(body=download_res.content,
                                           bucket=bucket_name,
                                           file_prefix=file_prefix,
                                           file_name=next_file)
        end_time = time.time()
        print(f"{file_prefix}/{next_file} upload to s3 bucket: {bucket_name} in {end_time - start_time}")

        start_time = time.time()
        upload_bookmark_res = uploader.upload_to_s3(body=next_file.encode("utf-8"),
                                                    bucket=bucket_name,
                                                    file_prefix=file_prefix,
                                                    file_name=bookmark_file)
        end_time = time.time()
        print(f"{file_prefix}/{next_file} upload to s3 bucket: {bucket_name} in {end_time - start_time}")

    return upload_res
