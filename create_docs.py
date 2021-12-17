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
import re






logger = logging.getLogger(__name__)






def setup_plugins(project_root, plugin_list=None, resolution=(640, 400), skip_layouts=False):
    '''create dictionary of plugins using sample configurations provided in each plugin directory
    
    Args:
        project_root(`str`): directory where main script is located
        use_all_layouts(`Bool`): use all discovered layouts
        plugin_list(`list`): list of plugins to update; when None all discovered plugins will be updated
        resolution(`tuple` of `int`): screen resolution to use when generating images
        load_layouts(`bool`): when True, create a full Plugin object with a layout and an image
        
    Returns:
        `dict` of Plugin objects and layout name used to generate the Plugin
        '''
            
    plugin_path = Path(f'{project_root}/{paperpi_constants.plugins}')
    
    # discover all plugins
    plugins = get_help.get_modules(plugin_path)
    
    # reduce the list down to just the specified plugins
    if plugin_list:
        my_list = []
        for i in plugins:
            if i in plugin_list:
                my_list.append(i)
            else:
                print(f'specified plugin not found: {i}')
        plugins = my_list
    
    cache = CacheFiles()
    
    plugin_dict = {}
    
    for plugin in plugins:
        plugin_dict[plugin] = []
        all_layouts = {}
        print(f'found up plugin {plugin}')
        
        pkg_name = f'{".".join(plugin_path.parts)}'
        logging.debug(f'importing pkg: {pkg_name}')
        
        # import the plugin, layout and sample configuration
        try:
            module = import_module(f'{pkg_name}.{plugin}')            
            layout_import =  import_module(f'{pkg_name}.{plugin}.layout')
            sample_import = import_module(f'{pkg_name}.{plugin}.sample')
        except ModuleNotFoundError as e:
            print(f'skipping plugin {plugin} due to previous error: {e}')
            continue
        
        # get all of the layout dictionarys from the layout file
        for a in dir(layout_import):
            if not a.startswith('_') and isinstance(getattr(layout_import, a), dict):
                all_layouts[a] = (getattr(layout_import, a))
                
        if len(all_layouts) < 1:
            print(f'skipping plugin {plugin} due to missing layouts')
            continue
            
        # remove the default layout from the list if there are multiple layouts defined
#         if len(all_layouts) > 1 and 'layout' in all_layouts:
#             all_layouts.pop('layout')
        
        # make sure there is a valid configuration:
        try:
            config = sample_import.config
        except AttributeError as e:
            print(f'skipping plugin {plugin} due to missing sample configuration: {e}')
            continue
        
        # setup plugin
        if skip_layouts:
            print('skipping creating full layouts and creating images due to command line switch (-s)')
        for name, layout in all_layouts.items():
            print(f'adding layout: {name}')
            if not skip_layouts:
                my_plugin = Plugin(resolution=resolution,
                                   cache=cache,
                                   layout=layout,
                                   update_function=module.update_function,
                                   config=config
                                  )
                my_plugin.refresh_rate = 1

                try:
                    if 'kwargs' in config:
                        my_plugin.update(**config['kwargs'])

                    else:
                        my_plugin.update()
                except Exception as e:
                    print(f'plugin "{plugin}" could not be configured due to errors: {e}')
            else:
                my_plugin = None
            plugin_dict[plugin].append({
                                   'plugin': plugin,
                                   'module': module, 
                                   'plugin_obj': my_plugin, 
                                   'doc_path': plugin_path/plugin,
                                   'layout': name})
    return plugin_dict






def update_ini_file(plugin_dict):
    '''append sample configurations for each module to the default paperpi.ini file
    distributed at install'''
    
    base_ini_file = './install/paperpi_base.ini'
    output_ini_file = './paperpi/config/paperpi.ini'
    
    config_sections = []
    
    print(f'updating {output_ini_file} using sample configs from plugins')
    
    for plugin, data in plugin_dict.items():
        try:
            sample_config = data[0]['module'].constants.sample_config
        except (IndexError, AttributeError):
            logging.info(f'no valid data for plugin {plugin}')
            continue
            
        # check that it matches the format
        match = re.match('^\s{0,}\[Plugin', sample_config)
        try:
            if match.string:
                sample_config = re.sub('^\s{0,}\[Plugin', '[xPlugin', sample_config)
            else:
                print(f'plugin {plugin} does not have a standard sample_config string. Please check formatting.')
                continue
        except AttributeError:
            print(f'plugin {plugin} has no valid sample_config string: {sample_config}')
            continue
        
        config_sections.append(sample_config)
        config_sections.append('\n')
    
    output_ini_list = []
    with open(base_ini_file, 'r') as base_f:
        for i in base_f:
            output_ini_list.append(i)
    
    output_ini_list.extend(config_sections)
    
    with open(output_ini_file, 'w') as out_f:
        for i in output_ini_list:
            out_f.write(i)






