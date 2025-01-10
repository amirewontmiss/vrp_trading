from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import pandas as pd
from datetime import datetime, timedelta

app = Flask(__name__)
socketio = SocketIO(app)

class WebApp:
    def __init__(self, strategy_manager, data_manager):
        self.strategy_manager = strategy_manager
        self.data_manager = data_manager

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/api/strategy_performance')
    def get_strategy_performance():
        performance_data = self.strategy_manager.get_performance_metrics()
        return jsonify(performance_data)

    @socketio.on('connect')
    def handle_connect():
        print('Client connected')

    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected')

    def run(self, host='0.0.0.0', port=5000):
        socketio.run(app, host=host, port=port)
