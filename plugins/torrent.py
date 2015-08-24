
from plugins import aria, uploader

def download_magnet(object_key, magnet_link):
    aria.download_torrent(magnet_link)
    uploader.upload_all(object_key)
