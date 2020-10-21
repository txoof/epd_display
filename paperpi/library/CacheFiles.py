#!/usr/bin/env python3
# coding: utf-8






import logging
from pathlib import Path
import tempfile
import shutil
import requests






class CacheFiles:
    '''file caching object
        Download remote files using requests.get and cache locally
        locally cached files will not be downloaded again'''
    
    def __init__(self, path=None, path_prefix=None):
        self.path_prefix = path_prefix
        self.path = path        
    
    def __repr__(self):
        return f'{type(self._path)}({self.path})'
    
    def __str__(self):
        return str(self.path)

    @property
    def path(self):
        '''path to file cache
            if no path is provided /tmp/ will be used
        
        Args:
            path(None or `str`): None(default) or /full/path/to/file_cache/'''
        if isinstance(self._path, tempfile.TemporaryDirectory):
            return Path(self._path.name)
        elif isinstance(self._path, Path):
            return str(self._path.absolute)
        else:
            return str(self._path)
    
    @path.setter
    def path(self, path):
        if path:
            self._path = Path(path)
        else:
            self._path = tempfile.TemporaryDirectory(prefix=self.path_prefix)
            
    @property
    def path_prefix(self):
        '''prefix to use when setting a cache path in /tmp
            prefixes will always be suffixed with "_" to make more readable
        
        Args:
            prefix(`str`): prefix-to-append; '''
        return self._path_prefix
    
    @path_prefix.setter
    def path_prefix(self, path_prefix):
        if not path_prefix:
            self._path_prefix = ''  
        elif path_prefix.endswith('_'):
            self._path_prefix = path_prefix
        else:
            self._path_prefix = path_prefix+'_'
    
    def cleanup(self):
        '''recursively remove all cached files and cache path'''
        if isinstance(self._path, tempfile.TemporaryDirectory):
            self._path.cleanup()
        
        elif isinstance(self._path, Path):
            shutil.rmtree(self._path)
        else:
            logging.warning(f'no cleanup method for this datatype: {type(self.path)}')
    
    def cache_file(self, url, file_id, force=False):
        '''download a remote file and return the local path to the file
            if a local file with the same name is found, download is skipped and path returned
        
        Args:
            url(`str`): url to remote file
            file_id(`str`): name to use for local file
            force(`bool`): force a download ignoring local files with the same name'''
        file_id = str(file_id)
        local_file = Path(self.path/file_id).absolute()
        
        logging.debug(f'caching file from url {url} to {local_file}')
        
        if local_file.exists() and force is False:
            logging.debug(f'file previously cached')
            return local_file
        
        try:
            r = requests.get(url, stream=True)
        except requests.exceptions.RequestException as e:
            logging.error(f'failed to fetch file at: {url} with error: {e}')
            return None
        
        if r.status_code == 200:
            logging.debug(f'writing file to file{local_file}')
            
            try:
                with open(local_file, 'wb') as file:
                    shutil.copyfileobj(r.raw, file)
            except (OSError, ValueError) as e:
                logging.error(f'failed to write {local_file}: {e}')
                return None
            except (FileExistsError) as e:
                logging.warning(f'file "{local_file}" appears to exist already; no action taken')
                return local_file
        else:
            logging.error(f'failed to fetch file at {url} with response code: {r.status_code}')
            return None
            
        return local_file






def main():
    logging.basicConfig(level=logging.DEBUG)
    cache = CacheFiles(path_prefix='demo_')
    print(f'created a cache directory: {cache}')
    file = cache.cache_file('https://en.wikipedia.org/static/images/project-logos/enwiki-2x.png', 'wiki_logo.png')
    print(f'cached a file: {file}')
    print(f'downloading the same file again...')
    file = cache.cache_file('https://en.wikipedia.org/static/images/project-logos/enwiki-2x.png', 'wiki_logo.png')
    print('cleaning up cache directory now...')
    cache.cleanup()






if __name__ == "__main__":
    main()









