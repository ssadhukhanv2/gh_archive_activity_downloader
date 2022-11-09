import requests


def download_file_from_gh_archive(file_name):
    res=requests.get(f'https://data.gharchive.org/{file_name}')
    return res
