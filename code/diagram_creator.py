import load_config
import additional_functions as af
import time
import selenium
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import selenium.common.exceptions as exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pynput.keyboard import Key, Controller
from selenium.webdriver import ActionChains
import os
import copy


def init_driver(url):
    options = webdriver.ChromeOptions()
    path = os.path.abspath('../download')
    prefs = {'download.default_directory' : path}
    options.add_experimental_option('prefs', prefs)
    #options.add_argument("=")

    driver = webdriver.Chrome(chrome_options=options)
    driver.maximize_window()
    driver.get(url)

    return driver

def login(driver):
    # hardcoded login for test purposes
    #TODO
    # change login to manual after testing
    username_id_box = driver.find_element_by_id('SplitMain_ContentPlaceHolderBodyCenter_LoginUser_UserName')
    username_id_box.send_keys('m.brokamp')

    password_id_box = driver.find_element_by_id('SplitMain_ContentPlaceHolderBodyCenter_LoginUser_Password')
    password_id_box.send_keys('Sumpffeld00_')

    login_button = driver.find_element_by_id('SplitMain_ContentPlaceHolderBodyCenter_LoginUser_LoginButton')
    login_button.click()
#    login_timer = time.time()
    #driver.execute_script("alert('Bitte loggen Sie sich ein')")
    #WebDriverWait(driver, 300).until(EC.invisibility_of_element_located((By.LINK_TEXT,"Bitte loggen Sie sich ein")))
#   #TODO
#   # throw exception


    # wait's until the user logged in and the url changes to the one below
    # if the user hasn't logged in after five minutes it will raise exception and the script will terminate
#    while driver.current_url != "https://ewus.eneffco.de/ChartPage.aspx":
#        time.sleep(0.5)
#        if time.time() - login_timer > 300:
#            #TODO
#            # throw exception
#            return False
#    return True
# method downloads the Excel File with all Plants in it and saves them in a list

#downloads the definition file with all plants in it
#the retry variable indicates if after a failed download attempt the process should be executed again
def get_all_plants(driver, retry):

    list_all_plants = []
    af.go_to_ChartPage(driver)
    path = os.path.abspath('../download')
    if os.path.isfile(path + "/InstallDefListExport.csv"):
        os.remove(path + "/InstallDefListExport.csv")

    driver.find_element_by_xpath("// *[ @ id = 'SplitMain_0_CC'] / table / tbody / tr / td[6]").click()
    time.sleep(2)
    contex_menu = driver.find_element_by_id("SplitMain_ContentPlaceHolderBodyLeft_DefinitionLeftCtrl_DefinitionLeftPanel_PlaceHolder_ctl00_ctl00_InstLeftTreeCollapsiblePanel_ctl00_ctl00_ToolbarItemMore")

    hover = ActionChains(driver)
    hover.move_to_element(contex_menu)
    hover.perform()
    csv_download_button = driver.find_element_by_id("SplitMain_ContentPlaceHolderBodyLeft_DefinitionLeftCtrl_DefinitionLeftPanel_PlaceHolder_ctl00_ctl00_InstLeftTreeCollapsiblePanel_ctl00_ctl00_ToolbarItemMore_ToolbarItemCSVDownload").click()
    if not af.download_wait(path, "InstallDefListExport.csv"):
        if not retry:
            #TODO
            # throw exception
            return []
        else:
            get_all_plants(driver, False)

    definition_file = open(path + "/InstallDefListExport.csv", "r")
    for line in definition_file.readlines():
        line = line.split(";")
        if len(line) < 3:
            continue
        plant_description = line[2]
        plant_description= plant_description.split(" - ")
        plant_code = plant_description[0]
        if plant_code[0] == "\"":
            plant_code = plant_code[1:]

        if len(plant_code) == 7 and plant_code[3] == ".":
            if len(plant_description) < 2:
                plant_description = ""
            else:
                plant_description = plant_description[1][:len(plant_description[1])]
            print(plant_code)
            print(plant_description + "\n")
        list_all_plants.append([plant_code, plant_description])
    af.go_to_ChartPage(driver)
    return list_all_plants



    return []

def get_plants_with_exiting_diagram(driver, diagram_name):
    af.go_to_ChartPage(driver)

    af.wait_and_reload(driver, 10, 2, By.XPATH,
                       "//*[@id='SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_PlaceHolder_ctl00_InstTreeDisplayCollapsiblePanel_ctl00_ctl00_ctl03']/img")
    search_for_analysis_button = driver.find_element_by_xpath("//*[@id='SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_PlaceHolder_ctl00_InstTreeDisplayCollapsiblePanel_ctl00_ctl00_ctl03']/img")
