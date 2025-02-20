# mongodb_client.py
from pymongo import MongoClient
from django.conf import settings

def get_mongodb_client():
    client = MongoClient('mongodb://localhost:27017/')
    return client

def get_db():
    client = get_mongodb_client()
    return client['bookstore']