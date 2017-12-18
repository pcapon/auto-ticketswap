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

parser = argparse.ArgumentParser()
parser.add_argument('email', metavar='e',
                    help='facebook email')
parser.add_argument('link', metavar='l',
                    help='ticketswap link')
args = parser.parse_args()

strpswd = getpass.getpass('Facebook password:')


driver = webdriver.Chrome('./chromedriver')  # Optional argument, if not specified will search path.
driver.get('https://www.facebook.com/')
mail = check_exists_by_xpath('//*[@id="email"]')
passwd = check_exists_by_xpath('//*[@id="pass"]')
mail.send_keys(args.email)
passwd.send_keys(strpswd)
connectbutton = driver.find_element_by_id('loginbutton').click()

driver.get('https://www.ticketswap.fr')
login = check_exists_by_xpath('/html/body/div[1]/nav[2]/ul/li[2]/a')
if login:
    login.click()

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.main-navigation > nav.main-navigation--desktop > ul > li.user.dropdown"))
    )
finally:
    pass

link = args.link

while (True):
    driver.get(link)
    driver.execute_script("window.scrollTo(0, 400)")
    time.sleep(1)
    dispo = check_exists_by_xpath('/html/body/div[2]/div/div[1]/section[1]/h2')
    if dispo:
        if dispo.text == "Disponible":
            linksele = check_exists_by_css('body > div:nth-child(5) > div > div.container > section.listings > div > article > div.listings-item--title > h3 > a')
            if linksele:
                link = linksele.get_attribute('href')
                driver.get(link)
                button = check_exists_by_xpath('//*[@id="listing-reserve-form"]/input[3]')
                if button:
                    button.click()
                    raw_input("Ticket find Enter to continue..")
    else:
        print "PAS DE TICKET"
