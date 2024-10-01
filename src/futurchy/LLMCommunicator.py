# LLMCommunicator.py

import json
import logging
import re
from openai import OpenAI

# Configure Logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

class LLMCommunicator:
    def __init__(self, openai_api_key=None):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.client = OpenAI()

    def query_openai(self, summary):
        """
        Sends the summary to OpenAI and retrieves the response.
        """
        try:
            instructions = (
                "You are an agent participating in a Harberger tax simulation game. "
                "Based on the following events and your current status, please decide whether to post a 'bid' order to buy assets or an 'ask' order to sell assets you own. "
                "Consider the current market conditions, your objectives, and any potential profits when making your decision. "
                "Your response should be in valid JSON format without any extra text, explanation, or formatting."
            )

            prompt = f"{instructions}\n\nEvents Summary:\n{summary}"
            self.logger.debug(f"Sending prompt to LLM: {prompt}")

            message = [{"role": "user", "content": prompt}]
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=message,
                # temperature=0.7,
            )

            response_text = response.choices[0].message.content
            self.logger.debug(f"Received response from LLM: {response_text}")

            ws_message = self.process_websocket_message(response_text)
            return ws_message

        except Exception as e:
            self.logger.error(f"Error communicating with OpenAI: {e}")
            return None

    def process_websocket_message(self, response_text):
        """
        Processes the LLM's response to ensure it's valid JSON.
        """
        try:
            # Clean the response text
            cleaned_response_text = response_text.strip().strip('```').strip()
            cleaned_response_text = re.sub(r'^json', '', cleaned_response_text, flags=re.IGNORECASE).strip()

            # Validate JSON
            response_json = json.loads(cleaned_response_text)
            self.logger.debug(f"Processed WebSocket message: {response_json}")
            return response_json

        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to decode JSON: {e} - Response text: {response_text}")
            return None
        except Exception as e:
            self.logger.error(f"Error processing WebSocket message: {e}")
            return None

    def send_to_websocket_client(self, websocket_client, message):
        """
        Sends a message to the WebSocket client.
        """
        try:
            if websocket_client:
                json_message = json.dumps(message)
                websocket_client.send_message(json_message)
                self.logger.debug(f"Sent message to WebSocket client: {json_message}")
            else:
                self.logger.error("WebSocket client is not available.")
        except Exception as e:
            self.logger.error(f"Error sending message to WebSocket client: {e}")
