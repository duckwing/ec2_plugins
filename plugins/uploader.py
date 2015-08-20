
from boto import config
from subprocess import Popen, PIPE
from plugins import s3

def upload_all(object_key):
    print('Uploading to {}'.format(object_key))
    recipients = config['plugins']['uploader_keys']
    recipients = [item for r in recipients.split(',')
                       for item in ['-r', r]]
    tar = Popen(['tar', 'cv', '.'], stdout=PIPE)
    gpg = Popen(['gpg', '-e'] + recipients, stdin=tar.stdout, stdout=PIPE)
    pv = Popen(['pv'], stdin=gpg.stdout, stdout=PIPE)
    tar.stdout.close()
    gpg.stdout.close()
    s3.upload_multipart(object_key, pv.stdout)
    res1 = tar.wait()
    res2 = gpg.wait()
    res3 = pv.wait()
    assert res1 == res2 == res3 == 0

def test_upload_all():
    from plugins.isolate import isolate
    isolate(upload_all, 'snapshot')
