from dotenv import load_dotenv
from flask_script import Manager
from eng_zap_challenge_python import create_app
from eng_zap_challenge_python.client import source_client

load_dotenv()  # take environment variables from .env.
source_client.load_data_source()
manager = Manager(create_app)
app = create_app()
