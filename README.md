# ULTRAVOX AGENT IN PYTHON

## High Level Call Creation Flow
<img width="920" alt="image" src="https://github.com/user-attachments/assets/a5a1768d-1e5d-4c31-bd78-ce62139e6fdf" />


## Requirements to run the project locally
* Python v >= 3.13.1
* Activate virtual environment with `source venv/bin/activate` in root directory
* Run `pip install -r requirements.txt` to install dependencies
* Setup AWS `AWS_ACCESS_KEY_ID` & `AWS_SECRET_ACCESS_KEY` either in .env or globally
* Set `ULTRAVOX_API_KEY` & `ULTRAVOX_API_URL` in .env file


## Configure Twilio
In order to acccess the app via Twilio port tunneling is needed. 
* Setup account with [ngrok](https://ngrok.com/docs/getting-started/) and start tunneling from application port 3000.
* Using the base public ngrok URL, point to `{baseUrl}/incoming (POST)` endpoint from Twilio active phone number voice Request URL.
* Create new agent using `/create-agent` endpoint after updating `toolsBaseUrl` var in `ultravox_config.py` with ngrok URL.
