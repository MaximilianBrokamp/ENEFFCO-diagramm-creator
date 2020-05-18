# -*- coding: utf-8 -*-
import os
import class_diagram
#import class_diagram
# loads the config file (in which the config to a diagram is described)
# if the config file is syntactically correct it saves the data in a diagram object and returns that.
# Otherwise it throws an ... exception
from class_diagram import diagram


def load_config(relative_file_path = "..\configs\config.txt"):
    valid_diagram_types = ["dashboard", "chart"]
    try:
        config_file = open(relative_file_path, "r", encoding="utf-8")
    except FileNotFoundError:
        exit(1)
    di = class_diagram.diagram()
    for line in config_file.readlines():

        line = line.lstrip(' ')
        #print(line)
        if line[0] == '#' or line[0] == '\n':
            continue
        line_split = line.split(':', 1)
        if line_split[0] == "diagram_name":
            name = line_split[1].split('\'', 2)[1]
            di.set_name(name)
        elif line_split[0] == "template_path":
            relative_template_path = "../" + line_split[1].split('\'', 2)[1]
            di.template_path = os.path.abspath(relative_template_path)
        elif line_split[0] == "diagram_type":
            type = line_split[1].split('\'', 2)[1]
            if type in valid_diagram_types:
                di.set_type(type)
            else:
                print("incorrect config")
                #TODO
                # Throw incorrect config exception
        elif line_split[0] == "hierarchical_codes_template":
            code_array = line_split[1].split('\'', 2)[1].split(',')
            for i in range(len(code_array)):
                code_array[i] = code_array[i].lstrip(' ')
                print(code_array[i])
                di.hierarchical_codes.append(code_array[i])
        elif line_split[0] == 'special_datapoints':
            datapoints_array = line_split[1].split('\'', 2)[1].split(',')
            for i in range(len(datapoints_array)):
                datapoints_array[i] = datapoints_array[i].lstrip(' ')
            di.special_datapoints = datapoints_array
        elif line_split[0] == 'ignore':
            ignore_list = line_split[1].split('\'', 2)[1].split(',')
            for i in range(len(ignore_list)):
                ignore_list[i] = ignore_list[i].lstrip(' ')
            di.set_ignore(ignore_list)
        else:
            print("incorrect config")
            #print(line)
            #TODO
            #Throw incorrect config exception
    return di
