#!/usr/bin/python3

import sys, os
import importlib.abc, importlib.util
import urllib.parse, urllib.request

def main():
    if len(sys.argv) != 2:
        usage()
        return 1
    hook_plugins()
    return invoke_plugin(sys.argv[1])

def get_config():
    from boto.pyami.config import Config
    return Config()

def import_plugin(plugin_name):
    return importlib.import_module('plugins.' + plugin_name)

def invoke_plugin(cmd):
    plugin, func = cmd.split('.', 1)
    print('Running {}.{}'.format(plugin, func))
    return getattr(import_plugin(plugin), func)()

def usage():
    print ('{} <module_name>.<function>'.format(sys.argv[0]))

def hook_plugins():
    if os.getenv('USE_LOCAL_PLUGINS'):
        return
    import types
    mod = types.ModuleType('plugins')
    mod.__path__ = [PluginImporter.PACKAGE_PATH]
    sys.modules['plugins'] = mod
    sys.path_hooks.append(PluginImporter)

class PluginImporter(importlib.abc.PathEntryFinder,
                     importlib.abc.SourceLoader):
    '''Implements path-based finder and loader protocols.'''
    PACKAGE_PATH = 'plugins://'
    def __init__(self, path):
        if path != PluginImporter.PACKAGE_PATH:
            raise ImportError
        self.base_url = get_config()['plugins']['base_url']
        #print('Spawned PluginImporter')
    def find_spec(self, fullname, target=None):
        #print('findspec({})'.format(fullname))
        return importlib.util.spec_from_loader(fullname, self)
    def get_filename(self, fullname):
        return urllib.parse.urljoin(self.base_url,
                                    fullname.replace('.', '/') + '.py')
    def get_data(self, path):
        print('Reading {}'.format(path))
        return urllib.request.urlopen(path).read()

if __name__ == '__main__':
    sys.exit(main())