#    if len(search_for_analysis_button) < 1:
#        af.go_to_ChartPage(driver)
#        if not af.waitForElement(driver, 10, By.XPATH,"//*[@id='SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_PlaceHolder_ctl00_InstTreeDisplayCollapsiblePanel_ctl00_ctl00_ctl03']/img"):
#            return False
#            #TODO
#            # Throw exception
#        search_for_analysis_button = driver.find_element_by_xpath(
#            "//*[@id='SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_PlaceHolder_ctl00_InstTreeDisplayCollapsiblePanel_ctl00_ctl00_ctl03']/img")
#    else:
#        search_for_analysis_button = search_for_analysis_button[0]


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
            # TODO
            # add am exeption
            driver.find_element_by_xpath(
                "//*[@id='SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_FileEntryGridPopUp_PopUp_PWH-1']/table/tbody/tr/td[2]/img").click()
            return False
        elif first_entry[0].text != diagram_name:
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
            print(row_number)
            row_number += 1
            current_row_code = driver.find_elements(By.XPATH, "//*[@id='" + analysis_search_id + "']/td[2]")
            if len(current_row_code) < 1:
                row_number -= 1
                break
            # TODO
            elif driver.find_element_by_xpath("//*[@id='" + analysis_search_id + "']/td[3]").text != diagram_name:
                print(driver.find_element_by_xpath("//*[@id='" + analysis_search_id + "']/td[2]").text)
                continue
            else:
                plant_code = current_row_code[0].text
                plant_code = plant_code.split(' ')
                if len(plant_code[0]) == 7 and plant_code[0][3] == '.':
                    plants_with_exiting_diagram.append(plant_code[0])
                    print(plant_code[0])

        # after the first Iteration the path to the next icon changes
        first_iteration = False

            #driver.find_element_by_
            #next_page_button = driver.find_elements(By.XPATH,
            #                                        "//*[@id='SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_FileEntryGridPopUp_PopUp_Panel_Grid_DXPagerBottom']/a[4]/img")
        next_page_button = driver.find_elements_by_class_name("dxp-bi")
        diabled = driver.find_elements_by_class_name("dxp-disabledButton")

        #else:
        #    next_page_button = driver.find_elements(By.XPATH,
        #                                            "//*[@id='SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_FileEntryGridPopUp_PopUp_Panel_Grid_DXPagerBottom']/a[5]/img")
        print(len(next_page_button))
        end = False
        for d in diabled:
            if d == next_page_button[1]:
                end = True
        if end:
            break

        next_page_button[1].click()
        af.waitForElement(driver, 10, By.ID,
                       "SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_FileEntryGridPopUp_PopUp_Panel_Grid_tccell" + str(row_number) + "_0")
        time.sleep(1)
    driver.find_element_by_id(
        "SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_FileEntryGridPopUp_PopUp_Panel_Grid_DXFREditorcol2_I").clear()

    driver.find_element_by_xpath(
        "//*[@id='SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_FileEntryGridPopUp_PopUp_PWH-1']/table/tbody/tr/td[2]/img").click()
    print(len(plants_with_exiting_diagram))
    return plants_with_exiting_diagram

