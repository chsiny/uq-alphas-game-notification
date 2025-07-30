#!/usr/bin/env python3
"""
Test script to simulate different dates and see how the game parsing works
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
from config import ULTRA_MSG_TOKEN, ULTRA_MSG_INSTANCE_ID, DEFAULT_PHONE_NUMBER, DEFAULT_GROUP_ID


def parse_game_date(date_text):
    """Parse the date text from the website and return a datetime object"""
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
            
            # Assume current year (or next year if we're past December)
            current_year = datetime.now().year
            if month_num < datetime.now().month:
                current_year += 1
                
            return datetime(current_year, month_num, day_num)
    except Exception as e:
        print(f"Error parsing date '{date_text}': {e}")
        return None
    return None


def get_games_with_simulated_date(simulated_date):
    """Get all games and show which would be selected with a simulated date"""
    url = "https://touchfootball.com.au/Competitions/Competition/s2-2025-thursday-girls-u15d-63174269?team=63354766"

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
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
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.l-grid > li")))
        time.sleep(3)

        # Find all matches
        all_matches = driver.find_elements(By.CSS_SELECTOR, "ul.l-grid > li")
        
        if not all_matches:
            print("❌ No matches found")
            return None

        print(f"🔍 Testing with simulated date: {simulated_date.strftime('%Y-%m-%d')}")
        print("=" * 60)
        
        # Find the next upcoming game
        next_game = None
        game_count = 0
        
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
                        continue
                
                if not date_element:
                    continue
                    
                date_text = date_element.text.strip()
                
                # Parse the date
                game_date = parse_game_date(date_text)
                if not game_date:
                    continue
                
                game_count += 1
                
                # Check if this game is in the future relative to simulated date
                is_future = game_date > simulated_date
                status = "🟢 FUTURE" if is_future else "🔴 PAST"
                
                print(f"Game {game_count}: {date_text}")
                print(f"  Parsed date: {game_date.strftime('%Y-%m-%d')}")
                print(f"  Status: {status}")
                
                # Get teams
                teams = match.find_elements(By.CSS_SELECTOR, ".match-team__name")
                if not teams:
                    teams = match.find_elements(By.CSS_SELECTOR, ".team-name")
                if not teams:
                    teams = match.find_elements(By.CSS_SELECTOR, "[class*='team']")

                if len(teams) >= 2:
                    home_team = teams[0].text.strip()
                    away_team = teams[1].text.strip()
                    print(f"  Teams: {home_team} vs {away_team}")
                    
                    # Get time
                    try:
                        time_element = match.find_element(By.TAG_NAME, "time")
                        time_text = time_element.text.strip()
                        print(f"  Time: {time_text}")
                    except:
                        print(f"  Time: Not found")
                    
                    # Get venue
                    try:
                        venue_element = match.find_element(By.CSS_SELECTOR, ".match-cta__link")
                        venue_text = venue_element.text.strip()
                        print(f"  Venue: {venue_text}")
                    except:
                        print(f"  Venue: Not found")
                    
                    # If this is the first future game, mark it as next
                    if is_future and next_game is None:
                        next_game = {
                            "date": date_text,
                            "time": time_text if 'time_text' in locals() else "Unknown",
                            "home": home_team,
                            "away": away_team,
                            "venue": venue_text if 'venue_text' in locals() else "Unknown",
                            "game_date": game_date
                        }
                        print(f"  🎯 SELECTED AS NEXT GAME!")
                        
                print("-" * 40)
                        
            except Exception as e:
                print(f"Error processing match: {e}")
                continue

        print("=" * 60)
        if next_game:
            print(f"✅ Next game found: {next_game['home']} vs {next_game['away']} on {next_game['date']}")
        else:
            print("❌ No future games found")
            
        return next_game

    except Exception as e:
        print(f"Error loading page: {e}")
        return None

    finally:
        driver.quit()


def test_different_dates():
    """Test the script with different simulated dates"""
    print("🧪 Testing game parsing with different dates")
    print("=" * 60)
    
    # Test dates
    test_dates = [
        datetime.now(),  # Current date
        datetime.now() - timedelta(days=30),  # 30 days ago
        datetime.now() + timedelta(days=7),   # 7 days from now
        datetime.now() + timedelta(days=30),  # 30 days from now
        datetime(2025, 7, 30),  # July 30, 2025
        datetime(2025, 8, 5),   # August 5, 2025
        datetime(2025, 8, 10),  # August 10, 2025
    ]
    
    for test_date in test_dates:
        print(f"\n📅 Testing with date: {test_date.strftime('%Y-%m-%d')}")
        get_games_with_simulated_date(test_date)
        print("\n" + "=" * 60)


if __name__ == "__main__":
    test_different_dates() 