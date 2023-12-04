from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pandas as pd
 
# instantiate options 
options = webdriver.ChromeOptions() 
 
# run browser in headless mode 
options.headless = True 
 
# instantiate driver 
driver = webdriver.Chrome(service=ChromeService( 
	ChromeDriverManager().install()), options=options) 
 
# load website 
url = 'https://legalmatch.ph/jobs/' 
 
# get the entire website content 
driver.get(url)
timeout = 5

jobTitles = []
jobDescriptions = []
jobLinks = []
  

try:
    element_present = EC.presence_of_element_located((By.CLASS_NAME, 'avail_post_list_ul'))
    WebDriverWait(driver, timeout).until(element_present)
except TimeoutException:
    print("Timed out waiting for page to load")
finally:
    print("Page loaded")


soup = BeautifulSoup(driver.page_source, "lxml")

#get all jobTitles
elements =  soup.select('.job_list_title_cont label')
for element in elements:
    jobTitles.append(element.text);
    print(element.text, end="\n")

#get jobDescriptions
elements =  soup.select('.job-description-text')
for element in elements:
    jobDescriptions.append(element.text);
    print(element.text, end="\n")

#get all jobLinks
elements =  soup.select('.apply-btn-')
for element in elements:
    jobLinks.append(element['href']);
    print(element['href'], end="\n")
    # parent_window = driver.current_window_handle
    # driver.execute_script('window.open(arguments[0]);', element['href'])
    # all_windows = driver.window_handles
    # child_window = [window for window in all_windows if window != parent_window][0]
    # driver.switch_to.window(child_window)
    # timeout = 5

   


    # try:
    #     element_present = EC.presence_of_element_located((By.CLASS_NAME, 'js-job-single'))
    #     WebDriverWait(driver, timeout).until(element_present)
    # except TimeoutException:
    #     print("Timed out waiting for page to load")
    # finally:
    #     print("NEW Page loaded")

    # new_soup = BeautifulSoup(driver.page_source, "lxml")
    # headings =  new_soup.select('h1.jobs-single__title')
    # print("ryan start -----")
    # for h in headings:
    #     print(h)
    
    # print("ryan end -----")
 


driver.quit()


df = pd.DataFrame({'jobTitle': jobTitles, 'jobDescription': jobDescriptions, 'jobLink': jobLinks})
df.to_csv('lmphJobsPython.csv', index=False);
print(df)