import os

from dotenv import load_dotenv

load_dotenv()

project_root = os.path.join(os.path.dirname(__file__), ".")

username = os.getenv("skype_username")
password = os.getenv("skype_password")
