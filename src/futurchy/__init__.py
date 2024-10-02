import re
import argparse
import logging
import time
from WebSocketClient import WebSocketClient
from concurrent.futures import ThreadPoolExecutor


def parse_url(url):
    match = re.search(r'https?://([^/:]+)(?::\d+)?/([\w-]+)/(\d+)/([\w-]+)',
                      url)
    if match:
        hostname = match.group(1)
        endpoint = match.group(2)
        game_id = int(match.group(3))
        recovery = match.group(4)
        return hostname, endpoint, game_id, recovery
    else:
        raise ValueError(
            "Invalid URL format. Expected format: http://<hostname>/<endpoint>/<gameId>/<recovery>")


def start_simulation(url):
    logger = logging.getLogger("Simulation")
    try:
        hostname, endpoint, game_id, recovery = parse_url(url)
        logger.info(
            f"Parsed URL successfully: Hostname={hostname}, Endpoint={endpoint}, Game ID={game_id}, Recovery={recovery}")

        ws_url = f"ws://{hostname}:3088/{endpoint}"
        logger.info(f"Constructed WebSocket URL: {ws_url}")
        print(f"Connecting to WebSocket URL: {ws_url}")

        client = WebSocketClient(url=ws_url, game_id=game_id,
                                 recovery=recovery, verbose=True)
        client.start()
        logger.info("WebSocket client started.")
        print("WebSocket client is running. Press Ctrl+C to exit.")

        while True:
            time.sleep(1)

    except Exception as e:
        logger.error(f"Error in simulation: {e}")
        print(f"Simulation error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Start multiple WebSocket simulations.")
    parser.add_argument('N', type=int, help='Number of agents (simulations)')
    parser.add_argument('urls', nargs='+', help='List of URLs for each agent')

    args = parser.parse_args()

    if len(args.urls) != args.N:
        raise ValueError(
            "The number of URLs must match the number of agents (N).")

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        handlers=[logging.StreamHandler()]
    )

    with ThreadPoolExecutor(max_workers=args.N) as executor:
        for url in args.urls:
            executor.submit(start_simulation, url)


if __name__ == "__main__":
    main()
