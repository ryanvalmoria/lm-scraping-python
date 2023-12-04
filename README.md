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


1. Clone the repo:
```
git clone https://github.com/ryanvalmoria/lm-scraping-python.git
```

2. Make sure you have Python 3 installed in your computer
```
sudo apt update
sudo apt install python3
```

3. Install Selenium
```
npm install puppeteer
```

4. Install BeautifulSoup
```
npm install xlsx
```

5. Install Pandas
```
npm install
```



To run the web scraping script in terminal or command line:
```
python3 scraper.py
```
In the root directory, you can find the scraped data in:
```
lmphJobsPython.xlsx
```
