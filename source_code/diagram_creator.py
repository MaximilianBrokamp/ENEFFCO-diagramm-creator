from source_code import additional_functions as af
import time
import os
import datetime
import traceback

from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from pynput.keyboard import Key, Controller
from selenium.webdriver import ActionChains

from source_code import extract_plants


#starts the chrome dirver and opens the website defined in "url"
#additionally chages the download directory
def init_driver(url):
    options = webdriver.ChromeOptions()
    relative_exe_path = "./webdrivers/chromedriver.exe"
    abs_exe_path = os.path.abspath(relative_exe_path)
    path = os.path.abspath('./download')
    prefs = {'download.default_directory': path}
    options.add_experimental_option('prefs', prefs)
    #options.add_argument("=")
    driver = webdriver.Chrome(executable_path=abs_exe_path, options=options)
    driver.maximize_window()
    driver.get(url)
    return driver

def login(driver):
    # hardcoded login for test purposes
   # username_id_box = driver.find_element_by_id('SplitMain_ContentPlaceHolderBodyCenter_LoginUser_UserName')
   # username_id_box.send_keys('')
   # password_id_box = driver.find_element_by_id('SplitMain_ContentPlaceHolderBodyCenter_LoginUser_Password')
   # password_id_box.send_keys('')

    #login_button = driver.find_element_by_id('SplitMain_ContentPlaceHolderBodyCenter_LoginUser_LoginButton')
    #login_button.click()

    # wait's until the user logged in and the url changes to the one below
    # if the user hasn't logged in after five minutes it will raise exception and the script will terminate
    while driver.current_url != "https://ewus.eneffco.de/ChartPage.aspx":
        time.sleep(0.5)
    return True


# method downloads the Excel File with all Plants in it and saves them in a list
#downloads the definition file with all plants in it
#the retry variable indicates if after a failed download attempt the process should be executed again
def get_all_plants(driver, retry):
    list_all_plants = []
    af.go_to_ChartPage(driver)
    path = os.path.abspath('./download')
    if os.path.isfile(path + "/InstallDefListExport.csv"):
        os.remove(path + "/InstallDefListExport.csv")

    driver.find_element_by_xpath("// *[ @ id = 'SplitMain_0_CC'] / table / tbody / tr / td[6]").click()
    time.sleep(2)
    contex_menu = driver.find_element_by_id("SplitMain_ContentPlaceHolderBodyLeft_DefinitionLeftCtrl_DefinitionLeftPanel_PlaceHolder_ctl00_ctl00_InstLeftTreeCollapsiblePanel_ctl00_ctl00_ToolbarItemMore")

    hover = ActionChains(driver)
    hover.move_to_element(contex_menu)
    hover.perform()
    time.sleep(1)
    driver.find_element_by_id("SplitMain_ContentPlaceHolderBodyLeft_DefinitionLeftCtrl_DefinitionLeftPanel_PlaceHolder_ctl00_ctl00_InstLeftTreeCollapsiblePanel_ctl00_ctl00_ToolbarItemMore_ToolbarItemCSVDownload").click()
    if not af.download_wait(path, "InstallDefListExport.csv"):
        if not retry:
            return None
        else:
            get_all_plants(driver, False)

    tree_all_plants = extract_plants.get_all_plants_as_tree()
    list_all_plants = extract_plants.get_all_plants_as_list()
    return [tree_all_plants, list_all_plants]

