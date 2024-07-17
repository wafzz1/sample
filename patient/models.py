from flask import Flask,request,jsonify
from mongoengine import *
import traceback
import json
class patientdetails(Document):
    patient_id=StringField(default="")
    patient_name=StringField(default="")
    address=StringField(default="")
    patient_contact=StringField(default="")
    patient_age=IntField(default="")