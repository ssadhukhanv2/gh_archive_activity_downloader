from util import get_client


def upload_to_s3(body, bucket, file_prefix, file_name):
    if file_prefix is not None:
        file_name = f'{file_prefix}/{file_name}'
    s3_client = get_client()
    res = s3_client.put_object(Bucket=bucket,
                               Key=file_name,
                               Body=body)
    return res