def get_plants_with_exiting_diagram(driver, diagram_name):
    #eiminate spaces at the end of a diagram name
    while diagram_name.endswith(" "):
        diagram_name = diagram_name[:len(diagram_name)-1]

    af.go_to_ChartPage(driver)

    af.wait_and_reload(driver, 10, 2, By.XPATH,"//*[@id='SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_PlaceHolder_ctl00_InstTreeDisplayCollapsiblePanel_ctl00_ctl00_ctl03']/img")
    search_for_analysis_button = driver.find_element_by_xpath("//*[@id='SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_PlaceHolder_ctl00_InstTreeDisplayCollapsiblePanel_ctl00_ctl00_ctl03']/img")


    search_for_analysis_button.click()
    af.waitForElement(driver, 10, By.ID,
                          "SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_FileEntryGridPopUp_PopUp_Panel_Grid_DXFREditorcol2_I")


    name_search_box = driver.find_element_by_id(
        "SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_FileEntryGridPopUp_PopUp_Panel_Grid_DXFREditorcol2_I")

    name_search_box.send_keys(diagram_name)
    name_search_box.send_keys(Keys.ENTER)
    while True:
        first_entry = driver.find_elements(By.ID,
                                           "SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_FileEntryGridPopUp_PopUp_Panel_Grid_tccell0_2")
        if len(first_entry) < 1:
            driver.find_element_by_xpath(
                "//*[@id='SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_FileEntryGridPopUp_PopUp_PWH-1']/table/tbody/tr/td[2]/img").click()
            return False
        elif first_entry[0].text.find(diagram_name) == -1:
            time.sleep(2)
            continue
        else:
            break

    plants_with_exiting_diagram = []
    row_number = 0
    while True:
        analysis_search_id = ""
        while True:
            analysis_search_id = "SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_FileEntryGridPopUp_PopUp_Panel_Grid_DXDataRow" + str(row_number)
            row_number += 1
            current_row_code = driver.find_elements(By.XPATH, "//*[@id='" + analysis_search_id + "']/td[2]")
            if len(current_row_code) < 1:
                row_number -= 1
                break
            # checks if the name of the diagram in the current row starts wit diagram_name
            # to change the check to an exact accordance change to:  elif driver.find_element_by_xpath("//*[@id='" + analysis_search_id + "']/td[3]").text != diagram_name:
            elif not driver.find_element_by_xpath("//*[@id='" + analysis_search_id + "']/td[3]").text.startswith(diagram_name):
                continue
            else:
                plant_code = current_row_code[0].text
                plant_code = plant_code.split(' ')
                if len(plant_code[0]) == 7 and plant_code[0][3] == '.':
                    if plant_code[0] not in plants_with_exiting_diagram:
                        plants_with_exiting_diagram.append(plant_code[0])

        # after the first Iteration the path to the next icon changes
        first_iteration = False
        next_page_button = driver.find_elements_by_class_name("dxp-bi")
        diabled = driver.find_elements_by_class_name("dxp-disabledButton")
        if len(next_page_button) == 0:
            break
        end = False
        for d in diabled:
            if d == next_page_button[1]:
                end = True
        if end:
            break

        next_page_button[1].click()
        af.waitForElement(driver, 10, By.ID,"SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_FileEntryGridPopUp_PopUp_Panel_Grid_tccell" + str(row_number) + "_0")
        time.sleep(1)
    driver.find_element_by_id("SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_FileEntryGridPopUp_PopUp_Panel_Grid_DXFREditorcol2_I").clear()

    driver.find_element_by_xpath("//*[@id='SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_FileEntryGridPopUp_PopUp_PWH-1']/table/tbody/tr/td[2]/img").click()
    return plants_with_exiting_diagram

