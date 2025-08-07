import os
from dotenv import load_dotenv

load_dotenv()

print(f"ENV KEY: {os.environ.get('API_KEY')}")





