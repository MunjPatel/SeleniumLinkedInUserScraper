import time
import pandas as pd
import streamlit as st

from lxml import html
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from dataclasses import dataclass
from bs4 import BeautifulSoup

def initilize_driver():
    try:
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        chrome_driver = webdriver.Chrome(options = options)
        return chrome_driver
    except Exception as e:
        print("Error while initiating the driver! Make sure you have chromedriver installed and present in cwd.")
        raise e
        
# chrome_driver = initilize_driver()

class PLinkedInProfileScraper:
    def __init__(self):
        self.driver = initilize_driver()

    @staticmethod
    def find_element(li_element, tag, class_name):
        try:
            return li_element.find(tag, class_=class_name).get_text(strip=True)
        except:
            return ""
    @staticmethod
    def equalize_length(names, titles, locations, hyperlinks, max_length):
        names.extend([""]*(max_length-len(names)))
        titles.extend([""]*(max_length-len(titles)))
        locations.extend([""]*(max_length-len(locations)))
        hyperlinks.extend([""]*(max_length-len(hyperlinks)))
        return names, titles, locations, hyperlinks
    @staticmethod
    def extract_profile_url(li_element):
        try:
            profile_link = li_element.find('a', class_='base-card').get('href')
            return profile_link
        except:
            return ""
    def fetch_profiles(self, pprofile_scraper_instance, first_name, last_name):
        # pprofile_scraper_instance = PLinkedInProfileScraper()
        try:
            format_url = f"https://www.linkedin.com/pub/dir?firstName={first_name}&lastName={last_name}"
            self.driver.get(format_url)
            self.driver.maximize_window()
            time.sleep(2)
            element = self.driver.find_element("xpath","""//*[@id="main-content"]/section/ul""").get_attribute("outerHTML")
            lxml_tree = html.fromstring(element)
            soup = BeautifulSoup(html.tostring(lxml_tree), "lxml")

            names, titles, locations, hyperlinks = [],[],[],[]
            li_elements = soup.find_all("ul")[0].find_all("li")
            
            for li in li_elements:
                names.append(pprofile_scraper_instance.find_element(li_element=li, tag="h3", class_name="base-search-card__title"))
                titles.append(pprofile_scraper_instance.find_element(li_element=li, tag="h4", class_name="base-search-card__subtitle"))
                locations.append(pprofile_scraper_instance.find_element(li_element=li, tag="p", class_name="people-search-card__location"))
                hyperlinks.append(pprofile_scraper_instance.extract_profile_url(li_element=li))

            max_len = max(len(names), len(titles), len(locations), len(hyperlinks))
            names, titles, locations, hyperlinks = pprofile_scraper_instance.equalize_length(names = names, titles = titles, locations = locations, hyperlinks = hyperlinks, max_length=max_len)
            data_dictionary = {
                "Name":names,
                "Profile":hyperlinks,
                "Title":titles,
                "Location":locations
            }
            profile_results = pd.DataFrame(data_dictionary)
            return profile_results
        except Exception as e:
            raise e
        finally:
            self.driver.quit()

profiles = PLinkedInProfileScraper()

profile_data = profiles.fetch_profiles(pprofile_scraper_instance=profiles, first_name="Munj", last_name="Patel")
print(profile_data)