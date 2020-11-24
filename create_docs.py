#!/usr/bin/env python3
# coding: utf-8






from library import Plugin, CacheFiles
from library import get_help
from importlib import import_module
from pathlib import Path
import constants
import logging
from IPython.display import Image 
import argparse






logger = logging.getLogger(__name__)






def setup_plugins():
    print('setting up plugins with sample configuration...')
    # discover plugins
    plugins = get_help.get_modules()
    # create a cache object for those plugins that need it
    cache = CacheFiles()
    plugin_path = Path(constants.plugins)
    resolution = constants.sample_resolution
    plugin_dict = {}
    for plugin in plugins:
        print(f'setting up plugin: {plugin}')
        # get sample values
        try:
            sample_info = import_module(f'{plugin_path}.{plugin}.sample')
            module = import_module(f'{plugin_path}.{plugin}')
        except ModuleNotFoundError as e:
            logging.warning(f'module "{plugin}" is missing a sample configuration or could not be loaded: {e}')
            continue
        
        # get the sample configuration
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
        plugin_dict[plugin] = {'module': module, 'plugin_obj': my_plugin}
    return plugin_dict
    






def create_readme(plugin_dict, overwrite_images=False):
    plugin_path = Path(constants.plugins)
    readme_name = 'README'
    readme_additional = '_additional'
    suffix = '.md'
    plugin_docs = {}
    
    print('processing README docs for plugins')
    if not overwrite_images:
        print(f'skipping existing image files: overwrite_images = {overwrite_images}')
        
    for plugin, values in plugin_dict.items():
        print(f'\tprocessing plugin: {plugin}')
        doc_path = Path(plugin_path/plugin)
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
            file.write(f'# {plugin}\n')
            file.write(f'![sample image for plugin {plugin}](./{plugin_image.name})\n')
            file.write('```\n'+get_help.get_help(plugin, False) + '\n```')
            file.write('\n\n')
            file.write(additional_text)
    
        
        plugin_docs[plugin] = {'readme': plugin_readme, 'image': plugin_image}
    return plugin_docs
        
                        






def update_plugin_docs(plugin_docs):
    doc_path = Path(constants.doc_path)
    plugin_readme_source = Path(doc_path/'source/Plugins.md')
    plugin_readme_final = Path(doc_path/plugin_readme_source.name)
    
    with open(plugin_readme_source, 'r') as file:
        source = file.read()
    
    with open(plugin_readme_final, 'w') as file:
        file.write(source)
        for plugin, values in plugin_docs.items():
            file.write(f'### [{plugin}]({Path("../paperpi")/values["readme"]})\n')
            file.write(f'![{plugin} sample Image]({Path("../paperpi")/values["image"]})\n\n')
        






def main():
    parser = argparse.ArgumentParser(description='create_docs')
    parser.add_argument('-o', '--overwrite_images', default=False, action='store_true',
                       help='overwrite existing images for plugins when updating README files')
    
    args = parser.parse_args()
#     args = parser.parse_known_args()
    plugin_dict = setup_plugins()
    plugin_docs = create_readme(plugin_dict, overwrite_images = args.overwrite_images)
    update_plugin_docs(plugin_docs)
    













if __name__ == "__main__":
    logger.setLevel('DEBUG')
    print('updating documents...')
    main()








# doc_path = Path('../documentation')
# plugin_readme_source = Path(doc_path/'source/Plugins.md')
# plugin_readme_final = Path(doc_path/plugin_readme_source.name)

# with open(plugin_readme_source, 'r') as file:
#     source = file.read()

# with open(plugin_readme_final, 'w') as file:
#     file.write(source)
#     for doc, value, in plugin_docs.items():
#         file.write(f'### [{doc}]({Path("../paperpi")/value["readme"]})\n')
#         file.write(f'![{plugin} sample image]({Path("../paperpi")/value["image"]})\n\n')






# # discover plugins
# plugins = get_help.get_modules()

# # set up basic configuration
# cache = CacheFiles()
# refresh_rate = 1
# plugin_path = Path('./plugins')
# resolution = (640,448)
# plugin_readme_name = f'README.md'
# plugin_readme_additional_name = f'{plugin_readme_name.split(".")[0]}_additional.md'
# plugin_docs = {}


# # loop through all the discovered plugins
# for plugin in plugins:
#     config = None
#     module = None
#     doc_path = Path(plugin_path/f'{plugin}/')
#     plugin_sample_img = None
#     try:
#         sample = import_module(f'{constants.plugins}.{plugin}.sample')
#         module = import_module(f'{constants.plugins}.{plugin}')
#     except ModuleNotFoundError:
#         logging.warning(f'module "{plugin}" is missing a sample configuration; cannot process')
#         continue
        
#     # pull configuration from sample.py
#     config = sample.config
#     if config and module:
#         # pull the appropriate layout from the layouts file
#         layout = getattr(module.layout, config['layout'])
#         # build a plugin using the sample configuration
#         my_plugin = Plugin(resolution=resolution, 
#                            cache=cache, layout=layout,
#                            update_function=module.update_function, config=config)
#         # set refresh rate
#         my_plugin.refresh_rate = refresh_rate
#         # pass any kwargs needed to configure this plugin
#         if 'kwargs' in config:
#             my_plugin.update(**config['kwargs'])
#         else:
#             my_plugin.update()
    
#     # write out readme and save image
#     plugin_readme = Path(doc_path/plugin_readme_name)
#     plugin_readme_additional = Path(doc_path/plugin_readme_additional_name)
    
#     if plugin_readme_additional.exists():
#         with open(plugin_readme, 'r') as file:
#             additional_text = file.read()
#     else:
#         additional_text = ''
            
#     if my_plugin.image:
#         plugin_sample_img = Path(doc_path/f'{plugin}_sample.png')
#         my_plugin.image.save(plugin_sample_img)
#     with open(plugin_readme, 'w') as file:
#         file.write(f'# {plugin}\n')
#         file.write(f'![sample image for plugin {plugin}]({plugin_sample_img.name})\n')
#         file.write('```\n' + get_help.get_help(plugin, False) + '\n```')
#         file.write('\n\n')
#         file.write(additional_text)
        
#     plugin_docs[plugin] = {'readme': plugin_readme, 'image': plugin_sample_img}


