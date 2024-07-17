from flask import Flask,request,jsonify
from mongoengine import *
import traceback
import json
from hsptl import hsptl
from doctor.models import doctordetails

@hsptl.route('/create/doctor',methods=["POST"])
def create():
    try:
        print(request.get_json())
        rs=request.get_json()
        doctor_name=rs.get("docname")
        department=rs.get("department")
        doctor_contact=rs.get("contact")
        print(doctor_name)
        print(department)
        print(doctor_contact)
        doctor_data=doctordetails(doctor_name=doctor_name,department=department,doctor_contact=doctor_contact).save()
        doctor_data.doctor_id=str(doctor_data.id)
        doctor_data.save()

        return {"description":"doctor created","status":True}
    except Exception as e:
        print(e)
        traceback.print_exc()
        logging.error('Exception occurred: %s', e, exc_info=True)
        return {"description":str(e),"status":False,"status_code":304}
