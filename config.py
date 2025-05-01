import os

REDIS_CHANNEL = os.environ.get('REDIS_CHANNEL', 'chat')
REDIS_CLIENTS_KEY = os.environ.get('REDIS_CLIENTS_KEY', 'active_clients')
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)