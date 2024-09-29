from GameHandlerFutarchy import GameHandler
import websocket
import threading
import json


class WebSocketClient:
    def __init__(self, url, game_id, recovery, verbose=True):
        self.url = url
        self.game_id = game_id
        self.recovery = recovery
        self.verbose = verbose
        self.game_handler = GameHandler(game_id, verbose=verbose, websocket_client=self, recovery=recovery)
        self.ws = websocket.WebSocketApp(url,
                                         on_message=self.on_message,
                                         on_error=self.on_error)
        self.ws.on_open = self.on_open
        self.should_continue = True  # Flag to control the send_message loop
        self.wst = threading.Thread(target=lambda: self.ws.run_forever(ping_interval=30, ping_timeout=10), daemon=True)

    def on_message(self, ws, message):
        if self.verbose:
            print("Received message:", message)

        self.game_handler.receive_message(message)

    def on_error(self, ws, error):
        """
        Callback executed when an error occurs.
        :param ws: Is the WebSocketApp instance that received the message.
        :param error: is the error that occurred.
        :return:
        """
        print("Error:", error)

    def reconnect(self):
        """
        Function to reconnect to the server.
        :return:
        """
        self.wst = threading.Thread(target=self.ws.run_forever, daemon=True)
        self.wst.start()

    def on_open(self, ws):
        """
        Callback executed when the connection is open.
        :param ws: Is the WebSocketApp instance that received the message.
        :return:
        """
        print("### Connection is open ###")

        initial_message = json.dumps({"gameId": self.game_id, "type": "join", "recovery": self.recovery})

        if self.verbose:
            print("Sending message:", initial_message)  # Debugging: Print the message to be sent
        ws.send(initial_message)

    def send_message(self, message):
        """
        Function to send a message to the server.
        :param message: The message to be sent.
        :return:
        """
        if self.verbose:
            print("Sending message:", message)  # Debugging: Print the message to be sent
        self.ws.send(message)

    def run_forever(self):
        """
        Function to start the WebSocket client and keep it running.
        :return:
        """
        self.wst.start()
        try:
            while self.wst.is_alive():
                self.wst.join(timeout=1)
        except KeyboardInterrupt:
            self.ws.close()