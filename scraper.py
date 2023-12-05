from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup, Comment
import pandas as pd
 
# instantiate options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--no-sandbox")  # Disable sandbox for Linux
chrome_options.add_argument("--disable-dev-shm-usage")  # Disable shared memory usage
 
# instantiate driver 
driver = webdriver.Chrome(service=ChromeService( 
	ChromeDriverManager().install()), options=chrome_options) 
 
# load website 
url = 'https://legalmatch.ph/jobs/' 
 
# get the entire website content 
driver.get(url)
timeout = 5

# array declarations
jobTitles = []
jobDescriptions = []
jobLinks = []
jobResponsibilities = []
jobRequirements = []
rawDetails = []
  
# wait for the page to load first
try:
    element_present = EC.presence_of_element_located((By.CLASS_NAME, 'avail_post_list_ul'))
    WebDriverWait(driver, timeout).until(element_present)
except TimeoutException:
    print("Timed out waiting for page to load")
finally:
    print("Page loaded: " + url)

# parse using BeautifulSoup HTML parser library
soup = BeautifulSoup(driver.page_source, "html.parser")

#get all jobLinks first from main page
elements =  soup.select('.apply-btn-')
for element in elements:
    jobLinks.append(element['href']);

    #switch the driver to the new page url
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(element['href'])
    timeout = 5

    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'jobs-single__head'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load: " + element['href'])
        jobResponsibilities.append('N/A')
        jobRequirements.append('N/A')
    finally:
        print("NEW Page loaded: " + element['href'])

    new_soup = BeautifulSoup(driver.page_source, "html.parser")

    #remove first the Apply Button
    divRemove = new_soup.find_all('div', class_='jobs-single__btn')
    for div in divRemove:
        div.extract()


    #extract the job title and append to array
    jobTitle =  new_soup.find('h1', class_='jobs-single__title')
    if jobTitle:
        jobTitles.append(jobTitle.text)
    else:
        jobTitles.append('N/A')
        

    #extract the job description and append to array
    jobDescription = new_soup.find('div', class_='jobs-single__content')
    if jobDescription:
        # Find the first <p> element within the div
        first_p_element = jobDescription.find('p')
        if first_p_element:
            jobDescriptions.append(first_p_element.get_text(strip=True))
        else:
            jobDescriptions.append('N/A')
    else:
        jobDescriptions.append('N/A')
    

    #extract the raw details and append to array
    jobDetails =  new_soup.select('div.jobs-single__content')
    if jobDetails:
        for detail in jobDetails:
            # Remove the specified comment from the HTML content
            comment_to_remove = detail.find(string=lambda text: isinstance(text, Comment) and "?php endif; ?" in text)
            if comment_to_remove:
                comment_to_remove.extract()

        rawDetails.append(jobDetails)
    else:
        rawDetails.append('N/A')


    #extract the requirements
    #Find all ul tags within the identified div
    for detail in jobDetails:
        ul_tags_within_div = detail.find_all('ul')

        #if length is 2, meaning the structure is 1 ul for responsibilities and 1 ul for requirements
        if len(ul_tags_within_div) == 2:
            jobResponsibilities.append(ul_tags_within_div[0])
            jobRequirements.append(ul_tags_within_div[1])
        else:
            jobResponsibilities.append('N/A')
            jobRequirements.append('N/A')


driver.quit()

#print(len(jobTitles), len(jobDescriptions), len(jobLinks), len(jobResponsibilities), len(jobRequirements), len(rawDetails))
df = pd.DataFrame({'Job Title': jobTitles, 'Job Description': jobDescriptions, 'Job Links': jobLinks, 'Job Responsibilities': jobResponsibilities, 'Job Requirements': jobRequirements, 'Raw Details': rawDetails})
df.to_excel('lmphJobsPython.xlsx', index=False)
print(df)