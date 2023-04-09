import os
import requests
import polars as pl

API_URL = 'https://api.github.com/repos/wadefagen/datasets/contents/gpa/uiuc-gpa-dataset.csv'

def get_previous_sha(sha_file):
    previous_sha = None
    os.makedirs(os.path.dirname(sha_file), exist_ok=True)
    if os.path.exists(sha_file):
        with open(sha_file, 'r') as sha_file:
            previous_sha = sha_file.read().strip()
    return previous_sha

def get_latest_file_info(api_url=API_URL):
    response = requests.get(api_url)
    file_info = response.json()
    latest_sha = file_info['sha']
    download_url = file_info['download_url']
    return latest_sha, download_url

def download_and_convert_csv(download_url, csv_file_name, feather_file, sha_file, latest_sha, give_feedback=True):
    os.makedirs(os.path.dirname(csv_file_name), exist_ok=True)
    os.makedirs(os.path.dirname(feather_file), exist_ok=True)
    os.makedirs(os.path.dirname(sha_file), exist_ok=True)
    csv_data = requests.get(download_url).content
    with open(csv_file_name, 'wb') as csv_file:
        csv_file.write(csv_data)
    df = pl.read_csv(csv_file_name)
    df.write_ipc(feather_file)
    with open(sha_file, 'w') as sha_file_obj:
        sha_file_obj.write(latest_sha)
    print('Downloaded and converted new CSV file to Feather format.') if give_feedback else None
    print('Data is now available at {}'.format(feather_file)) if give_feedback else None
    