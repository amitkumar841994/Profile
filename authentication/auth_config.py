from authlib.integrations.starlette_client import OAuth
import os
from dotenv import load_dotenv

load_dotenv()

oauth = OAuth()
google = oauth.register(
    name="google",
    client_id="540078242760-5sb5vsq6v09abikto5r7dknck37canei.apps.googleusercontent.com",
    client_secret="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",
    access_token_url="https://oauth2.googleapis.com/token",
    access_token_params=None,
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params=None,
    api_base_url="https://www.googleapis.com/oauth2/v1/",
    client_kwargs={"scope": "openid email profile"},
)
print("google>>>>>",google)
