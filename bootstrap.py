#!/usr/bin/python3

import sys, os
import importlib.abc, importlib.util

def main():
    if len(sys.argv) != 2:
        usage()
        return 1
    conf = get_config()
    print(conf['plugins'])
    plugin, func = sys.argv[1].split('.', 1)
    print('Running {}.{}'.format(plugin, func))
    hook_plugins()
    return getattr(import_plugin(plugin), func)()

def get_config():
    from boto.pyami.config import Config
    return Config()

def import_plugin(plugin_name):
    return importlib.import_module('plugins.' + plugin_name)

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
        #print('Spawned PluginImporter')
    def find_spec(self, fullname, target=None):
        #print('findspec({})'.format(fullname))
        return importlib.util.spec_from_loader(fullname, self)
    def get_filename(self, fullname):
        return fullname
    def get_data(self, path):
        return ('#print("Importing module from {0}")\n'
                'def test_msg():\n'
                '  print("You invoked test of {0}")\n'.format(path))

if __name__ == '__main__':
    sys.exit(main())
