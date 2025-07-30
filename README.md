# UQ Alphas Game Notification

This script automatically fetches the next UQ Alphas touch football game and sends WhatsApp notifications using Ultramsg API.

## Setup Instructions

### 1. Install Dependencies
```bash
pip install selenium webdriver-manager requests
```

### 2. Get Ultramsg API Credentials
1. Go to [https://ultramsg.com/](https://ultramsg.com/)
2. Sign up for an account
3. Create a new WhatsApp instance
4. Get your **Token** and **Instance ID**

### 3. Configure the Script
Edit `config.py` and replace the placeholder values:
```python
ULTRA_MSG_TOKEN = "your_actual_token_here"
ULTRA_MSG_INSTANCE_ID = "your_actual_instance_id_here"
DEFAULT_PHONE_NUMBER = "+61423339538"  # Your phone number
```

### 4. Run the Script
```bash
python main.py
```

## Features
- ✅ Automatically fetches next game from Touch Football Australia website
- ✅ Handles dynamic JavaScript content using Selenium
- ✅ Sends WhatsApp notifications via Ultramsg API
- ✅ Configurable phone number and API credentials
- ✅ Error handling and status reporting

## How it Works
1. **Web Scraping**: Uses Selenium to load the Touch Football Australia website and wait for Vue.js to render
2. **Data Extraction**: Extracts game details (date, time, teams, venue) from the first upcoming match
3. **WhatsApp Integration**: Sends formatted message via Ultramsg API
4. **Error Handling**: Provides clear feedback on success/failure

## Message Format
```
📅 THURSDAY 31ST JULY Round 1
🕖 Kickoff: 7:50pm
🏉 SS Chatterboxes vs UQ Alphas
📍 Venue: Whites Hill Recreation Reserve - Field 6
```

## 🚀 GitHub Actions Automation

This project includes GitHub Actions for automated notifications every Wednesday afternoon.

### **Setup for Automation:**
1. **Configure GitHub Secrets** (see `GITHUB_SETUP.md`)
2. **Push to GitHub** - The workflow will run automatically
3. **Monitor in Actions tab** - Check run history and logs

### **Schedule:**
- **Runs:** Every Wednesday at 2:00 PM UTC (10:00 PM Brisbane time)
- **Manual Trigger:** Available via "Run workflow" button
- **Logs:** Available in the Actions tab

## Troubleshooting
- **API Errors**: Check your Ultramsg credentials in `config.py` or GitHub secrets
- **Web Scraping Issues**: The website structure may have changed
- **Chrome Driver Issues**: The script automatically downloads the correct ChromeDriver version
- **GitHub Actions**: See `GITHUB_SETUP.md` for detailed setup instructions 