def new_diagram(driver, plant_code, diagram_name, template_path, diagram_type):

    af.go_to_ChartPage(driver)
    af.wait_loading_finished(driver, 1)

    time.sleep(2)

    plant_found = search_for_plant(driver, plant_code)
    if not plant_found:
        return 2, "could not find plant"

    uppload_completed = upload_defintion(driver, template_path, diagram_name)
    if not uppload_completed:
        return 2, "could not upload template"


    keyboard = Controller()
    #checks if the name of the diagram is the same as the one displayed in the content tab
    #if they are not the same there is already a diagram with this name and the current one is a ducplicate, which will be delete
    if diagram_name != driver.find_element_by_xpath(".//*[@id='SplitMain_ContentPlaceHolderBodyRight_ContentTabControl_ContentTabCallBackPanel_ContentTab_AT1']/table/tbody/tr/td[2]").text:
        diagram_name = driver.find_element_by_xpath(".//*[@id='SplitMain_ContentPlaceHolderBodyRight_ContentTabControl_ContentTabCallBackPanel_ContentTab_AT1']/table/tbody/tr/td[2]").text
        driver.find_element_by_xpath(".//*[@id='SplitMain_ContentPlaceHolderBodyRight_ContentTabControl_ContentTabCallBackPanel_ContentTab_AT1']/table/tbody/tr/td[3]").click()
        af.wait_loading_finished(driver, 1)
        diagram = af.find_diagram_in_evaluation_tab(driver, diagram_name)
        if diagram is not None:
            actionChains = ActionChains(driver)
            actionChains.context_click(diagram).perform()
            #actionChains.send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER)
            #actionChains.perform()
            context_menus = driver.find_elements_by_class_name("context-menu-list")
            for context_menu in context_menus:
                if context_menu.get_attribute("style") == "display: none;":
                    continue
                context_menu.find_element_by_xpath(".//li[2]").click()
                time.sleep(1)
                keyboard.press(Key.enter)
                keyboard.release(Key.enter)
                af.wait_loading_finished(driver, 1)
                return 2, "diagram already exists"
        else:
            return 2, "diagram already exists, found no matching diagram to delete"

    replace_datapoints_reutrn_value = replace_datapoints(driver, plant_code, diagram_type)
    if not replace_datapoints_reutrn_value[0]:
        return 2, replace_datapoints_reutrn_value[1]
    else:
        datapoints_to_delete = replace_datapoints_reutrn_value[1]
        number_datapoints = replace_datapoints_reutrn_value[2]
        number_not_matching_datapoints = replace_datapoints_reutrn_value[3]



    # clicking on the "Einstellungen übernehmen" button
    driver.find_element_by_xpath(".//*[@title = 'Einstellungen übernehmen']").click()
    af.wait_loading_finished(driver, 2)
    # checks if the diagram has sub diagrams
    sub_diagrams = driver.find_elements_by_class_name("dashTilePane")
    retry = False
    if len(sub_diagrams) > 0:
        i = 0
        while True:
            if i >= len(sub_diagrams):
                break
            actionChains = ActionChains(driver)
            actionChains.double_click(sub_diagrams[i]).perform()
            delete_wrong_datapoints(driver, datapoints_to_delete)
            if len(driver.find_elements_by_class_name("dashTilePane")) > 0:
                if retry:
                    return 2, "could not delete wrong datapoints, diagram not published"
                retry = True
                sub_diagrams = driver.find_elements_by_class_name("dashTilePane")
                continue
            driver.find_element_by_xpath("//*[contains(@title,'Zurück')]").click()
            af.wait_loading_finished(driver, 1)
            sub_diagrams = driver.find_elements_by_class_name("dashTilePane")
            i += 1

    else:
        driver.find_element_by_xpath("// *[ @ id = 'SplitMain_ContentPlaceHolderBodyRight_ContentTabControl_ContentTabCallBackPanel_ContentPanel_ctl07_ChartContentControlPanel_ChartControl_ChartEditorCallBackPanel_ChartEditorCollapsiblePanel'] /div[1] / table / tbody / tr / td[1]").click()
        delete_wrong_datapoints(driver, datapoints_to_delete)
        af.wait_loading_finished(driver, 1)

    # click save burron
    driver.find_element_by_xpath("//*[@title='Speichern']").click()
    af.wait_loading_finished(driver, 1)

    tab_control = driver.find_element_by_id("SplitMain_ContentPlaceHolderBodyRight_ContentTabControl_ContentTabCallBackPanel_ContentTab_AT1")
    tab_control.find_element_by_xpath(".//table/tbody/tr/td[3]").click()
    af.wait_loading_finished(driver, 1)

    #if the dialoug window "do you want to save changes" pop's up the enter press will confirm this
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    af.wait_loading_finished(driver, 1)


    # searches for the created diagram in the evaluation tab
    # if it's found it will be published
    diagram = af.find_diagram_in_evaluation_tab(driver, diagram_name)
    if diagram is not None:
        actionChains = ActionChains(driver)
        actionChains.context_click(diagram)
        actionChains.perform()
        context_menus = driver.find_elements_by_class_name("context-menu-list")
        for context_menu in context_menus:
            if context_menu.get_attribute("style") == "display: none;":
                continue
            context_menu.find_element_by_xpath(".//li[5]").click()
            af.wait_loading_finished(driver, 1)
            return 0, "diagram created successfuly", number_datapoints, number_not_matching_datapoints
    #    i += 1
    return 1, "could not publish created diagarm", number_datapoints, number_not_matching_datapoints

