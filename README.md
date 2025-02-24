# YouTube Unsubscriber

A Python script to automatically unsubscribe from all YouTube channels using the YouTube Data API v3.

## Warning
- The Youtube API limits the number of requests by users, you may not be able to unsubscribe from ALL channels at once if you have too many subscriptions. After waiting for your request quota to reset, you'll be able to continue. 

## Features

- Fetches all subscribed channels from your YouTube account
- Automatically unsubscribes from all channels
- Token-based authentication with refresh capabilities
- Error handling and logging for failed unsubscriptions

## Prerequisites

- Python 3.6+
- Google Cloud Project with YouTube Data API v3 enabled
- OAuth 2.0 Client credentials (client.json)

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/youtube-unsubscriber.git
   cd youtube-unsubscriber
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python -m venv youtube_env
   source youtube_env/bin/activate  # On Windows: youtube_env\Scripts\activate
   ```

3. **Install required packages:**
   ```sh
   pip install -r requirements.txt
   ```

## Configuration

1. **Set up Google Cloud Project:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable **YouTube Data API v3**
   - Create **OAuth 2.0 credentials** (Desktop application)
   - Download the credentials and save them as `client.json` in the project root

2. **First Run Authentication:**
   - The script will open a browser window for Google authentication
   - Grant the necessary permissions
   - A `token.json` file will be generated for future authentication

## Usage

Run the script to unsubscribe from all YouTube channels:
```sh
python unsubscribe.py
```

The script will:
- Retrieve all subscribed channels
- Unsubscribe from each one
- Display progress in the terminal

## Notes
- If you want to selectively unsubscribe from channels, modify `unsubscribe_all()` in `unsubscribe.py` to filter channels based on your criteria.
- The script uses OAuth 2.0 authentication, and the token is stored in `token.json` to avoid re-authentication on every run.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
