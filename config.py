import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'postgresql://postgres:Vignesha16**@localhost/Company'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
