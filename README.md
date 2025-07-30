# UQ Alphas Game Notification System

Automated WhatsApp notifications for UQ Alphas football games using web scraping and Ultramsg API.

## 🚨 **Important: GitHub Actions Scheduling Limitations**

**GitHub Actions scheduled workflows are NOT reliable for precise timing.** According to [GitHub's own documentation](https://upptime.js.org/blog/2021/01/22/github-actions-schedule-not-working/), scheduled workflows can have delays of 3-10 minutes or more, and may not run at all if delays are too long.

### **Current Status:**
- ✅ **Manual triggers work perfectly**
- ❌ **Scheduled runs are unreliable**
- 🔧 **Solution: Use external scheduler**

## 🎯 **Recommended Solutions:**

### **Option 1: External Cron Service (Recommended)**
Use a free service like **Cronhub** or **IFTTT** to trigger the workflow via GitHub API:

1. **Cronhub** (Free tier available):
   - Set up a webhook to trigger the workflow
   - More reliable than GitHub's built-in scheduling

2. **IFTTT** (Free):
   - Create an applet that runs on schedule
   - Triggers GitHub workflow via webhook

### **Option 2: Manual Triggers**
Since manual triggers work perfectly, you can:
- Run manually when needed
- Set reminders to trigger manually
- Use GitHub's "Run workflow" button

### **Option 3: Local Cron Job**
Run the script locally with cron:
```bash
# Add to crontab
0 12 * * 3 cd /path/to/repo && python main.py
```

## 📋 **Setup Instructions**

### **Environment Variables**
Create a `.env` file with:
```
ULTRA_MSG_TOKEN=your_token_here
ULTRA_MSG_INSTANCE_ID=your_instance_id_here
DEFAULT_PHONE_NUMBER=your_phone_number_here
```

### **GitHub Secrets (for manual triggers)**
Add these secrets in your repository:
- `ULTRA_MSG_TOKEN`
- `ULTRA_MSG_INSTANCE_ID` 
- `DEFAULT_PHONE_NUMBER`

## 🏃‍♂️ **How to Run**

### **Locally:**
```bash
python main.py
```

### **GitHub Actions (Manual):**
1. Go to Actions tab
2. Select "UQ Alphas Game Notification"
3. Click "Run workflow"

### **External Scheduler:**
Set up Cronhub or IFTTT to trigger the workflow via GitHub API.

## 📱 **WhatsApp Integration**

Uses Ultramsg API for reliable WhatsApp messaging:
- Professional API service
- No browser automation required
- Reliable delivery

## 🔧 **Technical Details**

- **Web Scraping:** Selenium with Chrome headless
- **WhatsApp:** Ultramsg API
- **Scheduling:** GitHub Actions (unreliable) + External services (recommended)
- **Language:** Python 3.11

## 📞 **Support**

If you need help setting up external scheduling, check out:
- [Cronhub](https://cronhub.io/) - Free tier available
- [IFTTT](https://ifttt.com/) - Free automation service
- [GitHub API Documentation](https://docs.github.com/en/rest/actions/workflows) 