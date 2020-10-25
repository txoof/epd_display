from . import layout
from . import constants
def my_help(func=None):
    '''Print help for this plugin

    Args:
        func(`string`): name of function '''
    import types
    print(f'Plugin: {constants.name}: {constants.version}')
    if not func:
        l = [f for f in globals().values() if type(f) == types.FunctionType]
        print('*'*50)
        print('Available functions in this plugin:')
        for i in l:
            print(f'##### {i.__name__} #####')
            print(f'{i.__doc__}\n\n')

        print('*'*50)
        print('Available Layouts:')
        for name in vars(layout).keys():
            if not name.startswith('__') and not name in ('os', 'dir_path'):
                print(f'  {name}')

        print('*'*50)
        print('data dictionary keys available for layouts:')
        for k in constants.data:
            print(f'   {k}')

    else:
        print(f'{func.__doc__}')
