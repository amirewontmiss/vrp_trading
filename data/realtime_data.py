import websocket
import json
import threading
from typing import Dict, Callable
from queue import Queue

class RealtimeDataManager:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.websocket: Optional[websocket.WebSocketApp] = None
        self.subscribers: Dict[str, List[Callable]] = {}
        self.data_queue = Queue()
        self.running = False

    def start(self):
        """Start realtime data streaming"""
        def on_message(ws, message):
            data = json.loads(message)
            self.data_queue.put(data)
            self._notify_subscribers(data)

        def on_error(ws, error):
            self.logger.error(f"WebSocket error: {error}")

        def on_close(ws, close_status_code, close_msg):
            self.logger.info("WebSocket connection closed")

        def on_open(ws):
            self.logger.info("WebSocket connection established")
            # Subscribe to relevant data streams
            subscribe_message = {
                "type": "subscribe",
                "symbols": list(self.subscribers.keys())
            }
            ws.send(json.dumps(subscribe_message))

        self.websocket = websocket.WebSocketApp(
            f"wss://your.websocket.url/{self.api_key}",
            on_message=on_message,
            on_error=on_error,
            on_close=on_close,
            on_open=on_open
        )

        self.running = True
        threading.Thread(target=self.websocket.run_forever).start()

    def stop(self):
        """Stop realtime data streaming"""
        self.running = False
        if self.websocket:
            self.websocket.close()

    def subscribe(self, symbol: str, callback: Callable):
        """Subscribe to updates for a symbol"""
        if symbol not in self.subscribers:
            self.subscribers[symbol] = []
        self.subscribers[symbol].append(callback)

    def _notify_subscribers(self, data: Dict):
        """Notify subscribers of new data"""
        symbol = data.get('symbol')
        if symbol in self.subscribers:
            for callback in self.subscribers[symbol]:
                callback(data)
