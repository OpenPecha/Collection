import os
import shutil
import uuid
from pathlib import Path
from typing import List

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


def get_fragment_id():
    return uuid.uuid4().hex[:4]


def get_opf_bases(opf_path: Path, base_names: List = None):
    """
    This function gives the bases of a given opf or path of bases

    :param opf_path: path of opf
    :base_names: List of Base names
    :return: list of bases path in Path obj
    """
    pecha_id = opf_path.stem
    bases = list(Path(f"{opf_path.as_posix()}/{pecha_id}.opf/base").iterdir())
    ret_bases = []
    if base_names:
        for base in bases:
            if base.stem in base_names:
                ret_bases.append(base)
    else:
        ret_bases = bases
    return ret_bases
