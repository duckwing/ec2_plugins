
from plugins.s3 import upload_multipart
import io

def test(*args):
    upload_multipart('test_object.txt', io.BytesIO(b'test binary data'))
