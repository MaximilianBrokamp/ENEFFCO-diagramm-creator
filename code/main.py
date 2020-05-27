import diagram_creator
import check_all_files
import additional_functions as af
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

def main():
    #checks if all necessary files and directories exist
    check_all_files_return = check_all_files.check_all_files()
    if not check_all_files_return[0]:
        print("Missing files or directories", check_all_files_return[1] )
        #TODO
        # show message in ui

    start = datetime.now()
    config_file_path = "..\configs\config.txt"
    diagram = load_config.load_config(config_file_path)
    driver = diagram_creator.init_driver("https://ewus.eneffco.de/ChartPage.aspx")
    diagram_creator.login(driver)
    #for testing
    #return_value = new_diagram(driver, "STO.001", diagram.name, diagram.template_path, diagram.hierarchical_codes, diagram.diagram_type)
    #print(return_value)
    #af.checkIfWindowIsClosed(driver)

    print("ignore List: ", diagram.ignore_list)

    # get a list of all plants
    for i in range(2):
        try:
            all_plants = diagram_creator.get_all_plants(driver, True)
            break
        except:
            if i == 1:
                #TODO
                # signal what went wrong
                print("could not get list of all plants")
                af.go_to_ChartPage(driver)
                return

    # get a list with all plants that already have the specified diagram
    for i in range(2):
        try:
            plant_with_diagrams = diagram_creator.get_plants_with_exiting_diagram(driver, diagram.name)
            break
        except:
            if i == 1:
                #TODO
                # signal what went wrong
                print("could not get plans with existing diagram")
                return
    # create a list of plants that need the specified diagram
    plants_without_diagram = []
    print(all_plants)
    print(plant_with_diagrams)
    number_ignored = 0
    for plant in all_plants:
        ignore = False
        if plant not in plant_with_diagrams:
            for element in diagram.ignore_list:
                if plant.find(element) != -1:
                    ignore = True
                    number_ignored += 1
                    print("ignore True: ", plant)
                    break
            if not ignore:
                plants_without_diagram.append(plant)

    number_diagrams_to_create = len(plants_without_diagram)
    number_successfully_created_diagrams = 0
    number_failed_diagrams = 0
    number_Warnings = 0

    print("all plants len: " + str(len(all_plants)))
    print("plants with diagram len: " + str(len(plant_with_diagrams)))
    print("plants without diagram len: " + str(len(plants_without_diagram)))
    for plant in plants_without_diagram:
        #exit loop after three runs for test purposes
        if plant == plants_without_diagram[3]:
            break

        start_diagram = datetime.now()
        try:
            return_value = diagram_creator.new_diagram(driver, plant, diagram.name, diagram.template_path, diagram.hierarchical_codes, diagram.diagram_type)
            print("plant code: ", plant)
            print(return_value)
            finished_diagram = datetime.now()
            delta = finished_diagram - start_diagram
            duration_diagram = delta.total_seconds()
            message = ""
            data = []
            if return_value[0] == 0:
                number_successfully_created_diagrams +=1
                message = return_value[1] + ", " + str(return_value[3]) + " out of " + str(return_value[2]) + " datapoints from the template could be replaced "
                data = [plant, return_value[0], message,  datetime.now(), duration_diagram]
            elif return_value[0] == 1:
                number_successfully_created_diagrams += 1
                number_Warnings += 1
                message = "diagram created Successfully, !WARNING: " + return_value[1] + "!," + str(return_value[3]) + " out of " + str(return_value[2]) + " datapoints from the template could be replaced"
                data = [plant, return_value[0], message, datetime.now(), duration_diagram]
            elif return_value[0] == 2:
                number_failed_diagrams += 1
                message = "!!!ERROR Could not create diagram!!! : " + return_value[1]
                data = [plant, return_value[0], message, datetime.now(), duration_diagram]
            diagram.add_plant(data)
        except:
            finished_diagram = datetime.now()
            delta = finished_diagram - start_diagram
            duration_diagram = delta.total_seconds()
            tb = traceback.format_exc()
            print(tb)
            number_failed_diagrams += 1
            message = "!!!ERROR!!! Ecxeption:" + tb.replace("\n", " ")
            data = [plant, 3, message, datetime.now(), duration_diagram]
            diagram.add_plant(data)

    number_created_diagrams = len(diagram.plants_with_created_diagram)
    task_complete = False
    if number_created_diagrams == number_diagrams_to_create:
        task_complete = True
    end = datetime.now()

    duration = round((end - start).total_seconds()/60, 2)
    create_report(driver, diagram, config_file_path, task_complete, duration, number_created_diagrams,
                  number_diagrams_to_create, number_successfully_created_diagrams, number_failed_diagrams,
                  number_ignored, number_Warnings)


if __name__ == "__main__":
    main()