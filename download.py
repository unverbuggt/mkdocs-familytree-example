import os
import logging
import hashlib
from urllib.request import urlopen
from os.path import exists
from pathlib import Path

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def download_and_check(filename, url, hash):
    hash_md5 = hashlib.md5()
    logger = logging.getLogger("mkdocs.download_and_check")
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    if not exists(filename):
        Path(cur_dir + '/' + filename.rsplit('/',1)[0]).mkdir(parents=True, exist_ok=True)
        with urlopen(url) as response:
            filecontent = response.read()
            hash_md5.update(filecontent)
            hash_check = hash_md5.hexdigest()
            if hash == hash_check:
                with open(Path(cur_dir + '/' + filename), 'wb') as file:
                    file.write(filecontent)
                    logger.info('downloaded external asset "' + filename + '"')
            else:
                logger.error('error downloading asset "' + filename + '" hash mismatch!')
                os._exit(1)

def get_external_assets(config, **kwargs):
    download_and_check('theme_override/assets/javascripts/d3.v7.min.js',
        'https://cdn.jsdelivr.net/npm/d3@7.8.0',
        '5dff98e11655fed5aa05dd0f2fff6072')
