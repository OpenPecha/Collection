import os
import shutil

from git import Repo
from openpecha.config import BASE_PATH

OPENPECHA_DATA_PREFIX_URL = "https://github.com/OpenPecha-Data"


def download_repo(item_id, item_path):
    item_github_url = f"{OPENPECHA_DATA_PREFIX_URL}/{item_id}"
    Repo.clone_from(item_github_url, item_path)
    return item_path


def get_item(item_id):
    item_path = BASE_PATH.as_posix() + "/" + item_id
    if os.path.exists(item_path):
        shutil.rmtree(item_path)
    repo_path = download_repo(item_id, item_path)
    return repo_path
