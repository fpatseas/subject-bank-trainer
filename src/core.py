import chromedriver_autoinstaller

from selenium import webdriver
from time import sleep

def main():
    driver = webdriver.Chrome()

    driver.get('https://trapeza.iep.edu.gr/public/subjects.php')
    sleep(2)