# Robot Trace

## Overview
**Robot Trace** is a tool designed to monitor Hamilton VENUS robot log folder
for errors and send notifications via Slack. It is based on python Watchdog
and slack webhook API with a simple http request.

## Getting Started
Follow these instructions to set up the project on your local machine for
development and testing purposes.

### Prerequisites
You will need:

- Python 3.x
- pip
- Virtualenv (optional, but recommended for environment management)

### Installation
Clone the repository and set up the environment:
```bash
git clone https://github.com/gorefbitim/robottrace.git
cd robottrace
```

Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Install the required packages:
```bash
pip install -r requirements.txt
```

## Configuring Slack Notifications
To enable Slack notifications, you need to create a Slack App for webhook
integration or bot functionality.

### Creating a Slack App
1. Go to [Your Apps](https://api.slack.com/apps) on the Slack API website.
2. Click **Create New App**, select **From scratch**.
3. Name your app (e.g., "Robot Monitor") and select your workspace.
4. Click **Create App**.

### Configuring Incoming Webhooks (for simple notifications)
1. Select **Incoming Webhooks** from the app settings.
2. Turn on incoming webhooks.
3. Click **Add New Webhook to Workspace**.
4. Choose a channel for the app to post to and authorize it.
5. Copy the webhook URL. Use this URL in Robot Monitor to send messages to
   Slack.

### Setting Bot Token (for interactive features)
1. Go to **OAuth & Permissions** in the app settings.
2. Add bot token scopes such as `chat:write` and `channels:read`.
3. Install the app in your workspace to obtain your Bot User OAuth Access
   Token.

### Usage
Ensure your webhook URL or bot token is set correctly in your project
configuration.

## Running the Application
Run the application with:
```bash
python robottrace.py
```

## Contributing
We welcome contributions! Please see `CONTRIBUTING.md` for how to submit
changes and our code of conduct.

## License
This project is licensed under the GNU General Public License v3.0 - see the
[LICENSE.md](LICENSE) file for more details.

## Acknowledgments
- Thanks to all contributors who help improve this project.
