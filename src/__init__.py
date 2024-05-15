import re
import websocket
from WebSocketClient import WebSocketClient

def parse_url(url):
    """
    Parse the URL to extract the gameId and recovery token.
    :param url: The URL to parse.
    :return: A tuple containing the gameId and recovery token.
    """
    # TODO: Make this work for other simulation such as DoubleAuction etc.
    match = re.search(r'/voting/(\d+)/(\w+)', url)
    if match:
        game_id = int(match.group(1))
        recovery = match.group(2)
        return game_id, recovery
    else:
        raise ValueError("URL format is incorrect. Expected format: http://localhost:8080/voting/<gameId>/<recovery>")

if __name__ == "__main__":
    websocket.enableTrace(False)
    url_input = input("Enter the URL: ")
    try:
        game_id, recovery = parse_url(url_input)
        client = WebSocketClient("ws://localhost:3088", game_id, recovery)
        client.run_forever()
    except ValueError as e:
        print(e)