class Config:
    DEBUG = True
    DATABASE = {
        'host': 'localhost',
        'port': 5432,
        'user': 'admin',
        'password': 'secret123',
        'db_name': 'my_database'
    }
    OLLAMA= {
        "url": "http://host.docker.internal:11434/",
        # "url": "http://home.wujialei.com:11434/",
        "model": 'llama3.2:1b',
    }
    API = {
        'service_url': 'https://api.example.com',
        'api_key': 'abc123456789'
    }