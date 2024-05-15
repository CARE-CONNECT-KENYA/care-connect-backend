import os

class Config():
    DEBUG = True
    TESTING = True
    CSRF_ENABLED = True
    SECTRET_KEY = "careconnect@dev-inshi"
    

class Development(Config):
    DEBUG = True
    TESTING = True

class Production(Config):
    DEBUG = False
    TESTING = False

class Testing(Config):
    DEBUG = True
    TESTING = True


app_config = {
    "development" : Development(),
    "testing" : Testing(),
    "production" : Production()
}

