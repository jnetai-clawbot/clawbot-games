#!/usr/bin/env python3
"""
ClawBot Reminder - Voice/Text Reminder Bot
Set reminders with voice or text
"""

import os
import time
import json
import threading
from datetime import datetime, timedelta
from pathlib import Path

REMINDERS_FILE = Path.home() / ".clawbot" / "reminders.json"

class ReminderBot:
    def __init__(self):
        self.reminders = []
        self.load_reminders()
        self.running = True
        
    def load_reminders(self):
        REMINDERS_FILE.parent.mkdir(parents=True, exist_ok=True)
        if REMINDERS_FILE.exists():
            with open(REMINDERS_FILE) as f:
                self.reminders = json.load(f)
    
    def save_reminders(self):
        with open(REMINDERS_FILE, 'w') as f:
            json.dump(self.reminders, f, indent=2)
    
    def add(self, message, minutes=0, hours=0, days=0):
        """Add a reminder"""
        remind_at = datetime.now() + timedelta(days=days, hours=hours, minutes=minutes)
        
        reminder = {
            'id': len(self.reminders) + 1,
            'message': message,
            'remind_at': remind_at.isoformat(),
            'created': datetime.now().isoformat()
        }
        
        self.reminders.append(reminder)
        self.save_reminders()
        
        print(f"✅ Reminder set: '{message}' at {remind_at.strftime('%Y-%m-%d %H:%M')}")
        return reminder
    
    def list_reminders(self):
        """List all reminders"""
        if not self.reminders:
            print("📝 No reminders set")
            return
        
        print("\n📋 Your Reminders:")
        print("-" * 50)
        
        for r in self.reminders:
            remind_at = datetime.fromisoformat(r['remind_at'])
            status = "⏰" if remind_at > datetime.now() else "✅"
            print(f"{r['id']}. {status} {r['message']}")
            print(f"   Due: {remind_at.strftime('%Y-%m-%d %H:%M')}")
            print()
    
    def delete(self, reminder_id):
        """Delete a reminder"""
        self.reminders = [r for r in self.reminders if r['id'] != reminder_id]
        self.save_reminders()
        print(f"🗑️ Reminder {reminder_id} deleted")
    
    def check_due(self):
        """Check for due reminders"""
        now = datetime.now()
        due = []
        
        for r in self.reminders:
            remind_at = datetime.fromisoformat(r['remind_at'])
            if remind_at <= now:
                due.append(r)
        
        return due
    
    def clear_completed(self):
        """Clear all completed reminders"""
        now = datetime.now()
        self.reminders = [r for r in self.reminders 
                        if datetime.fromisoformat(r['remind_at']) > now]
        self.save_reminders()
        print("✅ Cleared all completed reminders")


def main():
    import argparse
    
    bot = ReminderBot()
    parser = argparse.ArgumentParser(description='ClawBot Reminders')
    parser.add_argument('command', choices=['add', 'list', 'delete', 'clear'])
    parser.add_argument('--message', '-m', help='Reminder message')
    parser.add_argument('--minutes', '-min', type=int, default=0, help='Minutes from now')
    parser.add_argument('--hours', '-h', type=int, default=0, help='Hours from now')
    parser.add_argument('--days', '-d', type=int, default=0, help='Days from now')
    parser.add_argument('--id', '-i', type=int, help='Reminder ID for delete')
    
    args = parser.parse_args()
    
    if args.command == 'add':
        if not args.message:
            print("Error: --message required")
            return
        bot.add(args.message, args.minutes, args.hours, args.days)
    
    elif args.command == 'list':
        bot.list_reminders()
    
    elif args.command == 'delete':
        if args.id:
            bot.delete(args.id)
        else:
            print("Error: --id required")
    
    elif args.command == 'clear':
        bot.clear_completed()


if __name__ == "__main__":
    main()

# Example usage:
# python3 reminder.py add -m "Take out trash" -h 1
# python3 reminder.py add -m "Call mum" -d 1
# python3 reminder.py list
# python3 reminder.py delete --id 1
