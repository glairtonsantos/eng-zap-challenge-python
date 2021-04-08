import os
from dotenv import load_dotenv

from eng_zap_challenge_python import app
from eng_zap_challenge_python.client import source_client


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


def main():
    load_dotenv()  # take environment variables from .env.
    DEBUG = str2bool(os.environ.get("DEBUG", "False"))

    if not source_client.data_source:
        source_client.load_data_source()

    app.run(debug=DEBUG)


if __name__ == "__main__":
    main()
