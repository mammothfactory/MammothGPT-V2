import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.options import Options
import requests # request img from web
import shutil # save img locally
import os

RESULT_FOLDER = 'Scraped_Images/sunnyportal'
chromeoption = Options()
# chromeoption.add_argument('--headless')
driver = webdriver.Chrome(options=chromeoption)

driver.maximize_window()
driver.get('https://www.sunnyportal.com/FixedPages/EnergyAndPower.aspx');

button_accept_cookie = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "onetrust-accept-btn-handler")))
button_accept_cookie.click()

text_email = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "txtUserName")))
text_email.send_keys('woody@pch.net')

text_password = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "txtPassword")))
text_password.send_keys('RuWiWoBe1?')

button_login = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_Logincontrol1_LoginBtn")))
button_login.click()

button_close = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "ctl00_ctl14_ConfirmTermsOfUse_GeneralMessageLinkButton")))
button_close.click()

button_previous_date = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_UserControlShowDashboard1_UserControlShowEnergyAndPower1_btn_prev")))
button_previous_date.click()

time.sleep(1)

current_day = driver.find_elements(By.ID, "ctl00_ContentPlaceHolder1_UserControlShowDashboard1_UserControlShowEnergyAndPower1__datePicker_textBox")

print(current_day[0].get_attribute('value'))
# with open("date.jpg", 'wb') as file:
#     div_graph = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
#         (By.ID, "ctl00_ContentPlaceHolder1_UserControlShowDashboard1_UserControlShowEnergyAndPower1__datePicker_textBox")))
#     file.write(div_graph.screenshot_as_png)



tab_day = driver.find_elements(By.ID, "ctl00_ContentPlaceHolder1_UserControlShowDashboard1_UserControlShowEnergyAndPower1_titel_Tab")
if not tab_day:

# try:
    tab_day = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_UserControlShowDashboard1_UserControlShowEnergyAndPower1_LinkButton_TabFront3")))
    tab_day.click()
# except:
#     time.sleep(0.1)
    # tab_day = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID,"ctl00_ContentPlaceHolder1_UserControlShowDashboard1_UserControlShowEnergyAndPower1_titel_Tab")))
    # tab_day.click()

time.sleep(1)
# with open('graph_image.png', 'wb') as file:
#     div_graph = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
#         (By.ID, "ctl00_ContentPlaceHolder1_UserControlShowDashboard1_UserControlShowEnergyAndPower1_DiagramDiv")))
#     file.write(div_graph.screenshot_as_png)

img = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_UserControlShowDashboard1_UserControlShowEnergyAndPower1_MouseoverMiddleImg")))
img.click()
time.sleep(1)
download_img = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "UserControlShowEnergyAndPower1$_diagram")))
src = download_img.get_attribute('src')
print(src)


yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
time.sleep(1)
res = requests.get(src, stream=True)
# time.sleep(5)
print(res.status_code)
time.sleep(1)
#
file_name = "sunnyportal_" + str(yesterday) + ".jpg"
file_name = os.path.join(RESULT_FOLDER, file_name)

if res.status_code == 200:
    with open(file_name, 'wb') as f:
        shutil.copyfileobj(res.raw, f)
    print('Image sucessfully Downloaded: ', file_name)
else:
    print('Image Downloaded By ID')
    with open(file_name, 'wb') as file:
        div_graph = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
            (By.ID, "zoomDiagramCont")))
        file.write(div_graph.screenshot_as_png)
    # zoomDiagramCont

button_close_image = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//td[@id='zoomDiagramCancel']//img[@src='/Images/cancel.png']")))
button_close_image.click()

time.sleep(1)

