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
jobResponsibilities = []
jobRequirements = []
rawDetails = []
  

try:
    element_present = EC.presence_of_element_located((By.CLASS_NAME, 'avail_post_list_ul'))
    WebDriverWait(driver, timeout).until(element_present)
except TimeoutException:
    print("Timed out waiting for page to load")
finally:
    print("Page loaded")


soup = BeautifulSoup(driver.page_source, "html.parser")

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

    #version 2
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(element['href'])
    timeout = 5


    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'jobs-single__head'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
        jobResponsibilities.append('N/A')
        jobRequirements.append('N/A')
    finally:
        print("NEW Page loaded")

    new_soup = BeautifulSoup(driver.page_source, "html.parser")

    #remove first the Apply Button
    divRemove = new_soup.find_all('div', class_='jobs-single__btn')
    for div in divRemove:
        div.extract()

    #extract the raw details and append to array
    jobDetails =  new_soup.select('div.jobs-single__content')
    rawDetails.append(jobDetails);


    #extract the requirements
    #Find all ul tags within the identified div
    for detail in jobDetails:
        ul_tags_within_div = detail.find_all('ul')

        if len(ul_tags_within_div) == 2:
            jobResponsibilities.append(ul_tags_within_div[0])
            jobRequirements.append(ul_tags_within_div[1])
        else:
            jobResponsibilities.append('N/A')
            jobRequirements.append('N/A')


driver.quit()

print(len(jobTitles), len(jobDescriptions), len(jobLinks), len(jobResponsibilities), len(jobRequirements), len(rawDetails))
df = pd.DataFrame({'Job Title': jobTitles, 'Job Description': jobDescriptions, 'Job Links': jobLinks, 'Job Responsibilities': jobResponsibilities, 'Job Requirements': jobRequirements, 'Raw Details': rawDetails})
df.to_excel('lmphJobsPython.xlsx', index=False);
print(df)