def new_diagram(driver, plant_code, diagram_name, template_path):
    # quick test for creating a diagram
    search_plant_box = driver.find_element_by_id('SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_PlaceHolder_ctl00_InstTreeDisplayCollapsiblePanel_InstTreeDisplay_DXSE_I')


    search_plant_box.send_keys(plant_code)
    search_plant_box.send_keys(Keys.ENTER)

    time.sleep(2)
    # the id describes the first entry in the search
    # the id for the first entry should stay the same no matter the input.
    plant_icon = driver.find_element_by_xpath("// *[ @ id = 'SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_PlaceHolder_ctl00_InstTreeDisplayCollapsiblePanel_InstTreeDisplay_D'] / tbody/tr[3]")
    plant_icon.click()

    #click on Datapoints drop down button and check for special Datapoints (those that dont have the plant codes at the beginning)
    #af.waitForElement(driver, 10, By.ID, "SplitMain_ContentPlaceHolderBodyRight_ContentTabControl_ContentTabCallBackPanel_ContentPanel_ctl07_InstContentPanel_DescsGrid_InstDescsCP")
    #time.sleep(2)
    #driver.find_element_by_id("SplitMain_ContentPlaceHolderBodyRight_ContentTabControl_ContentTabCallBackPanel_ContentPanel_ctl07_InstContentPanel_DescsGrid_InstDescsCP").click()
    time.sleep(1)
    #     data_row_number = 0
    # special_datapoints = []
    # while True:
    #     row_id = "SplitMain_ContentPlaceHolderBodyRight_ContentTabControl_ContentTabCallBackPanel_ContentPanel_ctl07_InstContentPanel_DescsGrid_InstDescsCP_Grid_DXDataRow" + str(data_row_number)
    #     data_row_number += 1
    #     if af.check_existence(driver, By.ID, row_id):
    #         datapoint_description = driver.find_element_by_xpath("// *[ @ id = '" + row_id + "'] /td[2]")
    #         if datapoint_description.text.find("temperatur") != -1:
    #             datapoint_code = driver.find_element_by_xpath("//*[@id='" + row_id + "']/td[1]")
    #             special_datapoints.append([datapoint_code.text, datapoint_description.text])
    #             print(datapoint_code.text, ", ", datapoint_description.text)
    #     else:
    #         break
    # time.sleep(2)
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


    af.waitForElement(driver, 10, By.ID, "contentDlgSaveAs")
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

    af.wait_loading_finished(driver, 5)
    #af.waitForElement(driver, 30, By.ID,"SplitMain_ContentPlaceHolderBodyRight_ContentTabControl_ContentTabCallBackPanel_ContentPanel_ctl07_DashCallback_Content_ctl00_DashSettingsCallbackPanel_DashSettingsCollapsiblePanel_BindingsCollapsibelPanel_NamedRefCtrl_CBPanel_Grid_DXFREditorcol0_B-1")
    #af.waitForElement(driver, 30, By.ID,"SplitMain_ContentPlaceHolderBodyRight_ContentTabControl_ContentTabCallBackPanel_ContentPanel_ctl07_DashCallback_Content_ctl00_DashSettingsCallbackPanel_DashSettingsCollapsiblePanel_BindingsCollapsibelPanel_NamedRefCtrl_CBPanel_Grid_DXFREditorcol0_B-1")
    #af.waitForElement(driver, 10, By.ID, "SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_PlaceHolder_ctl00_InstTreeDisplayCollapsiblePanel_ctl00_ctl00_ctl02")
    driver.find_element_by_id("SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_PlaceHolder_ctl00_InstTreeDisplayCollapsiblePanel_ctl00_ctl00_ctl02").click()
    # datapoints_button = driver.find_element_by_xpath("//*[@id='SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderTabs_T1']/table/tbody/tr/td[2]")


    # wait for datapoints to load
    af.waitForElement(driver, 10, By.ID,"SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_PlaceHolder_ctl00_DescBrowsePanel_DescSearchGrid_SearchGrid_DXDataRow1")
    af.wait_loading_finished(driver, 1)
    # waitForElement(driver, 10, By.ID, "SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_PlaceHolder_ctl00_DescBrowsePanel_DescSearchGrid_SearchGrid_DXFREditorcol0_I")
    # datapoints_searchcode_box = driver.find_element_by_id("SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_PlaceHolder_ctl00_DescBrowsePanel_DescSearchGrid_SearchGrid_DXFREditorcol0_I")
    # datapoints_searchcode_box.send_keys("EWU.004")
    # time.sleep(5)
    # datapoints_searchcode_box.send_keys("EWU.004")
    # datapoints_searchcode_box.send_keys(Keys.ENTER)

    # while driver.find_element_by_id("SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_PlaceHolder_ctl00_DescBrowsePanel_DescSearchGrid_SearchGrid_DXDataRow0").text.find(plant_code) == -1:
    #     try:
    #         datapoints_searchcode_box = driver.find_element_by_id("SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_PlaceHolder_ctl00_DescBrowsePanel_DescSearchGrid_SearchGrid_DXFREditorcol0_I")
    #         datapoints_searchcode_box.clear()
    #         datapoints_searchcode_box.send_keys(plant_code)
    #         datapoints_searchcode_box.send_keys(Keys.ENTER)
    #         time.sleep(2)
    #     except:
    #         selenium.common.exceptions.StaleElementReferenceException
    #         break

    #time.sleep(1)

    # datapoints_searchcode_box.send_keys(Keys.ENTER)
    # read out all data points existing for the selected plant and save them
    row_number = 0
    datapoint_list = []
    while True:
        row_id = "SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_PlaceHolder_ctl00_DescBrowsePanel_DescSearchGrid_SearchGrid_DXDataRow" + str(row_number)
        current_datapoint = driver.find_elements(By.ID, row_id)

        if len(current_datapoint) != 0:
            datapoint_code = current_datapoint[0].text.split("\n", 1)
            print(datapoint_code[1])
            datapoint_list.append([datapoint_code[0], current_datapoint[0], datapoint_code[1]])
            row_number += 1
        else:
            break


    # read out the datapoints that are needed for the diagramm

    row_number = 0
    diagram_datapoint_list = []
    codes_to_replace = ["ACO.001", "STO.003"]
    while True:
        row_id = "SplitMain_ContentPlaceHolderBodyRight_ContentTabControl_ContentTabCallBackPanel_ContentPanel_ctl07_DashCallback_Content_ctl00_DashSettingsCallbackPanel_DashSettingsCollapsiblePanel_BindingsCollapsibelPanel_NamedRefCtrl_CBPanel_Grid_DXDataRow" + str(
            row_number)
        current_datapoint = driver.find_elements(By.ID, row_id)
        if len(current_datapoint) != 0:
            # print(current_datapoint.text)
            # print(driver.find_element_by_xpath(str("//*[@id='" + row_id + "']/td[1]")).text)
            if driver.find_element_by_xpath(str("//*[@id='" + row_id + "']/td[1]")).text == "Datenpunkt":
                datapoint = driver.find_element_by_xpath(str("//*[@id='" + row_id + "']/td[2]"))
                datapoint_drop_location_xpath = str("//*[@id='" + row_id + "']/td[6]")
                datapoint_code = datapoint.text
                datapoint_description = driver.find_element_by_xpath(str("//*[@id='" + row_id + "']/td[3]")).text
                # print(datapoint)
                for code in codes_to_replace:
                    datapoint_code = datapoint_code.replace(code, "")
                # print(datapoint)
                diagram_datapoint_list.append([datapoint_code, datapoint, datapoint_drop_location_xpath, datapoint_description])
            row_number += 1
        else:
            break

    datapoints_to_delete = []
    for diagram_datapoint in diagram_datapoint_list:
        existing = False
        #print("diagram datapoint    " + diagram_datapoint[3])
        datapoint_found = False
        for datapoint in datapoint_list:
            #print("datapoint    " +datapoint[2])
            if str(plant_code + diagram_datapoint[0]) == datapoint[0]:
                #print(diagram_datapoint[0])
                #print(datapoint[0])
                # print(diagram_datapoint[2])
                #print(datapoint[1])
                actionChains = ActionChains(driver)
                actionChains.drag_and_drop(datapoint[1], driver.find_element_by_xpath(diagram_datapoint[2])).perform()
                existing = True
                time.sleep(2)
                datapoint_found = True
            elif diagram_datapoint[3].find("Aussentemperatur") != -1 and diagram_datapoint[3].find("angepasste") == -1:
                if datapoint[2].find("Aussentemperatur") != -1 and datapoint[2].find("angepasste") == -1:
                    actionChains = ActionChains(driver)
                    actionChains.drag_and_drop(datapoint[1], driver.find_element_by_xpath(diagram_datapoint[2])).perform()
                    existing = True
                    time.sleep(2)
                    datapoint_found = True
            elif diagram_datapoint[3].find("Aussentemperatur") != -1 and diagram_datapoint[3].find("angepasste") != -1:
                if datapoint[2].find("Aussentemperatur") != -1 and datapoint[2].find("angepasste") != -1:
                    actionChains = ActionChains(driver)
                    actionChains.drag_and_drop(datapoint[1],driver.find_element_by_xpath(diagram_datapoint[2])).perform()
                    existing = True
                    time.sleep(2)
                    datapoint_found = True
            if datapoint_found:
                break
        if not datapoint_found:
            datapoints_to_delete.append(diagram_datapoint[0])


    # clicking on the "Einstellungen übernehmen" button
    driver.find_element_by_id("SplitMain_ContentPlaceHolderBodyRight_ContentTabControl_ContentTabCallBackPanel_ContentPanel_ctl07_DashCallback_Content_ctl00_DashSettingsCallbackPanel_DashSettingsCollapsiblePanel_ctl00_DashSettingsToolbar_commitSettings").click()
    af.wait_loading_finished(driver, 2)
    #TODO
    # check if the diagram has sub diagrams
    # class = dxsplPane_EnEffCo dashTilePane ui-droppable
    sub_diagrams = driver.find_elements_by_class_name("dashTilePane ")
    print(len(sub_diagrams))
    if len(sub_diagrams) > 0:
        i = 0
        while True:
            if i >= len(sub_diagrams):
                break
            actionChains = ActionChains(driver)
            actionChains.double_click(sub_diagrams[i]).perform()
            delete_wrong_datapoints(driver, datapoints_to_delete)
            driver.find_element_by_xpath("//*[contains(@title,'Zurück')]").click()
            af.wait_loading_finished(driver, 1)
            sub_diagrams = driver.find_elements_by_class_name("dashTilePane ")
            i += 1

    else:
        driver.find_element_by_xpath("// *[ @ id = 'SplitMain_ContentPlaceHolderBodyRight_ContentTabControl_ContentTabCallBackPanel_ContentPanel_ctl07_ChartContentControlPanel_ChartControl_ChartEditorCallBackPanel_ChartEditorCollapsiblePanel'] /div[1] / table / tbody / tr / td[1]").click()
        delete_wrong_datapoints(driver, datapoints_to_delete)

    driver.find_element_by_xpath("//*[@title='Speichern']").click()
    af.wait_loading_finished(driver, 1)
    #diagram_tab = driver.find_element_by_id("SplitMain_ContentPlaceHolderBodyRight_ContentTabControl_ContentTabCallBackPanel_ContentTab_AT1")
    #diagram_tab = driver.find_element_by_id("SplitMain_ContentPlaceHolderBodyRight_ContentTabControl_ContentTabCallBackPanel_ContentTab_AT1")
    close_button = driver.find_element_by_xpath("//*[@id = 'SplitMain_ContentPlaceHolderBodyRight_ContentTabControl_ContentTabCallBackPanel_ContentTab_AT1']/table/tbody/tr/td[3]")
    close_button.click()




