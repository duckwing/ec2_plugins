#!/usr/bin/python3

import sys

def usage():
    print ('{} <module_name>.<function>'.format(sys.argv[0]))

def import_plugin(plugin_name):
    import importlib
    return importlib.import_module('plugins.' + plugin_name)

def main():
    if len(sys.argv) != 2:
        usage()
        return 1
    plugin, func = sys.argv[1].split('.', 1)
    print('Running {}.{}'.format(plugin, func))
    plugin = import_plugin(plugin)
    return getattr(plugin, func)()

if __name__ == '__main__':
    sys.exit(main())