# searches for the plant in the right searchbox
# if the plant is found the programm will clik on the corresponding button
# if its not found it will retry one time. After the second failure it will return False
def search_for_plant(driver, plant_code):
    #//*[contains(text(),'match')]

    for i in range(2):
        search_plant_box = driver.find_element_by_id('SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_PlaceHolder_ctl00_InstTreeDisplayCollapsiblePanel_InstTreeDisplay_DXSE_I')
        if i == 1:
            search_plant_box.clear()
            time.sleep(2)
            search_plant_box = driver.find_element_by_id('SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_PlaceHolder_ctl00_InstTreeDisplayCollapsiblePanel_InstTreeDisplay_DXSE_I')

        search_plant_box.send_keys(plant_code)
        time.sleep(1)
        search_plant_box = driver.find_element_by_id('SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_PlaceHolder_ctl00_InstTreeDisplayCollapsiblePanel_InstTreeDisplay_DXSE_I')
        search_plant_box.send_keys(Keys.ENTER)
        af.wait_loading_finished(driver, 1)
        panel = driver.find_elements_by_id("SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_PlaceHolder_ctl00_InstTreeDisplayCollapsiblePanel_InstTreeDisplay_D")

        #plant_description = driver.find_elements_by_xpath("// *[ @ id = 'SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_PlaceHolder_ctl00_InstTreeDisplayCollapsiblePanel_InstTreeDisplay_D'] / tbody/tr[3]/td[3]/table/tbody/tr/td/span/span/span")
        if len(panel) > 0:
            plant_button = driver.find_elements_by_xpath("//*[contains(text(),'" + plant_code + "')]")
            if len(plant_button) > 0 and plant_button[1].text[:7] == plant_code:
                plant_button[1].click()
                break
            else:
                if i == 1:
                    return False
                continue
        else:
            if i == 1:
                return False
            continue
    #plant_icon = driver.find_element_by_xpath("// *[ @ id = 'SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_PlaceHolder_ctl00_InstTreeDisplayCollapsiblePanel_InstTreeDisplay_D'] / tbody/tr[3]")
    #plant_icon.click()

    af.wait_loading_finished(driver, 1)
    return True


# uploads the defintion of the diagram
# the correct plant needs to be already selcted
# returns True if it works, false if it dosen't
def upload_defintion(driver, template_path, diagram_name):
    upload_definition_button = driver.find_element_by_id('SplitMain_ContentPlaceHolderBodyRight_ContentTabControl_ContentTabCallBackPanel_ContentPanel_ctl07_InstContentPanel_InstFolderDisplay_InstFolderDisplayCP_ctl00_ctl00_ctl00')
    upload_definition_button.click()

    af.waitForElement(driver, 10, By.ID,"SplitMain_ContentPlaceHolderBodyRight_ContentTabControl_ContentTabCallBackPanel_ContentPanel_ctl07_InstContentPanel_FileUploadCtrl_FileUploadPopUp_UploadCtrl_TextBox0_FakeInput")
    upload_definition_box = driver.find_element_by_id('SplitMain_ContentPlaceHolderBodyRight_ContentTabControl_ContentTabCallBackPanel_ContentPanel_ctl07_InstContentPanel_FileUploadCtrl_FileUploadPopUp_UploadCtrl_Browse0')
    upload_definition_box.click()
    time.sleep(2)

    # simulating the keyboard to enter the path and file name for the upload

    keyboard = Controller()
    keyboard.type(template_path)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

    # should entering the path not work the programm will try a second time
    # if it still dosen't work it will close the upload window and reutrn false
    if not af.waitForElement(driver, 10, By.ID, "contentDlgSaveAs"):
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        keyboard = Controller()
        keyboard.type(template_path)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        if not af.waitForElement(driver, 10, By.ID, "contentDlgSaveAs"):
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            # presses three times tab and on time enter to close the upload window
            for i in range(3):
                keyboard.press(Key.tab)
                keyboard.release(Key.tab)
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            driver.find_element_by_xpath("//*[@id='SplitMain_ContentPlaceHolderBodyRight_ContentTabControl_ContentTabCallBackPanel_ContentPanel_ctl07_InstContentPanel_FileUploadCtrl_FileUploadPopUp_PWH-1']/table/tbody/tr/td[2]/img").click()
            return False
    # wirtes the diagram_name into the name field
    Name_field = driver.find_element_by_xpath("//*[@id='contentDlgSaveAsNewName']")
    Name_field.clear()
    Name_field.send_keys(diagram_name)
    save_as_private = driver.find_element_by_xpath(".//*[@value = 'private']")
    save_as_private.click()
    # enter press to confirm upload
    #keyboard.press(Key.enter)
    #keyboard.release(Key.enter)
    save_button = driver.find_element_by_xpath(".//*[text() = 'Speichern'][ @type='button']")
    save_button.click()
    af.wait_loading_finished(driver, 1)
    return True

