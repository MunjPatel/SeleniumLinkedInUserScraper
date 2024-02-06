import time
import pandas as pd

from lxml import html
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from dataclasses import dataclass
from bs4 import BeautifulSoup

def initilize_driver():
    try:
        chrome_driver = webdriver.Chrome()
        return chrome_driver
    except Exception as e:
        print("Error while initiating the driver! Make sure you have chromedriver installed and present in cwd.")
        raise e
        
chrome_driver = initilize_driver()

class PLinkedInProfileScraper:
    def __init__(self, driver, first_name, last_name):
        self.driver = driver
        self.first_name = first_name
        self.last_name = last_name
    @staticmethod
    def find_element(li_element, tag, class_name):
        try:
            return li_element.find(tag, class_=class_name).get_text(strip=True)
        except:
            return ""
    @staticmethod
    def equalize_length(names, titles, locations, organizations, hyperlinks, max_length):
        names.extend([""]*(max_length-len(names)))
        titles.extend([""]*(max_length-len(titles)))
        locations.extend([""]*(max_length-len(locations)))
        organizations.extend([""]*(max_length-len(organizations)))
        hyperlinks.extend([""]*(max_length-len(hyperlinks)))
        return names, titles, locations, organizations, hyperlinks
    @staticmethod
    def extract_profile_url(li_element):
        try:
            profile_link = li_element.find('a', class_='base-card').get('href')
            return profile_link
        except:
            return ""
    def fetch_profiles(self):
        pprofile_scraper_instance = PLinkedInProfileScraper(driver = self.driver, first_name = self.first_name, last_name = self.last_name)
        try:
            format_url = f"https://www.linkedin.com/pub/dir?firstName={self.first_name}&lastName={self.last_name}"
            self.driver.get(format_url)
            self.driver.maximize_window()
            time.sleep(2)
            element = self.driver.find_element("xpath","""//*[@id="main-content"]/section/ul""").get_attribute("outerHTML")
            lxml_tree = html.fromstring(element)
            soup = BeautifulSoup(html.tostring(lxml_tree), "lxml")

            names, titles, locations, organizations, hyperlinks = [],[],[],[],[]
            li_elements = soup.find_all("ul")[0].find_all("li")
            
            for li in li_elements:
                names.append(pprofile_scraper_instance.find_element(li_element=li, tag="h3", class_name="base-search-card__title"))
                titles.append(pprofile_scraper_instance.find_element(li_element=li, tag="h4", class_name="base-search-card__subtitle"))
                locations.append(pprofile_scraper_instance.find_element(li_element=li, tag="p", class_name="people-search-card__location"))
                hyperlinks.append(pprofile_scraper_instance.extract_profile_url(li_element=li))
                try:
                    orgs = [org.get_text(strip = True) for org in li.select(".entity-list-meta .entity-list-meta__entities-list")]
                    organizations.append(orgs)
                except:
                    organizations.append("")
            max_len = max(len(names), len(titles), len(organizations), len(locations), len(hyperlinks))
            names, titles, locations, organizations, hyperlinks = pprofile_scraper_instance.equalize_length(names = names, titles = titles, locations = locations, organizations = organizations, hyperlinks = hyperlinks, max_length=max_len)
            data_dictionary = {
                "Name":names,
                "Profile":hyperlinks,
                "Title":titles,
                "Location":locations,
                "Organizations":organizations
            }
            profile_results = pd.DataFrame(data_dictionary)
            if profile_results.shape[0] >= 10:
                return profile_results.iloc[:10,:]
            elif (profile_results.shape[0] > 0 and profile_results.shape[0] < 10):
                return profile_results
            elif profile_results.shape == 0:
                print("No profiles found.")
        except Exception as e:
            raise e
        finally:
            chrome_driver.quit()

public_scraper_instance = PLinkedInProfileScraper(driver = chrome_driver, first_name = "Shreya", last_name = "Patel")
results = public_scraper_instance.fetch_profiles()
print(results)

results.to_excel("profile_results.xlsx", index=False)