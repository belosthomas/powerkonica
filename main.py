import os
import threading
from os import system
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
from webdriver_manager.firefox import GeckoDriverManager

def forward():
    system("ssh -N -L 127.0.0.1:4433:172.30.129.131:443 belosth@imagine2.enpc.fr")

def printPDF(path):
    print("Printing " + path)

    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

    print("Loading page...")
    driver.get("https://127.0.0.1:4433/wcd/spa_login.html")

    print("Waiting for login page...")
    WebDriverWait(driver, 30).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "SPA-contents-body")))

    print("Fill login form...")
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "C_CTL_1"))).send_keys("964351")

    print("Click on login button...")
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "ID_LGI_LOGIN_BT"))).click()

    print("Waiting for home page...")
    WebDriverWait(driver, 30).until(EC.url_changes("https://127.0.0.1:4433/wcd/spa_main.html"))
    sleep(10)
    driver.get("https://127.0.0.1:4433/wcd/spa_main.html")

    print("Waiting for home page...")
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "ID_Menu_Print_DirectPrint"))).click()

    print("Waiting for print page...")
    WebDriverWait(driver, 30).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "SPA-contents-body")))

    print("Filling form...")
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "P7_F_FI"))).send_keys(path)

    print("Click on print button...")
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "ID_OK_P_PRI_SET"))).click()


if __name__ == '__main__':
    x = threading.Thread(target=forward)
    x.start()

    printpath = os.path.join(Path.home(), "autoprint")

    os.makedirs(printpath, exist_ok=True)

    while True:
        for elem in os.listdir(printpath):
            if True:
            #try:
                fullpath = os.path.join(printpath, elem)
                printPDF(fullpath)
                os.remove(fullpath)
            #except Exception as e:
            #    print(e)

        sleep(1)


