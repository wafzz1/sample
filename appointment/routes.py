from flask import Flask,request,jsonify
from mongoengine import *
import traceback
import json
from hsptl import hsptl
from appointment.models import appointmentdetails

@hsptl.route('/create/appointment',methods=["POST"])
def appointment():
    try:
        print(request.get_json())
        rs=request.get_json()
        appointment_date=rs.get("date")
        appointment_no=rs.get("number")
        slot=rs.get("slot")
        print(appointment_date)
        print(appointment_no)
        print(slot)
        appointment_data=appointmentdetails(appointment_date=appointment_date,appointment_no=appointment_no,slot=slot).save()
        appointment_data.appointment_id=str(appointment_data.id)
        appointment_data.save()

        return {"description":"appointment created","status":True}
    except Exception as e:
        print(e)
        traceback.print_exc()
        # logging.error('Exception occurred: %s', e, exc_info=True)
        return {"description":str(e),"status":False,"status_code":304}