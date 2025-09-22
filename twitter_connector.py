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
from selenium.webdriver.common.keys import Keys\
import time\
import random\
from datetime import datetime\
\
class TwitterConnector:\
    def __init__(self, email, password, username, headless=True):\
        self.email = email\
        self.password = password\
        self.username = username\
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
        """Login to Twitter"""\
        if not self.driver:\
            self.setup_driver()\
        \
        try:\
            self.driver.get("https://twitter.com/i/flow/login")\
            \
            # Wait for username/email field\
            username_field = WebDriverWait(self.driver, 10).until(\
                EC.presence_of_element_located((By.XPATH, "//input[@autocomplete='username']"))\
            )\
            \
            username_field.send_keys(self.email)\
            time.sleep(random.uniform(1, 3))\
            \
            # Click Next\
            next_button = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Next')]")\
            next_button.click()\
            \
            # Sometimes Twitter asks for username verification\
            try:\
                username_verification = WebDriverWait(self.driver, 5).until(\
                    EC.presence_of_element_located((By.XPATH, "//input[@data-testid='ocfEnterTextTextInput']"))\
                )\
                username_verification.send_keys(self.username)\
                next_button = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Next')]")\
                next_button.click()\
            except:\
                pass  # Username verification not required\
            \
            # Wait for password field\
            password_field = WebDriverWait(self.driver, 10).until(\
                EC.presence_of_element_located((By.XPATH, "//input[@name='password']"))\
            )\
            \
            password_field.send_keys(self.password)\
            time.sleep(random.uniform(1, 3))\
            \
            # Click Log in\
            login_button = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Log in')]")\
            login_button.click()\
            \
            # Wait for home timeline\
            WebDriverWait(self.driver, 15).until(\
                EC.presence_of_element_located((By.XPATH, "//div[@data-testid='tweetTextarea_0']"))\
            )\
            \
            self.is_logged_in = True\
            print("Successfully logged into Twitter")\
            return True\
            \
        except Exception as e:\
            print(f"Twitter login failed: \{e\}")\
            return False\
    \
    def post_tweet(self, content):\
        """Post a single tweet"""\
        if not self.is_logged_in and not self.login():\
            return \{'success': False, 'error': 'Login failed'\}\
        \
        try:\
            # Navigate to home if not already there\
            self.driver.get("https://twitter.com/home")\
            \
            # Wait for tweet compose box\
            tweet_box = WebDriverWait(self.driver, 10).until(\
                EC.presence_of_element_located((By.XPATH, "//div[@data-testid='tweetTextarea_0']"))\
            )\
            \
            # Click to focus and clear any existing content\
            tweet_box.click()\
            time.sleep(1)\
            \
            # Type content\
            tweet_box.send_keys(content)\
            time.sleep(2)\
            \
            # Find and click Tweet button\
            tweet_button = WebDriverWait(self.driver, 10).until(\
                EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='tweetButtonInline']"))\
            )\
            \
            tweet_button.click()\
            \
            # Wait for tweet to be posted\
            time.sleep(5)\
            \
            return \{\
                'success': True,\
                'tweet_id': f"twitter_\{int(time.time())\}",\
                'timestamp': datetime.now().isoformat()\
            \}\
            \
        except Exception as e:\
            print(f"Twitter posting failed: \{e\}")\
            return \{'success': False, 'error': str(e)\}\
    \
    def post_thread(self, tweets):\
        """Post a thread of tweets"""\
        if not self.is_logged_in and not self.login():\
            return \{'success': False, 'error': 'Login failed'\}\
        \
        thread_results = []\
        \
        for i, tweet_content in enumerate(tweets):\
            try:\
                if i == 0:\
                    # First tweet\
                    result = self.post_tweet(tweet_content)\
                else:\
                    # Reply to previous tweet\
                    # Navigate to home to continue thread\
                    self.driver.get("https://twitter.com/home")\
                    time.sleep(3)\
                    \
                    # Find tweet compose box for reply\
                    tweet_box = WebDriverWait(self.driver, 10).until(\
                        EC.presence_of_element_located((By.XPATH, "//div[@data-testid='tweetTextarea_0']"))\
                    )\
                    \
                    tweet_box.click()\
                    time.sleep(1)\
                    tweet_box.send_keys(tweet_content)\
                    time.sleep(2)\
                    \
                    # Click Tweet button\
                    tweet_button = WebDriverWait(self.driver, 10).until(\
                        EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='tweetButtonInline']"))\
                    )\
                    tweet_button.click()\
                    \
                    result = \{\
                        'success': True,\
                        'tweet_id': f"twitter_thread_\{int(time.time())\}_\{i\}",\
                        'position': i + 1\
                    \}\
                \
                thread_results.append(result)\
                \
                if not result.get('success'):\
                    break\
                    \
                # Small delay between tweets\
                time.sleep(3)\
                    \
            except Exception as e:\
                thread_results.append(\{\
                    'success': False,\
                    'error': str(e),\
                    'position': i + 1\
                \})\
                break\
        \
        return thread_results\
    \
    def close(self):\
        """Close the browser"""\
        if self.driver:\
            self.driver.quit()}