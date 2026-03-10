#!/usr/bin/env python3
"""
ClawBot CLI - Command Line Tools
Useful terminal utilities
"""

import sys
import os
import json
import subprocess
import argparse
from datetime import datetime

def cmd_sysinfo():
    """Display system information"""
    try:
        # CPU
        with open('/proc/cpuinfo', 'r') as f:
            cpuinfo = f.read()
            model = [line for line in cpuinfo.split('\n') if 'model name' in line]
            cpu = model[0].split(':')[1].strip() if model else 'Unknown'
        
        # Memory
        with open('/proc/meminfo', 'r') as f:
            meminfo = f.read()
            mem = [line for line in meminfo.split('\n') if 'MemTotal' in line]
            mem_total = int(mem[0].split()[1]) / 1024 / 1024 if mem else 0
        
        # Uptime
        with open('/proc/uptime', 'r') as f:
            uptime = float(f.read().split()[0])
            days = int(uptime // 86400)
            hours = int((uptime % 86400) // 3600)
        
        print(f"🖥️  System Info")
        print(f"CPU: {cpu}")
        print(f"RAM: {mem_total:.1f} GB")
        print(f"Uptime: {days}d {hours}h")
        
    except Exception as e:
        print(f"Error: {e}")

def cmd_weather(city="London"):
    """Get weather for a city (using wttr.in)"""
    try:
        result = subprocess.run(
            ['curl', '-s', f'wttr.in/{city}?format=%c%t+%h'],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            print(f"🌤️  Weather in {city}: {result.stdout.strip()}")
        else:
            print("Could not fetch weather")
    except Exception as e:
        print(f"Error: {e}")

def cmd_crypto():
    """Get crypto prices"""
    try:
        import urllib.request
        url = "https://api.binance.com/api/v3/ticker/price"
        data = urllib.request.urlopen(url).read()
        prices = json.loads(data)
        
        crypto = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'DOGEUSDT']
        print("💰 Crypto Prices:")
        
        for symbol in crypto:
            for p in prices:
                if p['symbol'] == symbol:
                    name = symbol.replace('USDT', '')
                    print(f"  {name}: ${float(p['price']):,.2f}")
                    break
    except Exception as e:
        print(f"Error: {e}")

def cmd_backup(source, dest):
    """Simple backup command"""
    if not dest:
        dest = f"backup-{datetime.now().strftime('%Y%m%d')}.tar.gz"
    
    print(f"📦 Creating backup of {source} to {dest}...")
    
    try:
        subprocess.run(['tar', '-czf', dest, source], check=True)
        print(f"✅ Backup created: {dest}")
    except Exception as e:
        print(f"❌ Backup failed: {e}")

def main():
    parser = argparse.ArgumentParser(description='ClawBot CLI Tools')
    parser.add_argument('command', choices=['sysinfo', 'weather', 'crypto', 'backup'])
    parser.add_argument('args', nargs='*', help='Arguments for command')
    
    args = parser.parse_args()
    
    if args.command == 'sysinfo':
        cmd_sysinfo()
    elif args.command == 'weather':
        city = args.args[0] if args.args else "London"
        cmd_weather(city)
    elif args.command == 'crypto':
        cmd_crypto()
    elif args.command == 'backup':
        source = args.args[0] if args.args else "."
        dest = args.args[1] if len(args.args) > 1 else None
        cmd_backup(source, dest)

if __name__ == "__main__":
    main()
