import time
import getpass
import argparse

from selenium                       import webdriver
from selenium.webdriver.common.by   import By
from selenium.webdriver.support.ui  import WebDriverWait
from selenium.common.exceptions     import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support     import expected_conditions as EC

def check_exists_by_xpath(xpath):
    try:
        element = driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return None
    return element

def check_exists_by_css(selector):
    try:
        element = driver.find_element_by_css_selector(selector)
    except NoSuchElementException:
        return None
    return element

def connect_to_facebook(driver, args, strpswd):
    driver.get('https://www.facebook.com/')
    mail = check_exists_by_xpath('//*[@id="email"]')
    passwd = check_exists_by_xpath('//*[@id="pass"]')
    mail.send_keys(args.email)
    passwd.send_keys(strpswd)
    connectbutton = driver.find_element_by_id('loginbutton').click()

def connect_to_ticketswap(driver, args, strpswd):
    driver.get('https://www.ticketswap.fr')
    login = check_exists_by_xpath("//button[contains(text(),'Connecte-toi')]")
    if login:
        login.click()
        time.sleep(2)
        facebookclick = check_exists_by_xpath("//button[contains(text(),'Se connecter avec Facebook')]")
        print(facebookclick)
        facebookclick.click()

    time.sleep(10)
    login = check_exists_by_xpath("//button[contains(text(),'Connecte-toi')]")
    if not login:
        print("Login success")
        return True
    else:
        print("ERROR: Can't connect, retry")
        return False

def checktickt(driver, link):
    end = False
    counter = 0

    while not end:
        driver.get(link)
        driver.execute_script("window.scrollTo(0, 400)")
        #time.sleep(1)
        dispo = check_exists_by_xpath("//h2[contains(text(),'Disponible')]")
        if dispo:
            if dispo.text == "Disponible":
                linklist = []
                linksele = check_exists_by_xpath('//*[@id="__next"]/div[2]/div[3]/div[1]/ul')
                if linksele:
                    items = linksele.find_elements_by_tag_name("a")
                    for item in items:
                        if "Billets officiels en vente" not in item.text:
                            linklist.append(item.get_attribute('href'))

                    for link in linklist:
                        driver.get(link)
                        try:
                            buttonbuy = check_exists_by_xpath("//button[contains(text(),'Acheter un e-billet')]")
                            print(buttonbuy)
                            buttonbuy.click()
                        except Exception as e:
                            print (e)

                    driver.get('https://www.ticketswap.fr/cart')
                    end = True
        else:
            print ("PAS DE TICKET, nombre de cycle:" + str(counter))
        counter += 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('email', metavar='e',
                        help='facebook email')
    parser.add_argument('link', metavar='l',
                        help='ticketswap link')
    args = parser.parse_args()
    strpswd = getpass.getpass('Facebook password:')
    driver = webdriver.Chrome('./chromedriver')  # Optional argument, if not specified will search path.
    connect_to_facebook(driver, args, strpswd)
    connect = False
    while not connect:
        connect = connect_to_ticketswap(driver, args, strpswd)
    checktickt(driver, args.link)