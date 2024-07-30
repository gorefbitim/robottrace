import requests
import sys
import os
from dotenv import load_dotenv


load_dotenv()


slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")


def webhook_post_message_to_slack(text):
    """
    Posts a simple message to a Slack channel.

    :param text: The text of the message to post.
    """
    # Send the message to Slack
    response = requests.post(slack_webhook_url, json={'text': text})

    if response.status_code != 200:
        raise ValueError(
            f"Request to Slack returned an error"
            f"{response.status_code}, the response is:\n{response.text}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        message = sys.argv[1]
        webhook_post_message_to_slack(message)
    else:
        print("Usage: script.py 'message to post'")
