# Download and install anaconda https://www.anaconda.com/distribution/#download-section
# Download geckodriver https://github.com/mozilla/geckodriver/releases

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import csv
import pandas as pd
from pandas import DataFrame
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.interaction import KEY
from selenium.webdriver.common import keys

email = ""
password = ""
how_many_pages = 3
search_phrase = "Danylo"

try:
    profiles_file = pd.read_csv('linkedin.csv')
except FileNotFoundError:
    profiles_file = DataFrame([], columns=['link', 'message_sent'])
    profiles_file.to_csv('linkedin.csv', index = None, header=True)

print(profiles_file['link'])

driver = webdriver.Firefox(executable_path=r'C:\Program Files\Geckodriver\geckodriver.exe')


# Authorization

# Go to url
driver.get("https://www.linkedin.com/")

# find text in page title
assert "LinkedIn" in driver.title

# find input
elem = driver.find_element_by_name("session_key")
# clear text
elem.clear()
# type text
elem.send_keys(email)

elem = driver.find_element_by_name("session_password")
elem.clear()
elem.send_keys(password)

time.sleep(0.5)

# press enter
elem.send_keys(Keys.RETURN)

# assert "No results found." not in driver.page_source
# driver.close()

# Search
# elem = driver.find_element_by_class_name("search-global-typeahead__input")
# elem.clear()
# elem.send_keys(search_phrase)
# elem.send_keys(Keys.RETURN)
driver.get('https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B%22pt%3A7405%22%5D&origin=FACETED_SEARCH')

for i in range(0, how_many_pages):

    # Scroll down
    time.sleep(random.choice([1, 2, 3]))
    body = driver.find_element_by_css_selector('body')
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(random.choice([1, 2, 3]))
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(random.choice([1, 2, 3]))
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(random.choice([1, 2, 3]))
    body.send_keys(Keys.PAGE_DOWN)

    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Scroll up
    time.sleep(random.choice([1, 2, 3]))
    driver.execute_script("window.scrollTo(0, 0);")

    # Find links
    result = driver.find_elements_by_xpath('//a[@data-control-name="search_srp_result"]')
    # Itterate over every element
    for element in result:
        # And find profile link
        profile_link = element.get_attribute("href")
        if not profile_link in profiles_file.link.values:
            profiles_file = profiles_file.append({'link': profile_link, 'message_sent': 'no'}, ignore_index=True)

    # And go to next page
    element = driver.find_element_by_class_name("artdeco-pagination__button--next")
    element.click()
    try:
        driver.find_element_by_class_name('search-no-results__message-image')
        print('No results')
        driver.close()
        break
        # stop
    except NoSuchElementException:
        pass
        # repeat

for (index_label, row) in profiles_file.iterrows():
    if (row['message_sent'] == 'yes'):
        continue

    driver.get(row['link'])
    element = driver.find_element_by_class_name('artdeco-button--primary')
    body = driver.find_element_by_css_selector('body')
    body.send_keys(Keys.PAGE_DOWN)
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(random.choice([1, 2, 3]))
    element.click()

    try:
        invite_modal = driver.find_element_by_class_name('send-invite__actions')
        personal_message = invite_modal.find_element_by_class_name('artdeco-button--secondary')
        time.sleep(random.choice([1, 2, 3]))
        personal_message.click()
        time.sleep(random.choice([1, 2, 3]))

        text_area = driver.find_element_by_class_name('send-invite__custom-message')

        text_area.send_keys('test')
        time.sleep(random.choice([1, 2, 3]))  # random wait

        invite_modal = driver.find_element_by_class_name('modal-content-wrapper')
        button = invite_modal.find_elements_by_class_name('artdeco-button')[0]  # second button by index 1

        profiles_file.loc[index_label, 'message_sent'] = 'yes'

        button.click()  # finish
    except NoSuchElementException:
        driver.find_elements_by_class_name('msg-form__footer-action')[3].click()
        driver.find_elements_by_class_name('emoji-button')[0].click()

        time.sleep(random.choice([1, 2]))

        driver.execute_script("""
            var collection = document.getElementsByTagName('P');
            var elements = [];
            for(var i = 0; i < collection.length; i++) {
                if (collection[i].classList.length === 0) {
                    elements.push(collection[i]);
                }
            }
            elements[0].innerHTML = 'Ola';
            var evt = new KeyboardEvent('keydown', {'keyCode':65, 'which':65});
            document.dispatchEvent (evt);
        """)

        time.sleep(random.choice([1, 2]))

        search_bar = driver.find_element_by_class_name('msg-form__message-texteditor')
        actions = ActionChains(driver)
        actions.click(search_bar)
        actions.key_down(keys.Keys.SHIFT)
        actions.send_keys("a")
        actions.key_up(keys.Keys.SHIFT)
        # perform the operation on the element
        actions.perform()

        send_button = driver.find_element_by_class_name('msg-form__send-button')
        send_button.click()
        print('test')
    break

profile_file.to_csv('linkedin1.csv', index = None, header=True)

