
from traceback import print_exc
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError # for handling future timeouts
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

    with ThreadPoolExecutor(1) as pool:
        while True:
            msg = queue.read(visibility_timeout=MESSAGE_VISIBILITY)
            if msg is None:
                continue
            cmd = msg.get_body().splitlines()
            if len(cmd) < 0:
                print('Skipping invalid message')
                continue
            async_result = pool.submit(_run_isolated, cmd)
            try:
                _monitor_message_completion(async_result, msg)
                print('Successfully processed a message')
                queue.delete_message(msg)
            except:
                print_exc()

def _monitor_message_completion(async_result, msg):
    while True:
        try:
            return async_result.result(MESSAGE_PING)
        except TimeoutError:
            pass
        msg.change_visibility(MESSAGE_VISIBILITY)

def _run_isolated(cmd):
    plugin_cmd = cmd[0]
    cmd_args = cmd[1:]
    return plugins.isolate.isolate(invoke_plugin, plugin_cmd, *cmd_args)