def replace_datapoints(driver, plant_code, diagram_type):
    af.wait_loading_finished(driver, 5)
    driver.find_element_by_id("SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_PlaceHolder_ctl00_InstTreeDisplayCollapsiblePanel_ctl00_ctl00_ctl02").click()
    # wait for datapoints to load
    af.waitForElement(driver, 10, By.ID,"SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_PlaceHolder_ctl00_DescBrowsePanel_DescSearchGrid_SearchGrid_DXDataRow1")
    af.wait_loading_finished(driver, 1)

    # datapoints_searchcode_box.send_keys(Keys.ENTER)
    # read out all data points existing for the selected plant and save them
    row_number = 0
    datapoint_list = []
    while True:
        row_id = "SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_PlaceHolder_ctl00_DescBrowsePanel_DescSearchGrid_SearchGrid_DXDataRow" + str(row_number)
        current_datapoint = driver.find_elements(By.ID, row_id)

        if len(current_datapoint) != 0:
            datapoint_code = current_datapoint[0].text.split("\n", 1)
            datapoint_list.append([datapoint_code[0], current_datapoint[0], datapoint_code[1]])
            row_number += 1
        else:
            break

    if len(datapoint_list) == 0:
        return False, "plant has no datapoints"

    af.wait_loading_finished(driver, 0)
    # read out the datapoints that are needed for the diagramm
    row_number = 0
    diagram_datapoint_list = []
    while True:
        if diagram_type == "EnEffCoDashBoard":
            row_id = "SplitMain_ContentPlaceHolderBodyRight_ContentTabControl_ContentTabCallBackPanel_ContentPanel_ctl07_DashCallback_Content_ctl00_DashSettingsCallbackPanel_DashSettingsCollapsiblePanel_BindingsCollapsibelPanel_NamedRefCtrl_CBPanel_Grid_DXDataRow" + str(
                row_number)
        elif diagram_type == "EnEffCoChart":
            row_id = "SplitMain_ContentPlaceHolderBodyRight_ContentTabControl_ContentTabCallBackPanel_ContentPanel_ctl07_ChartContentControlPanel_SettingsCtrl_ChartSettingsCallbackPanel_ChartSettingsCollapsiblePanel_BindingsCollapsible_NamedRefCtrl_CBPanel_Grid_DXDataRow" + str(
                row_number)
        else:
            return False, "no, valid diagram type"
        current_datapoint = driver.find_elements(By.ID, row_id)
        if len(current_datapoint) != 0:
            if driver.find_element_by_xpath(str("//*[@id='" + row_id + "']/td[1]")).text == "Datenpunkt":
                datapoint = driver.find_element_by_xpath(str("//*[@id='" + row_id + "']/td[2]"))
                datapoint_drop_location_xpath = str("//*[@id='" + row_id + "']/td[6]")
                datapoint_code = datapoint.text
                datapoint_description = driver.find_element_by_xpath(str("//*[@id='" + row_id + "']/td[3]")).text
                #CHANGED
                if len(datapoint_code) > 8 and datapoint_code[3] == "." and datapoint_code[7]:
                    datapoint_code = datapoint_code[7:]
                diagram_datapoint_list.append([datapoint_code, datapoint, datapoint_drop_location_xpath, datapoint_description])
            row_number += 1
        else:
            break
    datapoints_to_delete = []
    for diagram_datapoint in diagram_datapoint_list:
        existing = False
        datapoint_found = False
        for datapoint in datapoint_list:
            if str(plant_code + diagram_datapoint[0]) == datapoint[0]:
                actionChains = ActionChains(driver)
                actionChains.drag_and_drop(datapoint[1], driver.find_element_by_xpath(diagram_datapoint[2])).perform()
                existing = True
                time.sleep(2)
                datapoint_found = True
            elif diagram_datapoint[3].find("Aussentemperatur") != -1 and diagram_datapoint[3].find("angepasste") == -1:
                if datapoint[2].find("Aussentemperatur") != -1 and datapoint[2].find("angepasste") == -1:
                    actionChains = ActionChains(driver)
                    actionChains.drag_and_drop(datapoint[1],
                                               driver.find_element_by_xpath(diagram_datapoint[2])).perform()
                    existing = True
                    time.sleep(2)
                    datapoint_found = True
            elif diagram_datapoint[3].find("Aussentemperatur") != -1:
                if datapoint[2].find("Aussentemperatur"):
                    actionChains = ActionChains(driver)
                    actionChains.drag_and_drop(datapoint[1],driver.find_element_by_xpath(diagram_datapoint[2])).perform()
                    existing = True
                    time.sleep(2)
                    datapoint_found = True
            if datapoint_found:
                break
        if not datapoint_found:
            datapoints_to_delete.append(diagram_datapoint[0])
    number_datapoints = len(diagram_datapoint_list)
    number_not_matching_datapoints = len(datapoints_to_delete)

    if number_datapoints == number_not_matching_datapoints:
        return False, "plant has 0 datapoints for the template"

    return True, datapoints_to_delete, number_datapoints, number_not_matching_datapoints

