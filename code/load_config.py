# -*- coding: utf-8 -*-
import os
from class_diagram import diagram
#import class_diagram
# loads the config file (in which the config to a diagram is described)
# if the config file is syntactically correct it saves the data in a diagram object and returns that.
# Otherwise it throws an ... exception
def load_config(relative_file_path = "..\config.txt"):
    try:
        config_file = open(relative_file_path, "r", encoding="utf-8")
    except:
        FileNotFoundError
        exit(1)
    di = diagram()
    for line in config_file.readlines():
        line = line.lstrip(' ')
        if line[0] == '#':
            continue
        line_split = line.split(':', 1)
        if line_split[0] == "diagram_name":
            di.name = line_split[1].split('\'', 2)[1]
        elif line_split[0] == "template_path":
            relative_template_path = line_split[1].split('\'', 2)[1]
            di.template_path = os.path.abspath(relative_template_path)
        elif line_split[0] == "hierarchical_codes_template":
            code_array = line_split[1].split('\'', 2)[1].split(',')
            for i in range(len(code_array)):
                code_array[i] = code_array[i].lstrip(' ')
            di.hierarchical_codes = code_array
        elif line_split[0] == 'special_datapoints':
            datapoints_array = line_split[1].split('\'', 2)[1].split(',')
            for i in range(len(datapoints_array)):
                datapoints_array[i] = datapoints_array[i].lstrip(' ')
            di.special_datapoints = datapoints_array
        else:
            print('incorrect config')
            #TODO
            #Throw incorrect config exception




    return di

load_config()