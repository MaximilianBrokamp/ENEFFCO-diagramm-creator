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
import os


def init_driver(url):
    options = webdriver.ChromeOptions()
    path = os.path.abspath('../downloads')
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


def get_all_plants():
    #TODO
    # write function
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

def main():
    diagram = load_config.load_config()
    driver = init_driver("https://ewus.eneffco.de/ChartPage.aspx")
    login(driver)

    #get_all_plants()
    #existing_diagrams = get_plants_with_exiting_diagram(driver, diagram.name)

    af.checkIfWindowIsClosed(driver)





if  __name__ == "__main__":
    main()