def create_readme(plugin_dict, project_root, overwrite_images=False):
    plugin_docs = {}
    plugin_path = Path(f'{project_root}/{paperpi_constants.plugins}')
    readme_name = 'README'
    readme_additional = '_additional'
    readme_suffix = '.md'
    
    # run through each plugin and gather the document information
    for plugin, layouts in plugin_dict.items():
        print(f'Processing plugins: {plugin}')
        try:
            doc_path = Path(layouts[0]['doc_path'])
            plugin_readme = Path(doc_path)/f'{readme_name}{readme_suffix}'
            plugin_additional_readme = Path(doc_path)/f'{readme_name}{readme_additional}{readme_suffix}'
        except IndexError:
            print(f'   skipping {plugin} due to incomplete documentation')
            continue
        
        # pull the help information for the plugin
        readme_text = get_help.get_help(plugin, False, plugin_path=plugin_path)
        
        # read the additional documentation
        if plugin_additional_readme.exists():
            with open(plugin_additional_readme, 'r') as file:
                additional_text = file.read()
        else:
            additional_text = '' 
        
        default_layout_image = {'filename': 'not found',
                                'path': 'none',
                                'layout_name': 'layout'}
        layout_images = []
        # gather all the images associated with the plugin
        for layout in layouts:
            layout_name = layout['layout']
            image_filename = f'{plugin}.{layout["layout"]}-sample.png'
            image_path = Path(doc_path)/image_filename
                        
            print(f'   processing layout: {layout_name}')
            try:
                image = layout['plugin_obj'].image
            except AttributeError:
                print('  no image available, skipping this layout')
                continue
                
            if (image_path.exists() and overwrite_images) or not image_path.exists():
                print(f'   saving image: {image_path}')
                image.save(image_path)
            else:
                print(f'   image exists, skipping save')
                
            
            
            layout_entry = {'filename': image_filename,
                            'path': image_path,
                            'layout_name': layout_name}
            
            # try to locate the default "layout" to show at the top of the documentation
            if layout_name == 'layout':
                default_layout_image.update(layout_entry)
            
            layout_images.append(layout_entry)

        print('   writing README files')
        with open(plugin_readme, 'w') as file:
            plugin_name = ".".join(doc_path.parts)
            file.write(f'# {plugin}\n')
            file.write(f'![sample image for plugin {plugin_name}](./{default_layout_image["filename"]}) \n\n')
            file.write(f'```\n{readme_text}\n```\n\n')
            file.write(f'## Provided Layouts:\n\n')
            for l in layout_images:
                file.write(f'layout: **{l["layout_name"]}**\n\n')  
                file.write(f'![sample image for plugin {l["layout_name"]}](./{l["filename"]}) \n\n\n')

            file.write(additional_text)
        
        plugin_docs[plugin] = {'readme': plugin_readme, 'image': default_layout_image["path"]}
            
    
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
    
# this breaks README creation
#     parser.add_argument('-s', '--skip_layouts', default=False, action='store_true',
#                         help='skip loading layouts and do not create images')
    
    
    args = parser.parse_args()
    
#     args = parser.parse_known_args()
    plugin_dict = setup_plugins(args.project_root, args.plugin_list)
    plugin_docs = create_readme(plugin_dict, 
                                project_root=args.project_root,
                                overwrite_images=args.overwrite_images,
                                )
    update_ini_file(plugin_dict)
    update_plugin_docs(plugin_docs, doc_path=args.documentation_path)
    
    






if __name__ == "__main__":
    if '-f' in sys.argv:
        logging.debug('looks like this is running in a Jupyter notebook')
        idx = sys.argv.index('-f')
        del sys.argv[idx:idx+2]    
    logger.setLevel('DEBUG')
    logging.root.setLevel('DEBUG')
    print('updating documents...')
    r = main()











