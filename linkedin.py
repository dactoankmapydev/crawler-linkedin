import csv
import parameters
from parsel import Selector
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Operating in headless mode
driver = webdriver.Firefox()
url = 'https://www.linkedin.com'
driver.get(url)
sleep(3)

credential = open('credentials.txt')
line = credential.readlines()
email = line[0]
password = line[1]
sleep(2)

# locate email form by_class_name
email_field = driver.find_element_by_id('session_key')
# send_keys() to simulate key strokes
email_field.send_keys(email)
sleep(2)

# locate password form by_class_name
password_field = driver.find_element_by_id('session_password')
# send_keys() to simulate key strokes
password_field.send_keys(password)
sleep(2)

# locate submit button by_xpath
log_in_button = driver.find_element_by_class_name('sign-in-form__submit-button')

# .click() to mimic button click
log_in_button.click()
sleep(3)


# driver.get method() will navigate to a page given by the URL address
driver.get('https://www.google.com')
sleep(3)

# locate search form by_name
search = open('search.txt')
line = search.readlines()
search_query = line[0]
search_query = driver.find_element_by_name('q')

# send_keys() to simulate the search text key strokes
search_query.send_keys(search_query)
sleep(3)

# .send_keys() to simulate the return key
search_query.send_keys(Keys.RETURN)
sleep(3)

def GetURL():
    page_source = BeautifulSoup(driver.page_source, 'html.parser')
    sleep(3)
    profiles = page_source.find_all('div', class_ = 'yuRUbf')
    
    all_profile_URL = []
    for profile in profiles:
        for a in profile.find_all('a'):
            sleep(3)
            profile_URL = a.get('href')
            if profile_URL not in all_profile_URL:
                all_profile_URL.append(profile_URL)
    return all_profile_URL

URLs_all_page = []
for page in range(10):
    URLs_one_page = GetURL()
    sleep(3)
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') #scroll to the end of the page
    sleep(3)
    next_button = driver.find_element_by_xpath('//*[@id="pnnext"]')
    sleep(3)
    driver.execute_script("arguments[0].click();", next_button)
    URLs_all_page = URLs_all_page + URLs_one_page
    sleep(3)

with open('output.csv', 'w',  newline = '') as file_output:
    headers = ['Name', 'Job Title', 'Location', 'URL', 'Company']
    writer = csv.DictWriter(file_output, delimiter=',', lineterminator='\n',fieldnames=headers)
    writer.writeheader()
    for linkedin_URL in URLs_all_page:
        driver.get(linkedin_URL)
        print('- Accessing profile: ', linkedin_URL)
        sleep(3)
        page_source = BeautifulSoup(driver.page_source, "html.parser")
        info_div = page_source.find('div',{'class':'flex-1 mr5 pv-top-card__list-container'})
        info_company = page_source.find('ul',{'class':'pv-top-card--experience-list'})
        try:
            name = info_div.find('li', class_='inline t-24 t-black t-normal break-words').get_text().strip() #Remove unnecessary characters 
            print('--- Profile name is: ', name)

            location = info_div.find('li', class_='t-16 t-black t-normal inline-block').get_text().strip() #Remove unnecessary characters 
            print('--- Profile location is: ', location)

            title = info_div.find('h2', class_='mt1 t-18 t-black t-normal break-words').get_text().strip()
            print('--- Profile title is: ', title)

            company = info_div2.find('span', class_='text-align-left ml2 t-14 t-black t-bold full-width lt-line-clamp lt-line-clamp--multi-line ember-view').get_text().strip()
            print('--- Profile company is: ', company)

            writer.writerow({headers[0]:name, headers[1]:title, headers[2]:location, headers[3]:company, headers[4]:linkedin_URL})
            print('\n')
        except:
            pass

print('Mission Completed!')
