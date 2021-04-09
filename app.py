from flask_script import Manager
from eng_zap_challenge_python import create_app
from eng_zap_challenge_python.client import source_client

source_client.load_data_source()
manager = Manager(create_app)

if __name__ == "__main__":
    manager.run()
