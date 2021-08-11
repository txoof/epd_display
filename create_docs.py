#!/usr/bin/env python3
# coding: utf-8






# ugly hack to make the imports work properly
# import os
# os.chdir('./paperpi')






from paperpi.library import Plugin, CacheFiles, get_help
from importlib import import_module
from pathlib import Path
import paperpi.my_constants as paperpi_constants
import logging
from IPython.display import Image 
import argparse
import sys






logger = logging.getLogger(__name__)






def setup_plugins(project_root, plugin_list=None, resolution=(640, 400)):
    plugin_path = Path(f'{project_root}/{paperpi_constants.plugins}')
    print('setting up plugins with sample configuration...')
    logging.info(f'using plugin_path: {plugin_path}')
    
    # discover plugins
    plugins = get_help.get_modules(plugin_path)
#     resolution = resolution

    if plugin_list:
        my_list = []
        for i in plugins:
            if i in plugin_list:
                my_list.append(i)
            plugins = my_list
            
    cache = CacheFiles()
    
    plugin_dict = {}
    for plugin in plugins:
        print(f'setting up plugin {plugin}')
        # get sample values
        pkg_name = f'{".".join(plugin_path.parts)}'
        logging.debug(f'importing pkg: {pkg_name}')
        try:
            sample_info = import_module(f'{pkg_name}.{plugin}.sample')
            module = import_module(f'{pkg_name}.{plugin}')
        except ModuleNotFoundError as e:
            logging.warning(f'module "{plugin}" is missing a sample configuration or could not be loaded: {e}')
            continue

        try:
            config = sample_info.config
        except AttributeError as e:
            logging.warning(f'module "{plugin}" does not have a sample configuration: {e}')
            continue
        
        # get the sample layout
        try:
            layout = getattr(module.layout, config['layout'])
        except AttributeError as e:
            logging.warning(f'{plugin} layout file does not contain {config["layout"]}: {e}')
            continue
        except KeyError as e:
            logging.warning(f'{plugin} sample configuration file does not contain a value for "layout": {e}')
            
        
        my_plugin = Plugin(resolution=resolution,
                           cache=cache,
                           layout=layout,
                           update_function=module.update_function,
                           config=config
                          )
        my_plugin.refresh_rate = 1
        # pass any kwargs in from the sample config
        try:
            if 'kwargs' in config:
                my_plugin.update(**config['kwargs'])

            else:
                my_plugin.update()
        except Exception as e:
            logging.warning(f'plugin "{plugin}"could not be configured due to a thrown exception: {e}')
        plugin_dict[plugin] = {'module': module, 'plugin_obj': my_plugin, 'doc_path': plugin_path/plugin}
    return plugin_dict






def create_readme(plugin_dict, project_root, overwrite_images=False):
    '''build README.md for each plugin using information from docstrings and sample images
    
    Args:
        plugin_dict(dict): dictonary provided by setup_plugins
        overwrite_images(bool): overwrite existing sample image when true'''
#     plugin_path = Path(paperpi_constants.plugins)
    plugin_path = Path(f'{project_root}/{paperpi_constants.plugins}')
    readme_name = 'README'
    readme_additional = '_additional'
    suffix = '.md'
    plugin_docs = {}
    
    print('processing README docs for plugins')
    if not overwrite_images:
        print(f'skipping existing image files: overwrite_images = {overwrite_images}')
        
    for plugin, values in plugin_dict.items():
        print(f'\tprocessing plugin: {plugin}')
#         doc_path = Path(plugin_path/plugin)
        doc_path = values['doc_path']
        plugin_readme = Path(doc_path/f'{readme_name}{suffix}')
        additional_readme = Path(doc_path/f'{readme_name}{readme_additional}{suffix}')
        plugin_image = Path(doc_path/f'{plugin}_sample.png')
        
        try:
            my_plugin = values['plugin_obj']
            my_module = values['module']
        except KeyError as e:
            logging.warning(f'plugin "{plugin}" is missing data: {e}')
        
        if additional_readme.exists():
            with open(additional_readme, 'r') as file:
                additional_text = file.read()
        else:
            additional_text = ''
        

        if my_plugin.image:
            if plugin_image.exists() and overwrite_images:
                write_img = True
            elif not plugin_image.exists(): 
                write_img = True
            else:
                write_img = False
                logging.info('image exists, skipping')                

            if write_img:
                try:
                    my_plugin.image.save(plugin_image)
                except Exception as e:
                    logging.warning(f'failed to save plugin image "{plugin_image}" due to error: {e}')


        
        with open(plugin_readme, 'w') as file:
            plugin_name = ".".join(doc_path.parts)
            logging.debug(f'writing help for {plugin_name}')
            file.write(f'# {plugin}\n')
            file.write(f'![sample image for plugin {plugin}](./{plugin_image.name})\n')
            file.write('```\n'+get_help.get_help(plugin, False, plugin_path=plugin_path) + '\n```')
#             file.write('```\n'+get_help.get_help(plugin, False) + '\n```')
            file.write('\n\n')
            file.write(additional_text)
    
        
        plugin_docs[plugin] = {'readme': plugin_readme, 'image': plugin_image}
    return plugin_docs
        
                        






def update_plugin_docs(plugin_docs, doc_path):
    '''update Plugin.md documentation with snips from all plugin READMEs
    
    Args:
        plugin_docs(dict): dictionary provided by create_readme'''
    doc_path = Path(doc_path)
    plugin_readme_source = Path(doc_path/'source/Plugins.md')
    plugin_readme_post_source = Path(doc_path/'source/Plugins_post.md')
    plugin_readme_final = Path(doc_path/plugin_readme_source.name)
    print('updating Plugins.md...')
    print(f'using: {plugin_readme_source}')
    print(f'using postscript file: {plugin_readme_post_source}')
    with open(plugin_readme_source, 'r') as file:
        source = file.read()
        
    with open(plugin_readme_post_source, 'r') as file:
        post = file.read()
    
    with open(plugin_readme_final, 'w') as file:
        file.write(source)
        for plugin, values in plugin_docs.items():
            file.write(f'### [{plugin}]({Path("..")/values["readme"]})\n')
            file.write(f'![{plugin} sample Image]({Path("..")/values["image"]})\n\n')
            
        file.write(post)        






def main():
    parser = argparse.ArgumentParser(description='create_docs')
 
    parser.add_argument('-o', '--overwrite_images', default=False, action='store_true',
                       help='overwrite existing images for plugins when updating README files')
    
    parser.add_argument('-p', '--plugin_list', default=None, nargs='*', 
                       help='list of specific plugins to process')
    
    parser.add_argument('-r', '--project_root', default='./paperpi/', nargs=1,
                       help='path to project root')
    
    parser.add_argument('-d', '--documentation_path', default='./documentation',
                       help='path to documentation directory')
    
    args = parser.parse_args()
#     args = parser.parse_known_args()
    plugin_dict = setup_plugins(args.project_root, args.plugin_list)
    plugin_docs = create_readme(plugin_dict, 
                                project_root=args.project_root,
                                overwrite_images=args.overwrite_images)
    update_plugin_docs(plugin_docs, doc_path=args.documentation_path)
    






if __name__ == "__main__":
    if '-f' in sys.argv:
        logging.debug('looks like this is running in a Jupyter notebook')
        idx = sys.argv.index('-f')
        del sys.argv[idx:idx+2]    
    logger.setLevel('DEBUG')
    logging.root.setLevel('DEBUG')
    print('updating documents...')
    main()











