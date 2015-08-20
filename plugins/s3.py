from boto import config
from boto.s3.connection import S3Connection
from threading import Thread
import io

def upload_multipart(*args):    # see _uploader
    th = Thread(name='uploader', target=_uploader, args=args)
    th.start()

def _uploader(object_key, inp_file):
    def get_chunk():
        return inp_file.read(20000000)

    conn = S3Connection(profile_name='s3up')
    buck = conn.get_bucket(config['plugins']['s3_bucket'])

    assert object_key
    multi = buck.initiate_multipart_upload(object_key)
    part_num = 1
    try:
        chunk = get_chunk()
        while chunk:
            multi.upload_part_from_file(io.BytesIO(chunk), part_num)
            part_num += 1
            chunk = get_chunk()
        multi.complete_upload()
        print('Upload finished')
    except Exception as e:
        print('Canceling upload due to error')
        multi.cancel_upload()
        raise
    finally:
        inp_file.close()
