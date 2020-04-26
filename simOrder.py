from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from random import randint


locationToSend = str(
    input("What's the postcode of the address you'd like to send to? "))
locationToSend = locationToSend.upper()
while True:
    if re.findall("[A-Z]{1,2}[0-9][A-Z0-9]? [0-9][ABD-HJLNP-UW-Z]{2}", locationToSend):
        postcodeIn = locationToSend
        doorNumber = str(input("Door Number? "))
        break
    else:
        print("Not a valid choice")
        locationToSend = input(
            "What's the postcode of the address you'd like to send to? ")

with open('first-names.txt') as f:
    nameListLines = [line.rstrip() for line in f]


noOfSims = int(input("How many SIM cards do you want ordered? "))


def checkThreeSims():
    try:
        while "3" not in simcountElem.get_attribute("innerHTML"):
            addSim = WebDriverWait(
                browser, 10).until(
                EC.presence_of_element_located(
                    (By.ID, "siminc")))
            addSim.click()
            simcountElem = WebDriverWait(
                browser, 10).until(
                EC.presence_of_element_located(
                    (By.ID, "simcount")))
            time.sleep(5)
    except BaseException:
        print("Error occurred when trying to add sim to basket")


def mainOrderFunc():
    firstNameIn = nameListLines[randint(0, 4000)]
    secondNameIn = nameListLines[randint(0, 4000)]

    emailIn = str(firstNameIn + secondNameIn +
                  str(randint(2, 80)) + "@gmail.com")

    print(
        "Your name is " +
        firstNameIn,
        secondNameIn,
        "and your email is " +
        emailIn)
    print("Launching Chrome!")

    browser = webdriver.Chrome('./chromedriver')
    browser.get("https://www.lycamobile.co.uk/")
    time.sleep(2)

    orderNewSimHref = WebDriverWait(
        browser, 20).until(
        EC.presence_of_element_located(
            (By.LINK_TEXT, "Order New SIM")))
    orderNewSimHref.click()

    time.sleep(3)

    try:
        firstName1 = browser.find_element_by_id('input_2_1')
    except BaseException:
        time.sleep(3)
        firstName1 = browser.find_element_by_id('input_2_1')

    lastName1 = browser.find_element_by_id('input_2_2')
    email1 = browser.find_element_by_id('input_2_3')
    firstName1.send_keys(firstNameIn)
    lastName1.send_keys(secondNameIn)
    email1.send_keys(emailIn)
    # browser.set_window_size(240, 1000)
    browser.execute_script('getBuySimData()')

    print("Data Entered! Waiting 5 seconds for page to load")
    time.sleep(5)

    try:
        simcountElem = WebDriverWait(
            browser, 10).until(
            EC.presence_of_element_located(
                (By.ID, "simcount")))
    except BaseException:
        time.sleep(5)
        print("Sleeping for 5 since simcountElem could not be located")
        simcountElem = WebDriverWait(
            browser, 10).until(
            EC.presence_of_element_located(
                (By.ID, "simcount")))

    # try:
    #     checkThreeSims()
    # except:
    #     print("Failed on checkThreeSims(), sleeping")
    #     time.sleep(3)
    #     checkThreeSims()

    def afterSimSelect(isWorkaround):
        if not isWorkaround:
            print("Ticking Terms & Conditions box and proceeding")
        try:
            termsAndConditionsTick = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.ID, "terms_conditions")))
            termsAndConditionsTick.click()
        except BaseException:
            time.sleep(5)
            print("terms and conditions failed to aquire, trying again")
            termsAndConditionsTick = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.ID, "terms_conditions")))
            termsAndConditionsTick.click()

        browser.execute_script("nc_newsim_open_tab1('address','fid','sid')")

        time.sleep(4)

        postcode = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.ID, "postCodes")))
        postcode.send_keys(postcodeIn)
        browser.execute_script('findAddress()')
        if not isWorkaround:
            print(
                "Locating " +
                locationToSend)

        time.sleep(3)
        try:
            selectAddressfromList = browser.find_element(
                By.ID, 'select-country-selectized')
            selectAddressfromList.click()

            typeIntoAddress = browser.find_element(
                By.ID, "select-country-selectized")
            typeIntoAddress.send_keys(doorNumber + Keys.ENTER)
        except:
            address1Form = browser.find_element_by_id("houseNo")
            address2Form = browser.find_element_by_id("suburb")
            address3Form = browser.find_element_by_id("state")
            address4Form = browser.find_element_by_id("city")



        time.sleep(2)
        billingSameShipping = browser.find_element(By.ID, 'same_as_billing')
        billingSameShipping.click()

        if not isWorkaround:
            print("Removing Captcha")
        captcha = browser.find_element(By.ID, "free_sim_captcha")

        browser.execute_script("""
        var element = arguments[0];
        element.parentNode.removeChild(element);
        """, captcha)

        time.sleep(1)

        # print("DEBUG: About to confirm!")
        browser.execute_script("nc_newsim_open_tab2('payment','sid','tid')")

    afterSimSelect(False)

    time.sleep(7)

    try:
        weirdReset = browser.find_element(
            By.XPATH, "//*[@id=\"order\"]/div/div[1]/div[1]/div[2]/div[1]/h4")
        print("Soft block detected! Will reenter data")
        addSim = WebDriverWait(
            browser, 10).until(
            EC.presence_of_element_located(
                (By.ID, "siminc")))
        addSim.click()
        time.sleep(5)
        afterSimSelect(True)
        print("Ordered! teehee so naughty")
        time.sleep(2)
        browser.close()

    except BaseException:
        print("Ordered! teehee so naughty")
        time.sleep(2)
        browser.close()


for i in range(0, noOfSims):
    print("Sim Number: " + str(i + 1))
    mainOrderFunc()

print("All done! Now go get that yummy food >:)")
