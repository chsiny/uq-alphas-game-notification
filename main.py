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
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ultramsg API Configuration
# Get your credentials from https://ultramsg.com/
# Set these in your .env file or as environment variables

ULTRA_MSG_TOKEN_JUSTIN = os.getenv("ULTRA_MSG_TOKEN_JUSTIN", "")
ULTRA_MSG_INSTANCE_ID_JUSTIN = os.getenv("ULTRA_MSG_INSTANCE_ID_JUSTIN", "")
ULTRA_MSG_TOKEN_NOTITIER = os.getenv("ULTRA_MSG_TOKEN_NOTITIER", "")
ULTRA_MSG_INSTANCE_ID_NOTITIER = os.getenv("ULTRA_MSG_INSTANCE_ID_NOTITIER", "")
DEFAULT_GROUP_ID = os.getenv("DEFAULT_GROUP_ID", "") 
NOTIFICATION_GROUP_ID = os.getenv("NOTIFICATION_GROUP_ID", "")

class User:
    """User class for Ultramsg API"""
    def __init__(self, token: str, instance_id: str):
        self.token = token
        self.instance_id = instance_id


def get_brisbane_timezone() -> pytz.timezone:
    """Get Brisbane timezone"""
    return pytz.timezone('Australia/Brisbane')

def get_current_brisbane_time() -> datetime:
    """Get current time in Brisbane timezone"""
    brisbane_tz = get_brisbane_timezone()
    return datetime.now(brisbane_tz)

def parse_game_date(date_text: str) -> tuple[datetime, str]:
    """Parse the date text from the website and return a datetime object in Brisbane timezone"""
    try:
        # Split by newlines to separate date and additional info
        lines = date_text.split('\n')
        date_line = lines[0].strip()
        additional_info = lines[1].strip() if len(lines) > 1 else ""
        
        # Parse date like "THURSDAY 31ST JULY" (uppercase)
        # Extract day name, day number, and month
        parts = date_line.split()
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
            
            return brisbane_datetime, additional_info
    except Exception as e:
        print(f"Error parsing date '{date_text}': {e}")
        return None, ""
    return None, ""


def get_next_game() -> dict | None:
    """Get the next game"""
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
                
                # Parse the date and additional information
                game_date, additional_info = parse_game_date(date_text)
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

                        # Get time and convert to Brisbane time
                        time_element = match.find_element(By.TAG_NAME, "time")
                        time_text = time_element.text.strip()
                        
                        # Get the datetime attribute to convert to Brisbane time
                        try:
                            datetime_attr = time_element.get_attribute("datetime")
                            if datetime_attr:
                                # Parse UTC time and convert to Brisbane
                                utc_time = datetime.fromisoformat(datetime_attr.replace('Z', '+00:00'))
                                brisbane_tz = get_brisbane_timezone()
                                brisbane_time = utc_time.astimezone(brisbane_tz)
                                # Format time without leading zero
                                hour = brisbane_time.hour
                                if hour == 0:
                                    hour = 12
                                elif hour > 12:
                                    hour -= 12
                                time_text = f"{hour}:{brisbane_time.minute:02d}{brisbane_time.strftime('%p').lower()}"  # e.g., "7:50pm"
                        except Exception as e:
                            print(f"Error converting time to Brisbane: {e}")
                            # Keep original time if conversion fails

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
                            "game_date": game_date,
                            "round": additional_info
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


def format_message(info: dict) -> str:
    """Format the message for the next game"""
    # Calculate warm-up time (50 minutes before kickoff)
    try:
        # Parse the kickoff time to calculate warm-up time
        kickoff_time = info['time']  # e.g., "7:50pm"
        
        # Convert to 24-hour format for easier calculation
        if 'pm' in kickoff_time.lower():
            time_parts = kickoff_time.lower().replace('pm', '').split(':')
            hour = int(time_parts[0])
            if hour != 12:
                hour += 12
            minute = int(time_parts[1])
        elif 'am' in kickoff_time.lower():
            time_parts = kickoff_time.lower().replace('am', '').split(':')
            hour = int(time_parts[0])
            if hour == 12:
                hour = 0
            minute = int(time_parts[1])
        else:
            # Assume 24-hour format
            time_parts = kickoff_time.split(':')
            hour = int(time_parts[0])
            minute = int(time_parts[1])
        
        # Calculate warm-up time (50 minutes earlier)
        warmup_minute = minute - 50
        warmup_hour = hour
        
        if warmup_minute < 0:
            warmup_minute += 60
            warmup_hour -= 1
        
        if warmup_hour < 0:
            warmup_hour += 24
        
        # Convert back to 12-hour format
        if warmup_hour == 0:
            warmup_hour = 12
            ampm = 'am'
        elif warmup_hour < 12:
            ampm = 'am'
        elif warmup_hour == 12:
            ampm = 'pm'
        else:
            warmup_hour -= 12
            ampm = 'pm'
        
        warmup_time = f"{warmup_hour}:{warmup_minute:02d}{ampm}"
        
    except Exception as e:
        print(f"Error calculating warm-up time: {e}")
        warmup_time = "TBD"
    
    # Format the date properly (e.g., "THURSDAY 31ST JULY")
    date_text = info['date'].upper()
    
    # Get round information
    round_info = info.get('round', 'Round 1')  # Default to "Round 1" if not found
    
    # Clean up the date text to remove any round information that might be included
    if 'ROUND' in date_text:
        # Split by newlines and take only the first line (the actual date)
        date_lines = date_text.split('\n')
        date_text = date_lines[0].strip()
    
    # Format team names (assuming they're already in the right format)
    home_team = info['home']
    away_team = info['away']
    
    # Determine which team is UQ Alphas for proper formatting
    if 'UQ Alphas' in home_team:
        opponent = away_team
        vs_text = f"UQ Alphas vs {opponent}"
    elif 'UQ Alphas' in away_team:
        opponent = home_team
        vs_text = f"{opponent} vs UQ Alphas" 
    else:
        vs_text = f"{home_team} vs {away_team}"
    
    return f"""📅 *{date_text} – {round_info}*
🕖 *Warm-up: {warmup_time}*
🚀 *Kickoff: {info['time']}*
🏉 *{vs_text}*
📍 *{info['venue']}*"""


def send_whatsapp_message(user: User, phone_number: str, message: str) -> bool:
    """Send WhatsApp message using Ultramsg API"""
    # Ultramsg API configuration
    url = f"https://api.ultramsg.com/{user.instance_id}/messages/chat"
    
    payload = {
        "token": user.token,
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
        notify_group_id = NOTIFICATION_GROUP_ID
        justin = User(ULTRA_MSG_TOKEN_JUSTIN, ULTRA_MSG_INSTANCE_ID_JUSTIN)
        notitier = User(ULTRA_MSG_TOKEN_NOTITIER, ULTRA_MSG_INSTANCE_ID_NOTITIER)
        print("Sending WhatsApp message to group...")
        # send_whatsapp_message(justin, group_id, msg)
        send_whatsapp_message(notitier, notify_group_id, msg)

    else:
        print("⚠️ Could not find any upcoming game.")
