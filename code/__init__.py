import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pynput.keyboard import Key, Controller
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
    driver = webdriver.Chrome()
    driver.maximize_window()
    #driver.implicitly_wait(5)
    # Open the website
    driver.get('https://ewus.eneffco.de/ChartPage.aspx')
    login(driver)

    # quick test for creating a diagram
    search_facilities_box = driver.find_element_by_id(
        'SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_PlaceHolder_ctl00_InstTreeDisplayCollapsiblePanel_InstTreeDisplay_DXSE_I')
    search_facilities_box.send_keys('EWU.004')
    search_facilities_box.send_keys(Keys.ENTER)

    time.sleep(2)
    # the id describes the first entry in the search
    # the id for the first entry should stay the same no matter the input.
    facility_icon = driver.find_element_by_xpath(
        "// *[ @ id = 'SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_PlaceHolder_ctl00_InstTreeDisplayCollapsiblePanel_InstTreeDisplay_D'] / tbody/tr[3]")
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
    #change from button press to just klick enter
    waitForElement(driver, 15, By.XPATH, "html/body/div[3]/div[3]/div/button[1]")
    save_upload_button = driver.find_element_by_xpath("/html/body/div[3]/div[3]/div/button[1]")
    save_upload_button.click()

    waitForElement(driver, 30, By.ID , "SplitMain_ContentPlaceHolderBodyRight_ContentTabControl_ContentTabCallBackPanel_ContentPanel_ctl07_DashCallback_Content_ctl00_DashSettingsCallbackPanel_DashSettingsCollapsiblePanel_BindingsCollapsibelPanel_NamedRefCtrl_CBPanel_Grid_DXFREditorcol0_B-1")
    print("1")

    #waitForElement(driver, 10, By.ID , "SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderTabs_AT1")
    print("2")
    datapoints_button = driver.find_element_by_id("SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderTabs_AT1")
    datapoints_button = driver.find_element_by_xpath("//*[@id='SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderTabs_T1']/table/tbody/tr/td[2]")
    datapoints_button.click()

    waitForElement(driver, 10, By.ID, "SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_PlaceHolder_ctl00_DescBrowsePanel_DescSearchGrid_SearchGrid_DXFREditorcol0")
    datapoints_searchcode_box = driver.find_element_by_id("SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_PlaceHolder_ctl00_DescBrowsePanel_DescSearchGrid_SearchGrid_DXFREditorcol0")
    datapoints_searchcode_box.send_keys("EWU004")
    datapoints_searchcode_box.send_keys(Key.enter)
    checkIfWindowIsClosed(driver)


if __name__ == "__main__":
    init()