def delete_wrong_datapoints(driver, datapoints_to_delete):
    row_number = 0
    af.wait_loading_finished(driver, 4)
    current_datapoint_code = driver.find_elements_by_class_name("grid-cell-long-text")
    delete_buttons = driver.find_elements_by_xpath("//*[@title ='Entfernen']")
    if len(current_datapoint_code) > 0:
        i = 0
        while True:
            if i >= len(current_datapoint_code):
                break
            current_datapoint_code_value = current_datapoint_code[i].find_element_by_xpath(".//input").get_attribute("value")

            for datapoint in datapoints_to_delete:
                if current_datapoint_code_value.endswith(datapoint):
                    delete_buttons[i].click()
                    af.wait_loading_finished(driver, 1)
                    current_datapoint_code = driver.find_elements_by_class_name("grid-cell-long-text")
                    delete_buttons = driver.find_elements_by_xpath("//*[@title ='Entfernen']")
                    i -= 1
                    break
            i += 1
    else:
        html_button = driver.find_elements_by_id("SplitMain_ContentPlaceHolderBodyRight_ContentTabControl_ContentTabCallBackPanel_ContentPanel_ctl07_DashCallback_Content_ctl00_HtmlEditCP_HtmlEditCBPanel_Editor_TC_T1T")
        if len(html_button) > 0:
            driver.switch_to.frame("SplitMain_ContentPlaceHolderBodyRight_ContentTabControl_ContentTabCallBackPanel_ContentPanel_ctl07_DashCallback_Content_ctl00_HtmlEditCP_HtmlEditCBPanel_Editor_DesignIFrame")
            #table = driver.find_element_by_xpath("/html/body/table")
            af.wait_loading_finished(driver, 1)
            current_datapoints = driver.find_elements_by_class_name("dyntxttag")
            i = 0
            while True:
                if i >= len(current_datapoints):
                    break
                for datapoint in datapoints_to_delete:
                    if current_datapoints[i].get_attribute("src").find(datapoint) != -1:
                        current_datapoints[i].click()
                        driver.switch_to.default_content()
                        driver.find_element_by_id("SplitMain_ContentPlaceHolderBodyRight_ContentTabControl_ContentTabCallBackPanel_ContentPanel_ctl07_DashCallback_Content_ctl00_HtmlEditCP_HtmlEditCBPanel_Editor_TD_T0_DXI12_T").click()
                        driver.switch_to.frame("SplitMain_ContentPlaceHolderBodyRight_ContentTabControl_ContentTabCallBackPanel_ContentPanel_ctl07_DashCallback_Content_ctl00_HtmlEditCP_HtmlEditCBPanel_Editor_DesignIFrame")
                        current_datapoints = driver.find_elements_by_class_name("dyntxttag")
                        time.sleep(1.5)
                        i = i-1
                        break
                i += 1
            driver.switch_to.default_content()
    af.wait_loading_finished(driver, 2)

