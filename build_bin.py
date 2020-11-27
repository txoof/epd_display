#!/usr/bin/env python3
# coding: utf-8








import sys
from pathlib import Path
import os
import importlib
import subprocess
import pyinstaller_cfg






def hidden_imports(search_path):
    '''find the imports from the plugins
    
    pyinstaller cannot find the imports from the plugins because they are only
    loaded on demand at boot
    
    Args:
        search_path(str): path to plugin modules to search'''
    pre_import_modules = set(sys.modules)
    search_path = Path(search_path)

    # find all modules in search_path that do not start with . or _
    for i in search_path.glob('*'):
        if not i.name[0] in ['.', '_']:
            module = importlib.import_module(f"{'.'.join(search_path.parts)}.{i.name}")

    post_import_modules = set(sys.modules)

    imported_modules = post_import_modules - pre_import_modules
    
    unique_modules = set()
    
    for m in imported_modules:
        unique_modules.add(m.split('.')[0])
        
    
    return unique_modules






def build_pyinstaller_command():
    '''build a command list for Popen'''
    # calculate hidden imports
    my_hidden = hidden_imports(pyinstaller_cfg.plugin_path)
    
    cmd_list = ['pipenv', 'run', 'pyinstaller']

    for o in pyinstaller_cfg.options:
        if len(o) > 0:
            cmd_list.append(o)

    # calculated hidden imports
    for h in my_hidden:
        if len(h) > 0:
            cmd_list.extend(['--hidden-import', h])
    
    # explicit hidden imports from configuration file
    for h in pyinstaller_cfg.hidden_imports:
        cmd_list.extend(['--hidden-import', h])
    
    for d in pyinstaller_cfg.datas:
        if len(d) > 0:
            cmd_list.extend(['--add-data', f'{pyinstaller_cfg.base_path}/{d[0]}:{d[1]}'])

    for e in pyinstaller_cfg.exclude:
        if len(e) > 0:
            cmd_list.extend(['--exclude-module', e])

    cmd_list.append(f'{pyinstaller_cfg.base_path}/{pyinstaller_cfg.base_script}')

    return cmd_list






def main():
    pre_import_modules = set(sys.modules)
    pyinstaller_command = build_pyinstaller_command()
#     print(pyinstaller_command)
    proc = subprocess.Popen(pyinstaller_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        outs, errs = proc.communicate(timeout=120)
    except TimeoutExpired:
        proc.kill()
        outs, errs = proc.communicate()

    print(outs)
    print(errs)    






if __name__ == '__main__':
    build = True
    for i in sys.argv:
        if 'ipykernel' in i:
            print('this should **NOT** be run from within jupyter notebook')
            print('modules imported by jupyter can interfere with module discovery.')
            build = False
    if build:
        main()











