import schedule
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os 
import datetime

from backend.adapter_collection import AdapterCollection
from backend.errors import *

engine = create_engine(os.environ["DATABASE_URL"])
Session = sessionmaker(bind=engine)
adapters = AdapterCollection(Session)

def clean_expired_tokens():
    today = datetime.datetime.now()
    print("Cleaning Tokens")
    try:
        access_tokens = adapters.access_token_adapter.get_access_tokens()
        for token in access_tokens:
            if token['expiration_date'] < today:
                adapters.access_token_adapter.delete_access_token(token['id'])
    except Exception as e:
        print(e)

def clean_unset_accounts():
    print("Cleaning Unset Accounts")


schedule.every().day.at("00:00").do(clean_expired_tokens)
schedule.every().sunday.at("00:00").do(clean_unset_accounts)

while True:
    schedule.run_pending()
    time.sleep(1)