def delete_wrong_datapoints(driver, datapoints_to_delete):
    row_number = 0
    af.wait_loading_finished(driver, 4)
    current_datapoint_code = driver.find_elements_by_class_name("grid-cell-long-text")
    delete_buttons = driver.find_elements_by_xpath("//*[@title ='Entfernen']")
    if len(current_datapoint_code) > 0:
        print(len(delete_buttons))
        print(len(current_datapoint_code))
        i = 0
        while True:
            if i >= len(current_datapoint_code):
                break
            print(current_datapoint_code[i])
            current_datapoint_code_value = current_datapoint_code[i].find_element_by_xpath(".//input").get_attribute("value")
            print(current_datapoint_code_value)

            for datapoint in datapoints_to_delete:
                print("datapoint to delete value:   ", datapoint)
                print("cueen_datapoint_code value:  ", current_datapoint_code)
                if current_datapoint_code_value.endswith(datapoint):
                    delete_buttons[i].click()
                    time.sleep(1)
                    current_datapoint_code = driver.find_elements_by_class_name("grid-cell-long-text")
                    delete_buttons = driver.find_elements_by_xpath("//*[@title ='Entfernen']")
                    i -= 1
                    break
            i += 1
    else:
        print(len(driver.window_handles))
        html_button = driver.find_elements_by_id("SplitMain_ContentPlaceHolderBodyRight_ContentTabControl_ContentTabCallBackPanel_ContentPanel_ctl07_DashCallback_Content_ctl00_HtmlEditCP_HtmlEditCBPanel_Editor_TC_T1T")
        if len(html_button) > 0:
            driver.switch_to.frame("SplitMain_ContentPlaceHolderBodyRight_ContentTabControl_ContentTabCallBackPanel_ContentPanel_ctl07_DashCallback_Content_ctl00_HtmlEditCP_HtmlEditCBPanel_Editor_DesignIFrame")
            #table = driver.find_element_by_xpath("/html/body/table")
            current_datapoints = driver.find_elements_by_class_name("dyntxttag")
            print("len current_datapoints: ", len(current_datapoints))
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


def main():
    diagram = load_config.load_config()
    print(diagram.template_path)
    driver = init_driver("https://ewus.eneffco.de/ChartPage.aspx")
    login(driver)
    print(len(driver.window_handles))
    #all_plants = get_all_plants(driver, True)
    #plant_with_existing_diagrams = get_plants_with_exiting_diagram(driver, diagram.name)

    new_diagram(driver, "EWU.004", "00_Anlagenüberwachung", diagram.template_path)

    af.checkIfWindowIsClosed(driver)






if  __name__ == "__main__":
    main()
