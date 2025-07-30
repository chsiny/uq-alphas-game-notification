#!/usr/bin/env python3
"""
Script to find WhatsApp group IDs using Ultramsg API
"""

import requests
import json
from config import ULTRA_MSG_TOKEN, ULTRA_MSG_INSTANCE_ID

def get_groups():
    """Get list of all groups"""
    url = f"https://api.ultramsg.com/{ULTRA_MSG_INSTANCE_ID}/groups"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "token": ULTRA_MSG_TOKEN
    }
    
    try:
        response = requests.get(url, json=payload, headers=headers)
        if response.status_code == 200:
            result = response.json()
            print("✅ Groups found:")
            print("=" * 50)
            print(f"Raw response: {result}")
            if isinstance(result, list):
                for group in result:
                    print(f"📱 Group Name: {group.get('name', 'Unknown')}")
                    print(f"🆔 Group ID: {group.get('id', 'Unknown')}")
                    print(f"👥 Participants: {group.get('participants_count', 0)}")
                    print("-" * 30)
            elif isinstance(result, dict):
                for group in result.get("groups", []):
                    print(f"📱 Group Name: {group.get('name', 'Unknown')}")
                    print(f"🆔 Group ID: {group.get('id', 'Unknown')}")
                    print(f"👥 Participants: {group.get('participants_count', 0)}")
                    print("-" * 30)
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Error: {e}")

def send_test_message(group_id):
    """Send a test message to the group"""
    url = f"https://api.ultramsg.com/{ULTRA_MSG_INSTANCE_ID}/messages/chat"
    
    payload = {
        "token": ULTRA_MSG_TOKEN,
        "to": group_id,
        "body": "🧪 Test message from UQ Alphas notification system!"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            result = response.json()
            if result.get("sent"):
                print(f"✅ Test message sent successfully to group!")
                return True
            else:
                print(f"❌ Failed to send message: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error sending message: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Finding WhatsApp groups...")
    print("=" * 50)
    
    # Get all groups
    get_groups()
    
    print("\n" + "=" * 50)
    print("💡 To test a specific group, run:")
    print("python find_group_id.py <group_id>")
    print("=" * 50)
    
    # If group ID provided as argument, send test message
    import sys
    if len(sys.argv) > 1:
        group_id = sys.argv[1]
        print(f"\n🧪 Testing group: {group_id}")
        send_test_message(group_id) 