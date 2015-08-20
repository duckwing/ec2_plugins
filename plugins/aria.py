import subprocess

def download(url_or_file):
    return _invoke(url_or_file)

def download_torrent(file_or_magnet):
    return _invoke('--seed-time', '0', file_or_magnet)

def _invoke(*args):
    subprocess.check_call(['aria2c'] + list(args))
