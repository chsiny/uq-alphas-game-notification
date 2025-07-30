import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
import json
from datetime import datetime, timedelta
import pytz
from config import ULTRA_MSG_TOKEN, ULTRA_MSG_INSTANCE_ID, DEFAULT_PHONE_NUMBER, DEFAULT_GROUP_ID


def get_brisbane_timezone():
    """Get Brisbane timezone"""
    return pytz.timezone('Australia/Brisbane')

def get_current_brisbane_time():
    """Get current time in Brisbane timezone"""
    brisbane_tz = get_brisbane_timezone()
    return datetime.now(brisbane_tz)

def parse_game_date(date_text):
    """Parse the date text from the website and return a datetime object in Brisbane timezone"""
    try:
        # Remove "Round X" part if present
        date_text = date_text.split('\n')[0].strip()
        
        # Parse date like "THURSDAY 31ST JULY" (uppercase)
        # Extract day name, day number, and month
        parts = date_text.split()
        if len(parts) >= 3:
            day_name = parts[0]  # THURSDAY
            day_number = parts[1].replace('ST', '').replace('ND', '').replace('RD', '').replace('TH', '')  # 31
            month = parts[2]  # JULY
            
            # Convert month name to number (case insensitive)
            month_map = {
                'JANUARY': 1, 'FEBRUARY': 2, 'MARCH': 3, 'APRIL': 4,
                'MAY': 5, 'JUNE': 6, 'JULY': 7, 'AUGUST': 8,
                'SEPTEMBER': 9, 'OCTOBER': 10, 'NOVEMBER': 11, 'DECEMBER': 12
            }
            
            month_num = month_map.get(month, 1)
            day_num = int(day_number)
            
            # Get current Brisbane time to determine year
            current_brisbane = get_current_brisbane_time()
            current_year = current_brisbane.year
            
            # If we're past December, assume next year
            if month_num < current_brisbane.month:
                current_year += 1
                
            # Create datetime in Brisbane timezone
            brisbane_tz = get_brisbane_timezone()
            naive_datetime = datetime(current_year, month_num, day_num)
            brisbane_datetime = brisbane_tz.localize(naive_datetime)
            
            return brisbane_datetime
    except Exception as e:
        print(f"Error parsing date '{date_text}': {e}")
        return None
    return None


def get_next_game():
    url = "https://touchfootball.com.au/Competitions/Competition/s2-2025-thursday-girls-u15d-63174269?team=63354766"

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    # Initialize the driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Navigate to the page
        driver.get(url)

        # Wait for the page to load and Vue.js to render
        wait = WebDriverWait(driver, 10)

        # Wait for the match elements to appear
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.l-grid > li")))

        # Give extra time for Vue.js to fully render
        time.sleep(3)

        # Find all matches
        all_matches = driver.find_elements(By.CSS_SELECTOR, "ul.l-grid > li")
        
        if not all_matches:
            return None

        # Find the next upcoming game
        next_game = None
        current_date = get_current_brisbane_time()
        
        for match in all_matches:
            try:
                # Get date - try multiple selectors
                date_element = None
                try:
                    date_element = match.find_element(By.CSS_SELECTOR, ".match-header__title")
                except:
                    try:
                        date_element = match.find_element(By.CSS_SELECTOR, "[class*='header']")
                    except:
                        continue  # Skip this match if no date found
                
                if not date_element:
                    continue
                    
                date_text = date_element.text.strip()
                
                # Parse the date
                game_date = parse_game_date(date_text)
                if not game_date:
                    continue
                
                # Check if this game is in the future
                if game_date > current_date:
                    # Get teams
                    teams = match.find_elements(By.CSS_SELECTOR, ".match-team__name")
                    if not teams:
                        teams = match.find_elements(By.CSS_SELECTOR, ".team-name")
                    if not teams:
                        teams = match.find_elements(By.CSS_SELECTOR, "[class*='team']")

                    if len(teams) >= 2:
                        home_team = teams[0].text.strip()
                        away_team = teams[1].text.strip()

                        # Get time
                        time_element = match.find_element(By.TAG_NAME, "time")
                        time_text = time_element.text.strip()

                        # Get venue
                        venue_element = match.find_element(
                            By.CSS_SELECTOR, ".match-cta__link"
                        )
                        venue_text = venue_element.text.strip()

                        next_game = {
                            "date": date_text,
                            "time": time_text,
                            "home": home_team,
                            "away": away_team,
                            "venue": venue_text,
                            "game_date": game_date
                        }
                        break  # Found the next game, stop searching
                        
            except Exception as e:
                print(f"Error processing match: {e}")
                continue

        return next_game

    except Exception as e:
        print(f"Error loading page: {e}")
        return None

    finally:
        driver.quit()


def format_message(info):
    return f"""📅 *{info['date']}*
🕖 Kickoff: *{info['time']}*
🏉 *{info['home']}* vs *{info['away']}*
📍 Venue: *{info['venue']}*"""


def send_whatsapp_message(phone_number, message):
    """Send WhatsApp message using Ultramsg API"""
    # Ultramsg API configuration
    url = f"https://api.ultramsg.com/{ULTRA_MSG_INSTANCE_ID}/messages/chat"
    
    payload = {
        "token": ULTRA_MSG_TOKEN,
        "to": phone_number,
        "body": message
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            result = response.json()
            if result.get("sent"):
                print(f"✅ Message sent successfully to {phone_number}")
                return True
            else:
                print(f"❌ Failed to send message: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error sending WhatsApp message: {e}")
        return False


if __name__ == "__main__":
    print("Loading match data...")
    info = get_next_game()
    if info:
        msg = format_message(info)
        print(msg)

        # Send to group instead of individual number
        group_id = DEFAULT_GROUP_ID
        print("Sending WhatsApp message to group...")
        send_whatsapp_message(group_id, msg)

    else:
        print("⚠️ Could not find any upcoming game.")
