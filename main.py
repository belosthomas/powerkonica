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
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


KONICA_IP = "172.30.129.131:443"

def forward(username):
    global KONICA_IP

    KONICA_IP_bak = KONICA_IP
    KONICA_IP = "127.0.0.1:4433"
    system("ssh -N -L %s:%s %s@imagine2.enpc.fr" % (KONICA_IP_bak, KONICA_IP, username))
    print("Unable to forward. The script will only work when connected to eduroam or ENPC-PRO...")
    KONICA_IP = KONICA_IP_bak

def printPDF(path):
    global KONICA_IP

    print("Printing " + path)

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--ignore-certificate-errors")

    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)

    print("Loading page...")
    driver.get("https://" + KONICA_IP + "/wcd/spa_login.html")

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


def convertToPDF(path):
    err = system("lowriter --convert-to pdf " + path + " --outdir " + os.path.dirname(path))
    if err != 0:
        print("Error while converting to PDF")
        return
    os.remove(path)

if __name__ == '__main__':
    username = input("Imagine2 Username: ")
    x = threading.Thread(target=forward, args=(username,))
    x.start()

    printpath = os.path.join(Path.home(), "autoprint")

    os.makedirs(printpath, exist_ok=True)

    while True:
        for elem in os.listdir(printpath):
            if elem.endswith(".odt") or elem.endswith(".docx") or elem.endswith(".doc") or elem.endswith(".rtf") or elem.endswith(".txt"):
                convertToPDF(os.path.join(printpath, elem))
            elif elem.endswith(".pdf"):
                try:
                    fullpath = os.path.join(printpath, elem)
                    printPDF(fullpath)
                    os.remove(fullpath)
                except Exception as e:
                    print(e)
            else:
                print("Unknown file type: " + elem)

        sleep(1)