def create_report(diagram, task_complete, duration, number_created_diagrams, number_diagrams_to_create, number_successfully_created_diagrams, number_failed_diagrams, number_Warnings):
    # create the report file, should a file with this exact name already exists, it will add a number to the file name
    report_loccation = os.path.abspath("./reports")
    report_name = diagram.report_name + ".txt"
    report_path = os.path.join(report_loccation, report_name)
    i = 1
    while os.path.exists(report_path):
        report_name = diagram.report_name + str(i) +".txt"
        report_path = os.path.join(report_loccation, report_name)
        i += 1
    report = open(report_path, "w", encoding="utf-8")

    beginning = "Report for diagram : " + diagram.diagram_name + "\n"
    beginning += "associated Config File: " + diagram.config_file_name + "\n"
    beginning += "\n"
    beginning += "Task Complete: " + str(task_complete) + "     " + str(number_created_diagrams) + " out of " + str(number_diagrams_to_create) + " (" + str(round(((number_created_diagrams/number_diagrams_to_create)*100), 2)) + "%) " + "processed\n"
    beginning += "total time spend: " + str(round(duration, 1)) + " Minutes\n"
    beginning += str(number_failed_diagrams) + " FAILED    " + str(number_successfully_created_diagrams) + " Successfully created    " + str(number_Warnings) + " WARNINGS \n\n"
    report.write(beginning)
    i = 1
    line = ""
    for plant in diagram.plants_with_created_diagram:
        line = str(i) + ".   plant code: " + plant[0] + "    time: " + str(plant[3]) + "    duration: " + str(plant[4]) +" Seconds   " + plant[2] + "\n"
        i += 1
        report.write(line)

    report.close()
    return report_path


def create_diagram(driver, diagram_type, diagram_name, plant_code, template_path, diagram):
    start_diagram = datetime.datetime.now()
    successful = False
    warning = False
    try:
        return_value = new_diagram(driver, plant_code, diagram_name, template_path, diagram_type)
        finished_diagram = datetime.datetime.now()
        delta = finished_diagram - start_diagram
        duration_diagram = delta.total_seconds()
        message = ""
        data = []
        if return_value[0] == 0:
            successful = True
            message = return_value[1] + ", " + str(return_value[2] - return_value[3]) + " out of " + str(return_value[2]) + " datapoints from the template could be replaced "
            data = [plant_code, return_value[0], message,  datetime.datetime.now(), duration_diagram]
        elif return_value[0] == 1:
            successful = True
            warning = True
            message = "diagram created Successfully, !WARNING: " + return_value[1] + "!," + str(return_value[3]) + " out of " + str(return_value[2]) + " datapoints from the template could be replaced"
            data = [plant_code, return_value[0], message, datetime.datetime.now(), duration_diagram]
        elif return_value[0] == 2:
            message = "!!!ERROR Could not create diagram!!! : " + return_value[1]
            data = [plant_code, return_value[0], message, datetime.datetime.now(), duration_diagram]
        diagram.add_plant(data)
    except:
        finished_diagram = datetime.datetime.now()
        delta = finished_diagram - start_diagram
        duration_diagram = delta.total_seconds()
        tb = traceback.format_exc()
        #number_failed_diagrams += 1
        message = "!!!ERROR!!! Ecxeption:" + tb.replace("\n", " ")
        data = [plant_code, 3, message, datetime.datetime.now(), duration_diagram]
        data = [plant_code, 3, message, datetime.datetime.now(), duration_diagram]
        diagram.add_plant(data)
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




