
from boto import config
from subprocess import Popen, PIPE
from plugins import s3

def upload_all(bucket_name):
    recipients = config['plugins']['uploader_keys']
    recipients = [item for r in recipients.split(',')
                       for item in ['-r', r]]
    tar = Popen(['tar', 'cv', '.'], stdout=PIPE)
    gpg = Popen(['gpg', '-e'] + recipients, stdin=tar.stdout, stdout=PIPE)
    pv = Popen(['pv'], stdin=gpg.stdout, stdout=PIPE)
    tar.stdout.close()
    gpg.stdout.close()
    s3.upload_multipart(bucket_name, pv.stdout)

def test_upload_all():
    upload_all('snapshot')
