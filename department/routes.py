from flask import Flask,request,jsonify
from mongoengine import *
import traceback
import json
from hsptl import hsptl
from department.models import departmentdetails

@hsptl.route('/create/department',methods=["POST"])
def createdepartment():
    try:
        print(request.get_json())
        rs=request.get_json()
        department_name=rs.get("dpname")
        department_code=rs.get("code")
        print(department_name)
        print(department_code)
        department_data=departmentdetails(department_name=department_name,department_code=department_code).save()
        department_data.department_id=str(department_data.id)
        department_data.save()

        return {"description":"department created","status":True}
    except Exception as e:
        print(e)
        traceback.print_exc()
        # logging.error('Exception occurred: %s', e, exc_info=True)
        return {"description":str(e),"status":False,"status_code":304}