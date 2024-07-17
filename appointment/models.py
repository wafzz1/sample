from flask import Flask,request,jsonify
from mongoengine import *
import traceback
import json
class appointmentdetails(Document):
    appointment_id=StringField(default="")
    appointment_date=StringField(default="")
    appointment_no=StringField(default="")
    slot=StringField(default="")