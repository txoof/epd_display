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






def run(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        line = process.stdout.readline().rstrip()
        if not line:
            break
        yield line






def main():
    exit_status = 0
    pre_import_modules = set(sys.modules)
    pyinstaller_command = build_pyinstaller_command()
    
#     process = subprocess.Popen(pyinstaller_command, stdout=subprocess.PIPE)
#     while True:
#         output = process.stdout.readline()
#         if output == '' and process.poll() is not None:
#             break
#         if output:
#             print(output.strip())
    
#     rc = process.poll()
    
#     if rc > 0:
#         print('pyinstaller exited with errors!')
#         print('try running the build command manually from within a pipenv shell: ')
#         print(" ".join(pyinstaller_command))
#         print('pyinstaller exited with errors!')
#     else:
#         print('executable is stored in ./dist')
        
#     return rc
    
    timeout = 500
#     print(pyinstaller_command)
    proc = subprocess.Popen(pyinstaller_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f'starting build -- will timeout after {timeout} seconds')
    try:
        outs, errs = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        print('timeout exceeded! build failed!')
        print(f'try running this command manually from within the pipenv shell:')
        print(f'{" ".join(pyinstaller_command)}')
        print('timeout exceeded! build failed!')
        outs, errs = proc.communicate()
        exit_status = 1
    print(outs)
    print(errs)    
    if exit_status == 0:
        print(f'executable created in ./dist/')
    return exit_status






if __name__ == '__main__':
    exit_status = 0
    build = True
    for i in sys.argv:
        if 'ipykernel' in i:
            print('this should **NOT** be run from within jupyter notebook')
            print('modules imported by jupyter can interfere with module discovery.')
            build = False
            exit_status = 1
    if build:
        exit_status = main()
    exit(exit_status)








exit(0)









