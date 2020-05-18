import time
import os
import selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains


# checks if the main window is closed in an defined interval
# script is effectively paused when this method is called until the window is closed
def checkIfWindowIsClosed(driver):
    while True:
        try:
            whandle = driver.window_handles
            time.sleep(0.2)
        except selenium.common.exceptions.WebDriverException:
            print("Chrome Window closed")
            exit(1)


#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC

# waits for an element to be climbable
# length : time the function waits
# search_type : describes the method that will be used to find the element (example: BY.ID)
# search value : value to find the element
def waitForElement(driver, length, search_type, search_value):
    try:
        WebDriverWait(driver, length).until(
            EC.element_to_be_clickable((search_type, search_value))
        )
    except selenium.common.exceptions.TimeoutException:
        print("could not find element in time")
        return False
    return True


#cheks if a web elment exist
#returns True if it exist, otherwise false
def check_existence(driver, search_type, search_value):
    try:
        driver.find_element(search_type, search_value)
    except selenium.common.exceptions.NoSuchElementException:
        return False
    return True

#loads the standard overview page and resets everything to the standard
#can be used to ensure that the starting position for any function is right
def go_to_ChartPage(driver):
    driver.get("https://ewus.eneffco.de/ChartPage.aspx")
    waitForElement(driver, 10 , By.XPATH, "// *[ @ id = 'SplitMain_0_CC'] / table / tbody / tr / td[4]")
    driver.find_element_by_xpath("// *[ @ id = 'SplitMain_0_CC'] / table / tbody / tr / td[4]").click()
    waitForElement(driver, 10, By.ID, "SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderTabs_AT0")

    #closes the active diagram tab, should it exist
    tab_control = driver.find_elements_by_id("SplitMain_ContentPlaceHolderBodyRight_ContentTabControl_ContentTabCallBackPanel_ContentTab_AT1")
    if len(tab_control) > 0:
        tab_control[0].find_element_by_xpath(".//table/tbody/tr/td[3]").click()

    try:
        driver.find_element_by_id("SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderTabs_T0").click()
        wait_loading_finished(driver, 1)
    except selenium.common.exceptions.ElementNotInteractableException:
        driver.find_element_by_id('SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_PlaceHolder_ctl00_InstTreeDisplayCollapsiblePanel_InstTreeDisplay_DXSE_I').clear()
        return
    driver.find_element_by_id('SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_PlaceHolder_ctl00_InstTreeDisplayCollapsiblePanel_InstTreeDisplay_DXSE_I').clear()


def wait_and_reload(driver, length, reload_times, search_type, search_value):
    i = 1
    while i <= reload_times:
        if not waitForElement(driver, length, search_type, search_value):
            driver.get("https://ewus.eneffco.de/ChartPage.aspx")
            time.sleep(0.5)
            continue
        else:
            print("element Found")
            return True
    #TODO
    # throw element not found exception
    print("could not find elmenet after " + i + " reload times")
    driver.quit()
    return False

#waits until a file is completle downloaded
#waits a maximum of 10 seconds
def download_wait(path_to_downloads, filename):
    seconds = 0
    dl_wait = True
    while dl_wait and seconds < 10:
        time.sleep(1)
        dl_wait = False
        for fname in os.listdir(path_to_downloads):
            if fname.endswith(filename):
                return True
        seconds += 1
    return False

#waits for all the loading elements to be not displayed (which means that all elements of the website will be fully loaded)
#time_before_start: this time will be waited before checking for loading signs the first time
# if after 15 seconds the side hasn't fully loaded it will return false
def wait_loading_finished(driver, time_before_start):
    time.sleep(3)
    seconds = 0
    loading_finished = True
    try:
        while seconds < 15:
            print("loading")
            loading_finished = True
            loading_elements = driver.find_elements_by_class_name("dxpnlLoadingPanelWithContent_EnEffCo")
           #print(len(loading_elements))
            for element in loading_elements:
                if element.value_of_css_property("position") == "absolute":
                    loading_finished = False
            if loading_finished:
                return True
            time.sleep(1)
            seconds += 1
        return False
    except selenium.common.exceptions.StaleElementReferenceException:
        return wait_loading_finished(driver, 2)

# searches all entry in the evaluatin tab for a diagram with the name "diagram_name"
# the browser need to be in the evaluation tab before the function is called
# ignores public diagrams
# return: the corresponding web element if successful, else None
def find_diagram_in_evaluation_tab(driver, diagram_name):
    evaluation_tab = driver.find_element_by_xpath(".//*[@id = 'SplitMain_ContentPlaceHolderBodyRight_ContentTabControl_ContentTabCallBackPanel_ContentPanel_ctl07_InstContentPanel_InstFolderDisplay_InstFolderDisplayCP_collapsiblePanel_content']/div[1]")
    i = 1
    while True:
        print(i)
        diagram = evaluation_tab.find_elements_by_xpath(".//div[" + str(i) + "]/div[2]/span")
        if len(diagram) == 0:
            return None
        if len(evaluation_tab.find_elements_by_xpath(".//div[" + str(i) + "]/div[1]/img[2]")) > 0:
            print("private")
            if diagram[0].text == diagram_name:
                return diagram[0]
        i += 1



