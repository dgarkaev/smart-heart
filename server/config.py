import os

ENVIRONMENT = os.getenv('ENVIRONMENT', 'prod')

# REDIS
redis_host='app-server'
redis_port=6379
redis_db = 0
redis_app='SmartHeart'
app_name = "SmartHeart"

#pcg
pcg_path='pcg'