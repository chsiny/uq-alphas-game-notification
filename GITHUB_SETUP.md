# GitHub Actions Setup Guide

This guide will help you set up the automated game notification system using GitHub Actions.

## 🚀 Setup Steps

### 1. Fork/Clone the Repository
- Fork this repository to your GitHub account, OR
- Clone it to your local machine and push to your own repository

### 2. Configure GitHub Secrets
Go to your repository settings and add these secrets:

#### **ULTRA_MSG_TOKEN**
- Go to: `Settings` → `Secrets and variables` → `Actions`
- Click **"New repository secret"**
- Name: `ULTRA_MSG_TOKEN`
- Value: Your Ultramsg API token

#### **ULTRA_MSG_INSTANCE_ID**
- Click **"New repository secret"** again
- Name: `ULTRA_MSG_INSTANCE_ID`
- Value: Your Ultramsg instance ID

#### **DEFAULT_PHONE_NUMBER**
- Click **"New repository secret"** again
- Name: `DEFAULT_PHONE_NUMBER`
- Value: Your phone number (e.g., `+61423339538`)

### 3. Test the Workflow
1. Go to the **"Actions"** tab in your repository
2. Click on **"UQ Alphas Game Notification"**
3. Click **"Run workflow"** → **"Run workflow"**
4. This will manually trigger the script to test it

### 4. Verify Automation
- The workflow will automatically run every **Wednesday at 2:00 PM UTC** (10:00 PM Brisbane time)
- You can check the **"Actions"** tab to see run history
- Successful runs will show green checkmarks
- Failed runs will show red X marks with error details

## ⏰ Schedule Details

**Current Schedule:** Every Wednesday at 2:00 PM UTC
- **Brisbane Time:** 10:00 PM Wednesday
- **Sydney Time:** 10:00 PM Wednesday
- **Melbourne Time:** 10:00 PM Wednesday

**To change the schedule:**
Edit `.github/workflows/game-notification.yml` and modify the cron expression:
```yaml
- cron: '0 14 * * 3'  # Wednesday 2:00 PM UTC
```

## 🔧 Troubleshooting

### **Workflow Fails:**
1. Check the **Actions** tab for error logs
2. Verify your Ultramsg credentials are correct
3. Ensure your phone number includes country code

### **No Notifications Received:**
1. Check Ultramsg dashboard for message status
2. Verify your WhatsApp is connected to Ultramsg
3. Check the workflow logs for API errors

### **Manual Testing:**
- Use the **"Run workflow"** button to test anytime
- Check the logs in the Actions tab for detailed output

## 📊 Monitoring

- **Success Rate:** Check the Actions tab for green/red indicators
- **Logs:** Each run provides detailed logs
- **Artifacts:** Failed runs upload error logs as artifacts

## 🔒 Security Notes

- **Secrets are encrypted** and never visible in logs
- **Credentials are secure** and only used during workflow execution
- **No sensitive data** is stored in the repository 