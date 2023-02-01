
class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:qwerty@localhost:5432/university'


class TestingConfig(object):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:qwerty@localhost:5432/test_university'

