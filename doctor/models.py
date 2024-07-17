from flask import Flask,request,jsonify
from mongoengine import *
import traceback
import json
class doctordetails(Document):
    doctor_id=StringField(default="")
    doctor_name=StringField(default="")
    department=StringField(default="")
    doctor_contact=StringField(default="")