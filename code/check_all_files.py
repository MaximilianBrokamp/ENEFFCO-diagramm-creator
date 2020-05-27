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
    if not os.path.exists(path_to_check + "/code"): everything_existing = False; missing.append({"type": "directory", "name": "code", "path": path_to_check})
    if not os.path.exists(path_to_check + "/configs"): everything_existing = False; missing.append({"type": "directory", "name": "configs", "path": path_to_check})
    if not os.path.exists(path_to_check + "/reports"): everything_existing = False; missing.append({"type": "directory", "name": "reports", "path": path_to_check})
    if not os.path.exists(path_to_check + "/templates"): everything_existing = False; missing.append({"type": "directory", "name": "templates", "path": path_to_check})
    if not os.path.exists(path_to_check + "/webdrivers"): everything_existing = False; missing.append({"type": "directory", "name": "webdrivers", "path": path_to_check})

    #checking files in Directory: code
    path_to_check = os.path.join(program_root_directory, "code")
    if not os.path.exists(path_to_check + "/__init__.py"): everything_existing = False; missing.append({"type": "file", "name": "__init__.py", "path": path_to_check})
    if not os.path.exists(path_to_check + "/additional_functions.py"): everything_existing = False; missing.append({"type": "file", "name": "additional_functions.py", "path": path_to_check})
    if not os.path.exists(path_to_check + "/check_all_files.py"): everything_existing = False; missing.append({"type": "file", "name": "check_all_files.py", "path": path_to_check})
    if not os.path.exists(path_to_check + "/class_diagram.py"): everything_existing = False; missing.append({"type": "file", "name": "class_diagram.py", "path": path_to_check})
    if not os.path.exists(path_to_check + "/diagram_creator.py"): everything_existing = False; missing.append({"type": "file", "name": "diagram_creator.py", "path": path_to_check})
    if not os.path.exists(path_to_check + "/load_config.py"): everything_existing = False;  missing.append({"type": "file", "name": "load_config.py", "path": path_to_check})
    if not os.path.exists(path_to_check + "/main.py"): everything_existing = False; missing.append({"type": "file", "name": "main.py", "path": path_to_check})

    #check if chromedriver exists
    path_to_check = os.path.join(program_root_directory, "webdrivers")
    if not os.path.exists(path_to_check + "/chromedriver.exe"): everything_existing = False; missing.append({"type": "file", "name": "chromedriver.exe", "path": path_to_check})


    #used to check if method works correct, file does and should not exist
    #if not os.path.exists(path_to_check + "/test"): everything_existing = False; missing.append({"type": "file", "name": "test", "path": path_to_check})

    #TODO
    # add all files that are missing
    print(missing)
    if not everything_existing:
        return False, missing
    return True, missing

