from dotenv import load_dotenv
from flask_script import Manager
from eng_zap_challenge_python.client import source_client
from eng_zap_challenge_python import create_app


def main():
    load_dotenv()  # take environment variables from .env.
    source_client.load_data_source()

    manager = Manager(create_app)
    manager.run()


if __name__ == "__main__":
    main()
