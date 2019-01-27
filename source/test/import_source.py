import sys,os
from pathlib import Path
from os import path

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

def import_source_path():
    test_source_dir =  path.dirname(path.realpath(__file__))
    source_dir = path.dirname(test_source_dir)

    if source_dir not in sys.path:
        sys.path.append(source_dir)

    for file_it in os.listdir(source_dir) :
        full_path_it = source_dir + "/" + file_it
        print(full_path_it)
        if not os.path.isfile(full_path_it) and file_it[-3:] == ".py" and file_it[:-3] != "__init__" :
            pass
            #__import__( module_name + "." + file_it[:-3] )
            #file_names.append(file_it[:-3])

import_source_path()