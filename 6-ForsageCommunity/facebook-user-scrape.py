#!/usr/bin/env python3

import requests
import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import csv
import random
import sys
import math


counter = 0
with open("forsageinformationgroup.json", "r") as f:
    with open("forsageinformationgroup.csv","a") as f2:
        csvwriter = csv.writer(f2)
        links = json.loads(f.read())
        ff_user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0"
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", ff_user_agent)
        driver = webdriver.Firefox(profile)
        driver.get("https://m.facebook.com/login")
        if "Log into Facebook" in driver.title:
                print("Session invalid, logging in")
                login_field = driver.find_element_by_id("m_login_email")
                login_field.clear()
                login_field.send_keys("lolnicetry")
                pass_field = driver.find_element_by_name("pass")
                pass_field.clear()
                pass_field.send_keys("lolnicetry")
                login_field.send_keys(Keys.RETURN)
                time.sleep(3)
        for link in links:
            if counter % 5 == 0 or random.random() > 0.8:
                time.sleep(10 + random.random() * 20)
                driver.execute_script("window.scrollTo(0, {})".format(math.floor(random.random()*1000)))
                time.sleep(10 + random.random() * 20)
            person_name = ""
            gender = ""
            location = ""
            userid = link.split("user/")[1]
            userid = userid[:-2]
            print("Starting link ", counter, " user id ", userid)
            desired_url_string = "https://m.facebook.com/profile.php?id={}&sk=about".format(userid)
            driver.get(desired_url_string)
            if "Log into Facebook" in driver.title:
                print("Session invalid, logging in")
                login_field = driver.find_element_by_id("m_login_email")
                login_field.clear()
                login_field.send_keys("lolnope")
                pass_field = driver.find_element_by_name("pass")
                pass_field.clear()
                pass_field.send_keys("stillnothappeninglol")
                login_field.send_keys(Keys.RETURN)
                time.sleep(3)
            if "Log into Facebook" in driver.title:
                raise RuntimeException("can't seem to log in")
            if "You Can't Use This Feature Right Now" in driver.title:
                print("Rate limited. send halp, going to sleep for an hour")
                time.sleep(4510)
                driver.get(desired_url_string)
                if "You Can't Use This Feature Right Now" in driver.title:
                    raise RuntimeException("Rate limited even after waiting an hour. Abort")
            if "Error" in driver.title:
                print("Facebook 500 error? hmm")
                time.sleep(65)
                driver.get(desired_url_string)
                if "Error" in driver.title:
                    raise RuntimeException("Errors abound, needs manual checking")
            if "The page you requested cannot be displayed right now. It may be temporarily unavailable, the link you clicked on may be broken or expired, or you may not have permission to view this page." in driver.page_source or "Content Not Found" in driver.title:
                print("User deleted profile")
                counter +=1 
                time.sleep(1.5)
                continue
            else:
                person_name = driver.title
                print(person_name)
                try:
                    basic_info_elem = driver.find_element_by_id("basic-info")
                    soup = BeautifulSoup(basic_info_elem.get_attribute('innerHTML'), 'html.parser')
                    if soup.get_text().find("Gender") > -1:
                        if soup.get_text().find("Male") > -1:
                            print("Found Male")
                            gender = "Male"
                        if soup.get_text().find("Female") > -1:
                            print("Found female")
                            gender = "Female"
                    if gender == "":
                        print("Something wierd going on with basic info, no gender found oh well")
                except NoSuchElementException:
                    print("can't find basic info no gender")

                try:
                    places_lived_elem = driver.find_element_by_id("living")
                    soup2 = BeautifulSoup(places_lived_elem.get_attribute('innerHTML'), 'html.parser')
                    print(soup2.get_text())
                    location = soup2.get_text()
                except NoSuchElementException:
                    print("can't find locations")

            csvwriter.writerow([userid, person_name, gender, location])
            driver.execute_script("window.scrollTo(0, {})".format(math.floor(random.random()*1000)))
            time.sleep(random.random() * 5)
            driver.execute_script("window.scrollTo(0, {})".format(math.floor(random.random()*1000)))
            # find some random page to jump to so we don't look like a bot
            num_times_to_bounce = math.floor(random.random() * 3 + 1)
            potential_links_to_click = [ "Profile", "Messages", "Notifications", "Friends", "Pages", "Groups(99)", "Menu", "Home", "Home", "Home"]
            for _ in range(0, num_times_to_bounce):
                roll = math.floor(random.random() * len(potential_links_to_click))
                clicky_link = driver.find_element_by_link_text(potential_links_to_click[roll])
                print("clicking link: ", potential_links_to_click[roll])
                clicky_link.click()
                time.sleep(1.5 + random.random() * 3.5)
                driver.execute_script("window.scrollTo(0, {})".format(math.floor(random.random()*1000)))
            counter += 1
