# -*- coding: utf-8 -*-
import os
from code import class_diagram
from code.class_diagram import diagram

# loads the config file (in which the config to a diagram is described)
# if the config file is syntactically correct it saves the data in a diagram object and returns that.


def load_config(file_name):
    try:
        config_file = open(os.path.abspath("./configs/" + file_name), "r", encoding="utf-8")
    except FileNotFoundError:
        exit(1)
    di = class_diagram.diagram()
    di.config_file_name = file_name
    for line in config_file.readlines():

        line = line.lstrip(' ')
        #print(line)
        if line[0] == '#' or line[0] == '\n':
            continue
        line_split = line.split(':', 1)
        if line_split[0] == "diagram_name":
            diagram_name = line_split[1].split('\'', 2)[1]
            di.set_diagram_name(diagram_name)
        elif line_split[0] == "template_file":
            template_file = line_split[1].split('\'', 2)[1]
            relative_template_path = "./templates/" + template_file
            template_path = os.path.abspath(relative_template_path)
            if os.path.isfile(template_path):
                if template_path.endswith("EnEffCoDashBoard"):
                    di.diagram_type = "dashboard"
                elif template_path.endswith("EnEffCoChart"):
                    di.diagram_type = "chart"
                else:
                    return None
                di.template_path = template_path
                di.template_file = template_file.split(".")[0]
        elif line_split[0] == "hierarchical_codes_template":
            code_array = line_split[1].split('\'', 2)[1].split(',')
            for i in range(len(code_array)):
                code_array[i] = code_array[i].lstrip(' ')
                print(code_array[i])
                di.hierarchical_codes.append(code_array[i])
        elif line_split[0] == 'ignore':
            ignore_list = line_split[1].split('\'', 2)[1].split(',')
            for i in range(len(ignore_list)):
                ignore_list[i] = ignore_list[i].lstrip(' ')
            di.set_ignore(ignore_list)
        elif line_split[0] == 'select':
            select_list = line_split[1].split('\'', 2)[1].split(',')
            for i in range(len(ignore_list)):
                select_list[i] = ignore_list[i].lstrip(' ')
            di.set_select(ignore_list)
        elif line_split[0] == 'report_name':
            report_name = line_split[1].split('\'', 2)[1]
            di.set_report_name(report_name)

        else:
            print("incorrect config")
            return None
    return di
