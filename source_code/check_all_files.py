import os

def check_all_files():
    everything_existing = True
    missing = []


    current_directory = os.path.curdir
    program_root_directory = current_directory
    # program_root_directory = os.path.abspath(os.path.join(current_directory, "../"))
    # cuts chars form the path until the ends in the root directory of the Program
    # !!! directory has to be named "ENEFFCO diagram creator" !!!
    # while True:
    #     if len(program_root_directory) == 0:
    #         return False, [{"Fatal": "root directroy not found"}]
    #     if program_root_directory.endswith("diagramm-creator"):
    #         break
    #     else:
    #         program_root_directory = program_root_directory[:len(program_root_directory)-1]
    path_to_check = program_root_directory
    #check program root directory
    if not os.path.exists(path_to_check + "/source_code"): everything_existing = False; missing.append({"type": "directory", "name": "source_code", "path": path_to_check})
    if not os.path.exists(path_to_check + "/configs"): everything_existing = False; missing.append({"type": "directory", "name": "configs", "path": path_to_check})
    if not os.path.exists(path_to_check + "/reports"): everything_existing = False; missing.append({"type": "directory", "name": "reports", "path": path_to_check})
    if not os.path.exists(path_to_check + "/templates"): everything_existing = False; missing.append({"type": "directory", "name": "templates", "path": path_to_check})
    if not os.path.exists(path_to_check + "/webdrivers"): everything_existing = False; missing.append({"type": "directory", "name": "webdrivers", "path": path_to_check})
    if not os.path.exists(path_to_check + "/source_code/ui"): everything_existing = False; missing.append({"type": "directory", "name": "ui", "path": path_to_check})
    if not os.path.exists(path_to_check + "/source_code/ui/additional_ressources"): everything_existing = False; missing.append({"type": "directory", "name": "additional_ressources", "path": path_to_check})

    #checking files in Directory: source_source_code
    path_to_check = os.path.join(program_root_directory, "source_code")
    if not os.path.exists(path_to_check + "/__init__.py"): everything_existing = False; missing.append({"type": "file", "name": "__init__.py", "path": path_to_check})
    if not os.path.exists(path_to_check + "/additional_functions.py"): everything_existing = False; missing.append({"type": "file", "name": "additional_functions.py", "path": path_to_check})
    if not os.path.exists(path_to_check + "/check_all_files.py"): everything_existing = False; missing.append({"type": "file", "name": "check_all_files.py", "path": path_to_check})
    if not os.path.exists(path_to_check + "/class_diagram.py"): everything_existing = False; missing.append({"type": "file", "name": "class_diagram.py", "path": path_to_check})
    if not os.path.exists(path_to_check + "/diagram_creator.py"): everything_existing = False; missing.append({"type": "file", "name": "diagram_creator.py", "path": path_to_check})
    if not os.path.exists(path_to_check + "/load_config.py"): everything_existing = False;  missing.append({"type": "file", "name": "load_config.py", "path": path_to_check})
    if not os.path.exists(path_to_check + "/extract_plants.py"): everything_existing = False;  missing.append({"type": "file", "name": "extract_plants.py", "path": path_to_check})
    if not os.path.exists(path_to_check + "/qt_thread_task.py"): everything_existing = False;  missing.append({"type": "file", "name": "qt_thread_task.py", "path": path_to_check})
    if not os.path.exists(path_to_check + "/config_to_config_file.py"): everything_existing = False;  missing.append({"type": "file", "name": "config_to_config_file.py", "path": path_to_check})

    #checking sub direcotrys of source_code
    path_to_check = os.path.join(program_root_directory, "source_code/ui")
    if not os.path.exists(path_to_check + "/__init__.py"): everything_existing = False; missing.append({"type": "file", "name": "__init__.py", "path": path_to_check})
    if not os.path.exists(path_to_check + "/icons_rc.py"): everything_existing = False; missing.append({"type": "file", "name": "icons_rc.py", "path": path_to_check})
    if not os.path.exists(path_to_check + "/edit_config_file.py"): everything_existing = False; missing.append({"type": "file", "name": "edit_config_file.py", "path": path_to_check})
    if not os.path.exists(path_to_check + "/edit_config_file.ui"): everything_existing = False; missing.append({"type": "file", "name": "edit_config_file.ui", "path": path_to_check})
    #if not os.path.exists(path_to_check + "/error_missing_data.py"): everything_existing = False; missing.append({"type": "file", "name": "error_missing_data.py", "path": path_to_check})
    if not os.path.exists(path_to_check + "/error_missing_data.ui"): everything_existing = False; missing.append({"type": "file", "name": "error_missing_data.ui", "path": path_to_check})
    if not os.path.exists(path_to_check + "/error_no_config_files_found.py"): everything_existing = False; missing.append({"type": "file", "name": "error_no_config_files_found.py", "path": path_to_check})
    if not os.path.exists(path_to_check + "/error_no_config_files_found.ui"): everything_existing = False; missing.append({"type": "file", "name": "error_no_config_files_found.ui", "path": path_to_check})
    if not os.path.exists(path_to_check + "/error_not_a_valid_config_file.py"): everything_existing = False; missing.append({"type": "file", "name": "error_not_a_valid_config_file.py", "path": path_to_check})
    if not os.path.exists(path_to_check + "/error_not_a_valid_config_file.ui"): everything_existing = False; missing.append({"type": "file", "name": "error_not_a_valid_config_file.ui", "path": path_to_check})
    if not os.path.exists(path_to_check + "/finished.py"): everything_existing = False; missing.append({"type": "file", "name": "finished.py", "path": path_to_check})
    if not os.path.exists(path_to_check + "/finished.ui"): everything_existing = False; missing.append({"type": "file", "name": "finished.ui", "path": path_to_check})
    if not os.path.exists(path_to_check + "/load_or_create_config.py"): everything_existing = False; missing.append({"type": "file", "name": "load_or_create_config.py", "path": path_to_check})
    if not os.path.exists(path_to_check + "/load_or_create_config.ui"): everything_existing = False; missing.append({"type": "file", "name": "load_or_create_config.ui", "path": path_to_check})
    if not os.path.exists(path_to_check + "/loading.py"): everything_existing = False; missing.append({"type": "file", "name": "loading.py", "path": path_to_check})
    if not os.path.exists(path_to_check + "/loading.ui"): everything_existing = False; missing.append({"type": "file", "name": "loading.ui", "path": path_to_check})
    if not os.path.exists(path_to_check + "/login.py"): everything_existing = False; missing.append({"type": "file", "name": "login.py", "path": path_to_check})
    if not os.path.exists(path_to_check + "/login.ui"): everything_existing = False; missing.append({"type": "file", "name": "login.ui", "path": path_to_check})
    if not os.path.exists(path_to_check + "/running.py"): everything_existing = False; missing.append({"type": "file", "name": "running.py", "path": path_to_check})
    if not os.path.exists(path_to_check + "/running.ui"): everything_existing = False; missing.append({"type": "file", "name": "running.ui", "path": path_to_check})
    if not os.path.exists(path_to_check + "/select_config.py"): everything_existing = False; missing.append({"type": "file", "name": "select_config.py", "path": path_to_check})
    if not os.path.exists(path_to_check + "/select_config.ui"): everything_existing = False; missing.append({"type": "file", "name": "select_config.ui", "path": path_to_check})
    if not os.path.exists(path_to_check + "/select_plants.py"): everything_existing = False; missing.append({"type": "file", "name": "select_plants.py", "path": path_to_check})
    if not os.path.exists(path_to_check + "/select_plants.ui"): everything_existing = False; missing.append({"type": "file", "name": "select_plants.ui", "path": path_to_check})
    if not os.path.exists(path_to_check + "/start.py"): everything_existing = False; missing.append({"type": "file", "name": "start.py", "path": path_to_check})
    if not os.path.exists(path_to_check + "/start.ui"): everything_existing = False; missing.append({"type": "file", "name": "start.ui", "path": path_to_check})
    if not os.path.exists(path_to_check + "/ui_main.py"): everything_existing = False; missing.append({"type": "file", "name": "ui_main.py", "path": path_to_check})
    if not os.path.exists(path_to_check + "/warning_progress_will_be_lost.py"): everything_existing = False; missing.append({"type": "file", "name": "warning_progress_will_be_lost.py", "path": path_to_check})
    if not os.path.exists(path_to_check + "/warning_progress_will_be_lost.ui"): everything_existing = False; missing.append({"type": "file", "name": "warning_progress_will_be_lost.ui", "path": path_to_check})

    # checking sub direcotry of source_code/ui
    path_to_check = os.path.join(program_root_directory, "source_code/ui/additional_ressources")
    if not os.path.exists(path_to_check + "/error.png"): everything_existing = False; missing.append({"type": "file", "name": "warning_progress_will_be_lost.ui", "path": path_to_check})
    if not os.path.exists(path_to_check + "/gifs.qrc"): everything_existing = False; missing.append({"type": "file", "name": "warning_progress_will_be_lost.ui", "path": path_to_check})
    if not os.path.exists(path_to_check + "/icons.qrc"): everything_existing = False; missing.append({"type": "file", "name": "warning_progress_will_be_lost.ui", "path": path_to_check})
    if not os.path.exists(path_to_check + "/loading.gif"): everything_existing = False; missing.append({"type": "file", "name": "warning_progress_will_be_lost.ui", "path": path_to_check})
    if not os.path.exists(path_to_check + "/warning.png"): everything_existing = False; missing.append({"type": "file", "name": "warning_progress_will_be_lost.ui", "path": path_to_check})

    #check if chromedriver exists
    path_to_check = os.path.join(program_root_directory, "webdrivers")
    if not os.path.exists(path_to_check + "/chromedriver.exe"): everything_existing = False; missing.append({"type": "file", "name": "chromedriver.exe", "path": path_to_check})

    #check if install.sh exist
    path_to_check = program_root_directory
    if not os.path.exists(path_to_check + "/install.sh"): everything_existing = False; missing.append({"type": "file", "name": "install.sh", "path": path_to_check})

    # check if starting script exists
    path_to_check = program_root_directory
    if not os.path.exists(path_to_check + "/Eneffco_diagram_creator.pyw"): everything_existing = False; missing.append({"type": "file", "name": "Eneffco_diagram_creator.pyw", "path": path_to_check})



    #used to check if method works correct, file does and should not exist
    #if not os.path.exists(path_to_check + "/test"): everything_existing = False; missing.append({"type": "file", "name": "test", "path": path_to_check})

    #TODO
    # add all files that are missing
    if not everything_existing:
        return False, missing
    return True, missing

