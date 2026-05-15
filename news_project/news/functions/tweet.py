"""
Singleton class to manage Twitter API interactions.
"""
from requests_oauthlib import OAuth1Session

class Tweet:
    """
    Manages the Twitter OAuth session to prevent multiple 
    connections.
    """
    _instance = None

    # Dummy keys for testing purposes
    api_key = "DUMMY_KEY"
    api_secret = "DUMMY_SECRET"
    access_token = "DUMMY_TOKEN"
    access_secret = "DUMMY_SECRET"

    def __new__(cls):
        """Returns the single instance of the class."""
        if cls._instance is None:
            cls._instance = super(Tweet, cls).__new__(cls)
            cls._instance.authenticate()
        return cls._instance

    def authenticate(self):
        """Creates the OAuth session."""
        self.oauth_session = OAuth1Session(
            self.api_key,
            client_secret=self.api_secret,
            resource_owner_key=self.access_token,
            resource_owner_secret=self.access_secret,
        )

    def make_tweet(self, tweet_data):
        """
        Sends a POST request to Twitter API.
        Robustness: Anticipates errors so the app doesn't crash.
        """
        try:
            api_url = "https://api.twitter.com/2/tweets"
            response = self.oauth_session.post(
                api_url,
                json=tweet_data,
            )
            if response.status_code != 201:
                error_msg = "Twitter API error: "
                error_msg += str(response.status_code)
                print(error_msg)
        except Exception as error_msg:
            print("Failed to post tweet: " + str(error_msg))