
from bootstrap import invoke_plugin
from boto import config as boto_config
import boto.sqs
import plugins.isolate

MESSAGE_PING = 5 # seconds
MESSAGE_VISIBILITY = MESSAGE_PING * 2

def listen():
    region = boto_config['plugins']['region']
    sqs_queue = boto_config['plugins']['sqs_listener_queue']
    conn = boto.sqs.connect_to_region(region, profile_name='sqs_listener')
    queue = conn.get_queue(sqs_queue)

    while True:
        msg = queue.read(visibility_timeout=MESSAGE_VISIBILITY,
                         message_attributes=['All'])
        if msg is None:
            continue

        cmd = msg.message_attributes['CMD']['string_value']
        plugins.isolate.isolate(_make_plugin_invoker(cmd))

def _make_plugin_invoker(cmd):
    def invoker():
        return invoke_plugin(cmd)
    return invoker
