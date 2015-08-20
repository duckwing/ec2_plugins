from boto import config
from boto.s3.connection import S3Connection
from concurrent.futures import ThreadPoolExecutor
from traceback import print_exc
import io

def upload_multipart(*args):    # see _uploader
    pool = ThreadPoolExecutor(1)
    pool.submit(_uploader, *args)
    pool.shutdown()

def _uploader(object_key, inp_file):
    print('thread started')
    def get_chunk():
        return inp_file.read(20000000)

    conn = S3Connection(profile_name='s3up')
    buck = conn.get_bucket(config['plugins']['s3_bucket'])

    assert object_key
    multi = buck.initiate_multipart_upload(object_key)
    part_num = 1
    try:
        ch = get_chunk()
        while ch:
            multi.upload_part_from_file(io.BytesIO(ch), part_num)
            part_num += 1
            ch = get_chunk()
        multi.complete_upload()
        print('Upload finished')
    except:
        print('Canceling upload due to error')
        multi.cancel_upload()
        print_exc()
        raise
    finally:
        inp_file.close()
