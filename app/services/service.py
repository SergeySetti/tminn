import os

from dotenv import load_dotenv
from injector import Module, provider, singleton
from pymongo import MongoClient
from dns import resolver

from app.db.mongodb import Db

load_dotenv()

# --- Start of DNS Fix ---
# In some environments (like Termux on Android), accessing /etc/resolv.conf is restricted.
# PyMongo's dependency `dnspython` needs a DNS server to resolve the hostname in the MONGODB_URI.
# We can manually configure it to use a public DNS server.
try:
    res = resolver.Resolver(configure=False)
    res.nameservers = ['8.8.8.8']
    resolver.default_resolver = res
except Exception as e:
    print(f"Error configuring DNS resolver: {e}")
# --- End of DNS Fix ---

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL')
OPENAI_WHISPER_MODEL = os.getenv('OPENAI_MODEL')

MONGODB_URI = os.getenv('MONGODB_URI')
WHISPER_AUDIO_FOLDER_PATH = os.getenv('WHISPER_AUDIO_FOLDER_PATH')
SUMMARIZER_MODEL = 'o3-mini'


class AppModule(Module):
    def configure(self, binder):
        binder.bind(MongoClient, to=MongoClient(MONGODB_URI), scope=singleton)

    @provider
    @singleton
    def provide_app_db(self, client: MongoClient) -> Db:
        return Db(client)
