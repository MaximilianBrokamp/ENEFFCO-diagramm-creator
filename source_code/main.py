from source_code import diagram_creator
from source_code import check_all_files
from source_code import additional_functions as af
import os
from datetime import datetime
import traceback


def create_report(driver, diagram, config_file_path, task_complete, duration, number_created_diagrams, number_diagrams_to_create, number_successfully_created_diagrams, number_failed_diagrams, number_ignored, number_Warnings):
    # create the report file, should a file with this exact name already exists, it will add a number to the file name
    report_loccation = os.path.abspath("../reports")
    report_name = "report " + diagram.name + "_" + str(datetime.date(datetime.now())) + ".txt"
    report_path = os.path.join(report_loccation, report_name)
    i = 1
    while os.path.exists(report_path):
        report_name = report_name = "report " + diagram.name + "_" + str(datetime.date(datetime.now())) + "_" + str(i) + ".txt"
        report_path = os.path.join(report_loccation, report_name)
        i += 1
    report = open(report_path, "w")

    beginning = "Report for diagram : " + diagram.name + "\n"
    beginning += "associated Config File: " + config_file_path + "\n"
    beginning += "\n"
    beginning += "Task Complete: " + str(task_complete) + "     " + str(number_created_diagrams) + " out of " + str(number_diagrams_to_create) + "(" + str(round(((number_created_diagrams/number_diagrams_to_create)*100), 2)) + "%) " + "processed    ignored: " + number_ignored + " plants \n"
    beginning += "total time spend: " + str(round(duration, 1)) + "\n"
    beginning += str(number_failed_diagrams) + " FAILED    " + str(number_successfully_created_diagrams) + " Successfully created    " + str(number_Warnings) + " WARNINGS \n\n"
    report.write(beginning)
    i = 1
    line = ""
    for plant in diagram.plants_with_created_diagram:
        print(plant)
        line = str(i) + ".   plant code: " + plant[0] + "    time: " + str(plant[3]) + "    duration:" + str(plant[4]) +"    " + plant[2] + "\n"
        i += 1
        report.write(line)

    report.close()
    af.checkIfWindowIsClosed(driver)


def create_diagram(driver, diagram_type, diagram_name, plant_code, template_path,):
    start_diagram = datetime.now()
    successful = False
    warning = False
    try:
        return_value = diagram_creator.new_diagram(driver, plant_code, diagram_name, template_path, diagram_type)
        print("plant code: ", plant_code)
        print(return_value)
        finished_diagram = datetime.now()
        delta = finished_diagram - start_diagram
        duration_diagram = delta.total_seconds()
        message = ""
        data = []
        if return_value[0] == 0:
            successful = True
            message = return_value[1] + ", " + str(return_value[3]) + " out of " + str(return_value[2]) + " datapoints from the template could be replaced "
            data = [plant_code, return_value[0], message,  datetime.now(), duration_diagram]
        elif return_value[0] == 1:
            successful = True
            warning = True
            message = "diagram created Successfully, !WARNING: " + return_value[1] + "!," + str(return_value[3]) + " out of " + str(return_value[2]) + " datapoints from the template could be replaced"
            data = [plant_code, return_value[0], message, datetime.now(), duration_diagram]
        elif return_value[0] == 2:
            message = "!!!ERROR Could not create diagram!!! : " + return_value[1]
            data = [plant_code, return_value[0], message, datetime.now(), duration_diagram]
        #diagram.add_plant(data)
    except:
        finished_diagram = datetime.now()
        delta = finished_diagram - start_diagram
        duration_diagram = delta.total_seconds()
        tb = traceback.format_exc()
        print(tb)
        #number_failed_diagrams += 1
        message = "!!!ERROR!!! Ecxeption:" + tb.replace("\n", " ")
        data = [plant_code, 3, message, datetime.now(), duration_diagram]
    return data, successful, warning

    #number_created_diagrams = len(diagram.plants_with_created_diagram)
    #task_complete = False
    #if number_created_diagrams == number_diagrams_to_create:
    #    task_complete = True
    #end = datetime.now()

    #duration = round((end - start).total_seconds()/60, 2)
    #create_report(driver, diagram, config_file_path, task_complete, duration, number_created_diagrams,
    #              number_diagrams_to_create, number_successfully_created_diagrams, number_failed_diagrams,
    #              number_ignored, number_Warnings)

