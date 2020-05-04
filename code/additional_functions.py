import selenium
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


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
    waitForElement(driver, 10, By.ID, "SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderTabs_AT0")
    driver.find_element_by_id("SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderTabs_AT0").click()
    driver.find_element_by_id(
        'SplitMain_ContentPlaceHolderBodyLeft_FolderTabCtrl_FolderPanel_PlaceHolder_ctl00_InstTreeDisplayCollapsiblePanel_InstTreeDisplay_DXSE_I').clear()

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