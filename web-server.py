#!/usr/bin/env python3
"""
ClawBot Web Server
Flask web server with system monitoring and API
"""

import os
import psutil
import socket
import json
from datetime import datetime
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# HTML Template
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>ClawBot Monitor</title>
    <style>
        body { 
            font-family: 'Courier New', monospace; 
            background: #0d1117; 
            color: #c9d1d9; 
            padding: 20px;
        }
        .card {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 20px;
            margin: 10px;
            display: inline-block;
            min-width: 150px;
        }
        h1 { color: #58a6ff; }
        .value { font-size: 2em; color: #238636; }
        .label { opacity: 0.7; }
    </style>
</head>
<body>
    <h1>🤖 ClawBot System Monitor</h1>
    <p>Hostname: {{ hostname }}</p>
    <p>Uptime: {{ uptime }}</p>
    
    <div class="card">
        <div class="value">{{ cpu }}%</div>
        <div class="label">CPU</div>
    </div>
    
    <div class="card">
        <div class="value">{{ ram }}%</div>
        <div class="label">RAM</div>
    </div>
    
    <div class="card">
        <div class="value">{{ disk }}%</div>
        <div class="label">Disk</div>
    </div>
    
    <div class="card">
        <div class="value">{{ temp }}°C</div>
        <div class="label">Temp</div>
    </div>
    
    <h2>Processes</h2>
    <pre>{{ processes }}</pre>
    
    <p><small>🤖 ClawBot | github.com/jnetai-clawbot</small></p>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML,
        hostname=socket.gethostname(),
        uptime=get_uptime(),
        cpu=psutil.cpu_percent(),
        ram=psutil.virtual_memory().percent,
        disk=psutil.disk_usage('/').percent,
        temp=get_temp(),
        processes=get_top_processes()
    )

@app.route('/api/stats')
def api_stats():
    return jsonify({
        'cpu': psutil.cpu_percent(),
        'ram': psutil.virtual_memory().percent,
        'disk': psutil.disk_usage('/').percent,
        'temp': get_temp(),
        'uptime': get_uptime(),
        'hostname': socket.gethostname(),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/crypto')
def api_crypto():
    try:
        import urllib.request
        url = "https://api.binance.com/api/v3/ticker/price"
        data = urllib.request.urlopen(url).read()
        prices = json.loads(data)
        
        crypto = {}
        for symbol in ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'DOGEUSDT']:
            for p in prices:
                if p['symbol'] == symbol:
                    crypto[symbol] = float(p['price'])
                    break
        return jsonify(crypto)
    except Exception as e:
        return jsonify({'error': str(e)})

def get_uptime():
    try:
        with open('/proc/uptime') as f:
            seconds = float(f.read().split()[0])
            hours = int(seconds // 3600)
            mins = int((seconds % 3600) // 60)
            return f"{hours}h {mins}m"
    except:
        return "Unknown"

def get_temp():
    try:
        with open('/sys/class/thermal/thermal_zone0/temp') as f:
            return int(f.read()) / 1000
    except:
        return 0

def get_top_processes():
    procs = []
    for p in psutil.process_iter(['name', 'cpu_percent', 'memory_percent']):
        try:
            procs.append(p.info)
        except:
            pass
    procs.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
    return '\n'.join([f"{p['name'][:30]:<30} CPU: {p['cpu_percent']:.1f}%  RAM: {p['memory_percent']:.1f}%" 
                      for p in procs[:10]])

if __name__ == '__main__':
    print("🤖 Starting ClawBot Web Server...")
    print("📍 Open http://localhost:5000 in your browser")
    app.run(host='0.0.0.0', port=5000, debug=False)
