import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pynput.keyboard import Key, Controller
from selenium.webdriver.chrome.options import Options

import time


# temporary login method
# uses login data from a user written directly into the function
def login(driver):
    username_id_box = driver.find_element_by_id('SplitMain_ContentPlaceHolderBodyCenter_LoginUser_UserName')
    username_id_box.send_keys('m.brokamp')

    password_id_box = driver.find_element_by_id('SplitMain_ContentPlaceHolderBodyCenter_LoginUser_Password')
    password_id_box.send_keys('Sumpffeld00_')

    login_button = driver.find_element_by_id('SplitMain_ContentPlaceHolderBodyCenter_LoginUser_LoginButton')
    login_button.click()


# checks if the main window is closed in an defined interval
# script is effectively paused when this method is called until the window is closed
def checkIfWindowIsClosed(driver):
    while True:
        try:
            whandle = driver.window_handles
            time.sleep(0.5)
        except selenium.common.exceptions.WebDriverException:
            print("Chrome Window closed")
            exit(1)

def waitForElement(driver, length, search_type, search_value):
    try:
        WebDriverWait(driver, length).until(
            EC.element_to_be_clickable((search_type, search_value))
        )
    except selenium.common.exceptions.TimeoutException:
        #driver.quit()
        print("could not find element in time")
        checkIfWindowIsClosed(driver)
        #exit(1)

