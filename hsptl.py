from flask import Flask,request,jsonify
from mongoengine import *
import traceback
import json
from flask import Blueprint
dbs=connect(db='hsptl', host='127.0.0.1', port=27017) #local
hsptl = Flask(__name__)

from doctor import routes
from patient import routes
from department import routes
from appointment import routes

if __name__ == "__main__":
    hsptl.run() 