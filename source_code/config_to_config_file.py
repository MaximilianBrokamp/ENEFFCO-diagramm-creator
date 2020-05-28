from source_code import class_diagram
import os

def config_to_config_file(config, config_file_name):
    config_location = os.path.abspath("./configs")
    path = os.path.join(config_location, config_file_name + ".txt")
    #i = 1
    #while os.path.exists(path):
    #    file_name = config_file_name + str(i) + " .txt"
    #    path = os.path.join(config_location, file_name)
    #    i += 1
    config_file = open(path, "w", encoding="utf-8")

    line = "diagram_name: '" + config.diagram_name + "'" + "\n"
    config_file.write(line)
    line = "report_name: '" + config.report_name + "'" + "\n"
    config_file.write(line)
    line = "template_file: '" + config.template_file + "'" + "\n"
    config_file.write(line)
    line = "#template_path: '" + config.template_path + "'" + "\n"
    config_file.write(line)

    line = "select: '"
    i = 1
    if len(config.select_list) > 0:
        line += config.select_list[0]
        while i < len(config.select_list):
            line += ", " + config.select_list[i]
            i += 1
        line += "'\n"
        config_file.write(line)

    line = "ignore: '"
    i = 1
    if len(config.ignore_list) > 0:
        line += config.ignore_list[0]
        while i < len(config.ignore_list):
            line += ", " + config.ignore_list[i]
            i += 1
        line += "'\n"
        config_file.write(line)