def init():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(chrome_options=chrome_options)

    driver.maximize_window()

    facility_code = "EWU.004"
    daigram_template_code = "ACO.001"
    #driver.implicitly_wait(5)
    # Open the website
    driver.get('https://ewus.eneffco.de/ChartPage.aspx')
    login(driver)

    # quick test for creating a diagram
    search_facilities_box = driver.find_element_by_id('SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_PlaceHolder_ctl00_InstTreeDisplayCollapsiblePanel_InstTreeDisplay_DXSE_I')
    search_facilities_box.send_keys('EWU.004')
    search_facilities_box.send_keys(Keys.ENTER)

    time.sleep(2)
    # the id describes the first entry in the search
    # the id for the first entry should stay the same no matter the input.
    facility_icon = driver.find_element_by_xpath("// *[ @ id = 'SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_PlaceHolder_ctl00_InstTreeDisplayCollapsiblePanel_InstTreeDisplay_D'] / tbody/tr[3]")
    facility_icon.click()

    time.sleep(2)
    upload_definition_button = driver.find_element_by_id('SplitMain_ContentPlaceHolderBodyRight_ContentTabControl_ContentTabCallBackPanel_ContentPanel_ctl07_InstContentPanel_InstFolderDisplay_InstFolderDisplayCP_ctl00_ctl00_ctl00')
    upload_definition_button.click()

    waitForElement(driver, 10, By.ID, "SplitMain_ContentPlaceHolderBodyRight_ContentTabControl_ContentTabCallBackPanel_ContentPanel_ctl07_InstContentPanel_FileUploadCtrl_FileUploadPopUp_UploadCtrl_TextBox0_FakeInput")
    upload_definition_box = driver.find_element_by_id('SplitMain_ContentPlaceHolderBodyRight_ContentTabControl_ContentTabCallBackPanel_ContentPanel_ctl07_InstContentPanel_FileUploadCtrl_FileUploadPopUp_UploadCtrl_Browse0')
    upload_definition_box.click()
    time.sleep(2)

    #simulating the keyboard to enter the path and file name for the upload


    keyboard = Controller()
    keyboard.type("C:\\Users\\Brokamp\\Desktop\\00 Anlagenüberwachung.EnEffCoDashBoard")
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)


    #TODO
    #change sleep to a dynnamic waiting
    time.sleep(5)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

    waitForElement(driver, 30, By.ID , "SplitMain_ContentPlaceHolderBodyRight_ContentTabControl_ContentTabCallBackPanel_ContentPanel_ctl07_DashCallback_Content_ctl00_DashSettingsCallbackPanel_DashSettingsCollapsiblePanel_BindingsCollapsibelPanel_NamedRefCtrl_CBPanel_Grid_DXFREditorcol0_B-1")
    waitForElement(driver, 10, By.ID , "SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderTabs_T1")
    datapoints_button = driver.find_element_by_id("SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderTabs_T1")
    #datapoints_button = driver.find_element_by_xpath("//*[@id='SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderTabs_T1']/table/tbody/tr/td[2]")
    datapoints_button.click()

    # wait for datapoints to load
    waitForElement(driver, 10, By.ID,"SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_PlaceHolder_ctl00_DescBrowsePanel_DescSearchGrid_SearchGrid_DXDataRow1")
    #waitForElement(driver, 10, By.ID, "SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_PlaceHolder_ctl00_DescBrowsePanel_DescSearchGrid_SearchGrid_DXFREditorcol0_I")
    #datapoints_searchcode_box = driver.find_element_by_id("SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_PlaceHolder_ctl00_DescBrowsePanel_DescSearchGrid_SearchGrid_DXFREditorcol0_I")
    #datapoints_searchcode_box.send_keys("EWU.004")
    #time.sleep(5)
    #datapoints_searchcode_box.send_keys("EWU.004")
    #datapoints_searchcode_box.send_keys(Keys.ENTER)
    #TODO
    #Change EWU.004 to a variable which containins the current facility code
    while driver.find_element_by_id("SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_PlaceHolder_ctl00_DescBrowsePanel_DescSearchGrid_SearchGrid_DXDataRow0").text.find("EWU.004") == -1:
        try:
            datapoints_searchcode_box = driver.find_element_by_id("SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_PlaceHolder_ctl00_DescBrowsePanel_DescSearchGrid_SearchGrid_DXFREditorcol0_I")
            datapoints_searchcode_box.clear()
            datapoints_searchcode_box.send_keys("EWU.004")
            datapoints_searchcode_box.send_keys(Keys.ENTER)
            time.sleep(2)
        except:
            selenium.common.exceptions.StaleElementReferenceException
            break


    time.sleep(1)

    #datapoints_searchcode_box.send_keys(Keys.ENTER)
    # read out all data points existing for the selected facility and save them
    row_number = 0
    datapoint_list = []
    while True:
        row_id = "SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_PlaceHolder_ctl00_DescBrowsePanel_DescSearchGrid_SearchGrid_DXDataRow" + str(
            row_number)
        current_datapoint = driver.find_elements(By.ID, row_id)
        if len(current_datapoint) != 0:
            datapoint_code = str(current_datapoint[0].text).split("\n", 1)
            print(datapoint_code[0])
            datapoint_list.append([datapoint_code[0], current_datapoint[0]])
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
            #print(driver.find_element_by_xpath(str("//*[@id='" + row_id + "']/td[1]")).text)
            if driver.find_element_by_xpath(str("//*[@id='" + row_id + "']/td[1]")).text == "Datenpunkt":
                datapoint = driver.find_element_by_xpath(str("//*[@id='" + row_id + "']/td[2]"))
                datapoint_drop_location_xpath = str("//*[@id='" + row_id + "']/td[6]")
                datapoint_code = datapoint.text
                #print(datapoint)
                for code in codes_to_replace:
                    datapoint_code = datapoint_code.replace(code, "")
                #print(datapoint)
                diagram_datapoint_list.append([datapoint_code, datapoint, datapoint_drop_location_xpath])
            row_number += 1
        else:
            break

    actionChains = ActionChains(driver)
    for diagram_datapoint in diagram_datapoint_list:
        existing = False
        for datapoint in datapoint_list:
            if str("EWU.004" + diagram_datapoint[0]) == datapoint[0]:
                # TODO
                # drag and drop elements
                print(diagram_datapoint[0])
                print(datapoint[0])
                #print(diagram_datapoint[2])
                print(datapoint[1])
                actionChains = ActionChains(driver)
                actionChains.drag_and_drop(datapoint[1], driver.find_element_by_xpath(diagram_datapoint[2])).perform()
                existing = True
                time.sleep(1)
                break

    driver.find_element_by_id("SplitMain_ContentPlaceHolderBodyRight_ContentTabControl_ContentTabCallBackPanel_ContentPanel_ctl07_DashCallback_Content_ctl00_DashSettingsCallbackPanel_DashSettingsCollapsiblePanel_ctl00_DashSettingsToolbar_commitSettings").click()
    checkIfWindowIsClosed(driver)



if __name__ == "__main__":
    init()



