import os
import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery
import google.auth.transport.requests

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

class YouTubeUnsubscriber:
    def __init__(self):
        self.youtube = self._authenticate()

    def _authenticate(self):
        """Handles YouTube API authentication."""
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        credentials = None
        token_path = "token.json"

        # Load existing token
        if os.path.exists(token_path):
            with open(token_path, "rb") as token_file:
                credentials = pickle.load(token_file)

        # Refresh or request new token
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(google.auth.transport.requests.Request())
            else:
                flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                    "client.json", SCOPES
                )
                credentials = flow.run_local_server(port=8080)

            # Save token
            with open(token_path, "wb") as token_file:
                pickle.dump(credentials, token_file)

        return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

    def get_subscriptions(self):
        """Fetches all subscribed channels."""
        subscriptions = []
        request = self.youtube.subscriptions().list(
            part="id,snippet",
            mine=True,
            maxResults=50  # Fetch 50 at a time (API limit)
        )
        while request:
            response = request.execute()
            for item in response.get("items", []):
                subscriptions.append((item["id"], item["snippet"]["title"]))
            request = self.youtube.subscriptions().list_next(request, response)
        return subscriptions

    def unsubscribe_all(self):
        """Unsubscribes from all channels."""
        subscriptions = self.get_subscriptions()
        if not subscriptions:
            print("No subscriptions found.")
            return

        for sub_id, title in subscriptions:
            try:
                self.youtube.subscriptions().delete(id=sub_id).execute()
                print(f"Unsubscribed from: {title}")
            except Exception as e:
                print(f"Failed to unsubscribe from {title}: {e}")

def main():
    unsubscriber = YouTubeUnsubscriber()
    unsubscriber.unsubscribe_all()

if __name__ == "__main__":
    main()
