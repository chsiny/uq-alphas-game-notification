# UQ Alphas Game Notification System

Automated WhatsApp notifications for UQ Alphas football games using web scraping and Ultramsg API.

## 🎯 **What This Does**

This system automatically:
- Scrapes the UQ Alphas football team's game schedule
- Sends WhatsApp notifications about upcoming games
- Keeps team members informed about game times and locations

## 📋 **Setup Instructions**

### **Environment Variables**
Create a `.env` file with:
```
ULTRA_MSG_TOKEN=your_token_here
ULTRA_MSG_INSTANCE_ID=your_instance_id_here
DEFAULT_PHONE_NUMBER=your_phone_number_here
```

### **GitHub Secrets (for GitHub Actions)**
Add these secrets in your repository:
- `ULTRA_MSG_TOKEN`
- `ULTRA_MSG_INSTANCE_ID` 
- `DEFAULT_PHONE_NUMBER`

## 🏃‍♂️ **How to Run**

### **Locally:**
```bash
python main.py
```

### **GitHub Actions:**
1. Go to Actions tab
2. Select "UQ Alphas Game Notification"
3. Click "Run workflow"

## 📱 **WhatsApp Integration**

Uses Ultramsg API for reliable WhatsApp messaging:
- Professional API service
- No browser automation required
- Reliable delivery

## 🔧 **Technical Details**

- **Web Scraping:** Selenium with Chrome headless
- **WhatsApp:** Ultramsg API
- **Language:** Python 3.11 