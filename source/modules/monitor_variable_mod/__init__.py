import sys,os
from pathlib import Path


'''
in this directory
each module should be a independent plugin
'''

def import_module_path():
    source_dir =  os.path.dirname(os.path.realpath(__file__))

    if source_dir not in sys.path:
        sys.path.append(source_dir)

    module_name = Path(source_dir).name
    file_names = []
    for file_it in os.listdir(source_dir) :
        full_path_it = source_dir + "/" + file_it
        if os.path.isfile(full_path_it) and file_it[-3:] == ".py" and file_it[:-3] != "__init__" :
            __import__( module_name + "." + file_it[:-3] )
            file_names.append(file_it[:-3])


    return file_names

__all__ = import_module_path()