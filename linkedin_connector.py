{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 from selenium import webdriver\
from selenium.webdriver.common.by import By\
from selenium.webdriver.support.ui import WebDriverWait\
from selenium.webdriver.support import expected_conditions as EC\
from selenium.webdriver.chrome.options import Options\
from webdriver_manager.chrome import ChromeDriverManager\
from selenium.webdriver.chrome.service import Service\
import time\
import random\
from datetime import datetime\
\
class LinkedInConnector:\
    def __init__(self, email, password, headless=True):\
        self.email = email\
        self.password = password\
        self.headless = headless\
        self.driver = None\
        self.is_logged_in = False\
    \
    def setup_driver(self):\
        """Setup Chrome driver with options"""\
        chrome_options = Options()\
        if self.headless:\
            chrome_options.add_argument("--headless")\
        chrome_options.add_argument("--no-sandbox")\
        chrome_options.add_argument("--disable-dev-shm-usage")\
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")\
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])\
        chrome_options.add_experimental_option('useAutomationExtension', False)\
        \
        # Add user agent\
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")\
        \
        service = Service(ChromeDriverManager().install())\
        self.driver = webdriver.Chrome(service=service, options=chrome_options)\
        \
        # Execute script to hide webdriver property\
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', \{get: () => undefined\})")\
    \
    def login(self):\
        """Login to LinkedIn"""\
        if not self.driver:\
            self.setup_driver()\
        \
        try:\
            self.driver.get("https://www.linkedin.com/login")\
            \
            # Wait for page to load\
            WebDriverWait(self.driver, 10).until(\
                EC.presence_of_element_located((By.ID, "username"))\
            )\
            \
            # Enter credentials\
            username_field = self.driver.find_element(By.ID, "username")\
            password_field = self.driver.find_element(By.ID, "password")\
            \
            username_field.send_keys(self.email)\
            time.sleep(random.uniform(1, 3))\
            password_field.send_keys(self.password)\
            time.sleep(random.uniform(1, 3))\
            \
            # Click login button\
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")\
            login_button.click()\
            \
            # Wait for redirect to feed\
            WebDriverWait(self.driver, 15).until(\
                EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Start a post')]"))\
            )\
            \
            self.is_logged_in = True\
            print("Successfully logged into LinkedIn")\
            return True\
            \
        except Exception as e:\
            print(f"LinkedIn login failed: \{e\}")\
            return False\
    \
    def post_update(self, content):\
        """Post an update to LinkedIn"""\
        if not self.is_logged_in and not self.login():\
            return \{'success': False, 'error': 'Login failed'\}\
        \
        try:\
            # Navigate to feed if not already there\
            self.driver.get("https://www.linkedin.com/feed/")\
            \
            # Wait for and click "Start a post" button\
            start_post_button = WebDriverWait(self.driver, 10).until(\
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Start a post')]"))\
            )\
            start_post_button.click()\
            \
            # Wait for modal to open and find text area\
            text_area = WebDriverWait(self.driver, 10).until(\
                EC.presence_of_element_located((By.XPATH, "//div[@role='textbox']"))\
            )\
            \
            # Clear and enter content\
            text_area.clear()\
            time.sleep(1)\
            text_area.send_keys(content)\
            \
            # Wait a moment for content to register\
            time.sleep(3)\
            \
            # Find and click Post button\
            post_button = WebDriverWait(self.driver, 10).until(\
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Post')]"))\
            )\
            \
            # Scroll to make sure button is visible\
            self.driver.execute_script("arguments[0].scrollIntoView();", post_button)\
            time.sleep(1)\
            \
            post_button.click()\
            \
            # Wait for post to be submitted\
            time.sleep(5)\
            \
            return \{\
                'success': True,\
                'post_id': f"linkedin_\{int(time.time())\}",\
                'timestamp': datetime.now().isoformat()\
            \}\
            \
        except Exception as e:\
            print(f"LinkedIn posting failed: \{e\}")\
            return \{'success': False, 'error': str(e)\}\
    \
    def close(self):\
        """Close the browser"""\
        if self.driver:\
            self.driver.quit()}