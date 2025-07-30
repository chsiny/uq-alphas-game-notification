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
from config import ULTRA_MSG_TOKEN, ULTRA_MSG_INSTANCE_ID, DEFAULT_PHONE_NUMBER, DEFAULT_GROUP_ID


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

        # Find the first match
        first_match = driver.find_element(By.CSS_SELECTOR, "ul.l-grid > li")

        # Extract match information
        try:
            # Get date
            date_element = first_match.find_element(
                By.CSS_SELECTOR, ".match-header__title"
            )
            date_text = date_element.text.strip()

            # Get teams - try multiple selectors
            teams = first_match.find_elements(By.CSS_SELECTOR, ".match-team__name")
            if not teams:
                teams = first_match.find_elements(By.CSS_SELECTOR, ".team-name")
            if not teams:
                teams = first_match.find_elements(By.CSS_SELECTOR, "[class*='team']")

            if len(teams) < 2:
                return None

            home_team = teams[0].text.strip()
            away_team = teams[1].text.strip()

            # Get time
            time_element = first_match.find_element(By.TAG_NAME, "time")
            time_text = time_element.text.strip()

            # Get venue
            venue_element = first_match.find_element(
                By.CSS_SELECTOR, ".match-cta__link"
            )
            venue_text = venue_element.text.strip()

            return {
                "date": date_text,
                "time": time_text,
                "home": home_team,
                "away": away_team,
                "venue": venue_text,
            }

        except Exception as e:
            print(f"Error extracting match data: {e}")
            return None

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
