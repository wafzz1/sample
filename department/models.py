from flask import Flask,request,jsonify
from mongoengine import *
import traceback
import json
class departmentdetails(Document):
    department_id=StringField(default="")
    department_name=StringField(default="")
    department_code=StringField(default="")
