
def get_all_plants_as_list():
    definition_file = open("./download/InstallDefListExport.csv", "r", encoding="utf-8")
    list_all_plants = []
    for line in definition_file.readlines():
        line = line.split(";")
        if len(line) < 3:
            continue
        plant_description = line[2]
        plant_description = plant_description.split(" - ")
        plant_code = plant_description[0]
        if plant_code[0] == "\"":
            plant_code = plant_code[1:]
        if len(plant_code) == 7 and plant_code[3] == ".":
            list_all_plants.append(plant_code)
    definition_file.close()
    return list_all_plants

def get_all_plants_as_tree():
    tree_all_plants = []
    definition_file = open("./download/InstallDefListExport.csv", "r", encoding="utf-8")
    lines = definition_file.readlines()
    for row_number in range(len(lines)):
        if row_number == 0:
            continue
        line = lines[row_number].split(";")
        if line[0] == "\"\"":
            if row_number + 1 < len(lines):
                tree_all_plants.append(get_sub_tree(lines, row_number, line[2]))
    definition_file.close()
    print(tree_all_plants)
    return tree_all_plants

def get_sub_tree(lines, row_number, sub_tree_name):
    sub_tree = []
    if sub_tree_name[0] == "\"":
        sub_tree_name = sub_tree_name[1:]
    if sub_tree_name.endswith("\""):
        sub_tree_name = sub_tree_name[:len(sub_tree_name)-1]
    sub_tree.append(sub_tree_name)
    sub_tree.append([])
    sub_tree_list = sub_tree[1]
    while row_number < len(lines):
        row_number += 1
        line = lines[row_number].split(";")
        if line[0] == "\"\"":
            break
        #if (line[2].find(" - ") == -1 and line[2][3] != "." and line[2] != "\"\"") or (row_number + 1 < len(lines) and str(line[0] + "." + line[1]).replace("\"","") == lines[row_number+1].split(";")[0].replace("\"","")):
        if row_number + 1 < len(lines) and str(line[0] + "." + line[1]).replace("\"","") == lines[row_number+1].split(";")[0].replace("\"",""):
            if row_number + 1 < len(lines):
                return_value = get_sub_sub_tree(lines, row_number, line[2])
                sub_tree_list.append(return_value[1])
                row_number = return_value[0]
            else:
                break
        plant_description = line[2]
        plant_description = plant_description.split(" - ")
        plant_code = plant_description[0]
        if plant_code[0] == "\"":
            plant_code = plant_code[1:]
        if len(plant_code) == 7 and plant_code[3] == ".":
            sub_tree_list.append(plant_code)

    return sub_tree

def get_sub_sub_tree(lines, row_number, sub_tree_name):
    sub_tree = []
    if sub_tree_name[0] == "\"":
        sub_tree_name = sub_tree_name[1:]
    if sub_tree_name.endswith("\""):
        sub_tree_name = sub_tree_name[:len(sub_tree_name)-1]
    sub_tree.append(sub_tree_name)
    sub_tree.append([])
    sub_tree_list = sub_tree[1]
    while row_number < len(lines):
        row_number += 1
        line = lines[row_number].split(";")
        if line[0] != lines[row_number - 1].split(";")[0] and str(line[0]).replace("\"","") != (lines[row_number - 1].split(";")[0].replace("\"","") + "." + lines[row_number - 1].split(";")[1].replace("\"","")):
        #if line[0] == "\"\"" or line[2].find(" - ") == -1 and line[2][3] != "." and line[2] != "\"\"" or line[0] != lines[row_number-1].split(";")[0]:
            break
        plant_description = line[2]
        plant_description = plant_description.split(" - ")
        plant_code = plant_description[0]
        if plant_code[0] == "\"":
            plant_code = plant_code[1:]
        if len(plant_code) == 7 and plant_code[3] == ".":
            sub_tree_list.append(plant_code)

    return row_number-1, sub_tree

