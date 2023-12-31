# LMPH WEB SCRAPING EXAM USING PYTHON 3

## General Requirements:
The requirement is to scrape the contents of the Job page of Legalmatch PH, https://legalmatch.ph, for the following information
- Job positions/roles
- General description of the role/position
- Apply link
- Job details information
  - responsibilities
  - requirements
  - raw paragraph of relevant entire details page
  
The requirement is to code the scraper using PYTHON 3. As much as possible, unless otherwise
demonstrated/proven impractical or semi-impossible for the exam duration, the scraping
tool should run on command line and headless.
The scraped-off information should be in XLS format.

## Prerequisites:
1. Clone the repo:
```
git clone https://github.com/ryanvalmoria/lm-scraping-python.git
```

2. Make sure you have Python 3 installed in your computer
```
sudo apt update
sudo apt install python3
sudo apt install python3-pip

```

3. Install Selenium - used to interact with a webpage in a dynamic way
```
sudo pip3 install selenium
```

4. Install BeautifulSoup - used for parsing html / xml files
```
sudo apt install python3-bs4
```

5. Install Pandas - used for saving the scraped data into an excel file
```
sudo apt-get install python3-pandas
```


## Running the script:
To run the web scraping script in terminal or command line:
```
python3 scraper.py
```
In the root directory, you can find the scraped data in:
```
lmphJobsPython.xlsx
```
Sample result:
![image](https://github.com/ryanvalmoria/lm-scraping-python/assets/149349681/bca8176a-a338-4e5c-b283-aad156361a7c)

