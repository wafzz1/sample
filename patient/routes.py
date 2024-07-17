from flask import Flask,request,jsonify
from mongoengine import *
import traceback
import json
from hsptl import hsptl
from patient.models import patientdetails
from mongoengine.queryset.visitor import Q

@hsptl.route('/create/patient',methods=["POST"])
def createpatient():
    try:
        print(request.get_json())
        rs=request.get_json()
        patient_name=rs.get("pname")
        address=rs.get("address")
        patient_contact=rs.get("contact")
        patient_age=rs.get("age")
        print(patient_name)
        print(address)
        print(patient_contact)
        print(patient_age)
        patient_data=patientdetails(patient_name=patient_name,address=address,patient_contact=patient_contact,patient_age=patient_age).save()
        patient_data.patient_id=str(patient_data.id)
        patient_data.save()

        return {"description":"patient created","status":True}
    except Exception as e:
        print(e)
        traceback.print_exc()
        return {"description":str(e),"status":False,"status_code":304}

# Route for searching patients
@hsptl.route('/search/patient', methods=["POST"])
def search_patient():
    try:
        # Get search parameters from query string
        rs=request.get_json()
        age=rs.get("age")

        # Perform the search in MongoDB
        patients = patientdetails.objects(patient_age__lt=30).to_json()
        print(patients)
        newdata=json.loads(patients)
        return {"description":"patient datail","status":True,"data":newdata}

    except Exception as e:
        print(e)
        return jsonify({"description": str(e), "status": False}), 500


# Route for limiting patients
@hsptl.route('/limiting/patient', methods=["POST"])
def limiting_patient():
    try:
        # Get search parameters from query string
        rs=request.get_json()
        pname=rs.get("pname")

        # Perform the search in MongoDB
        patients = patientdetails.objects[:3].to_json()
        print(patients)
        newdata=json.loads(patients)
        return {"description":"patient datail","status":True,"data":newdata}

    except Exception as e:
        print(e)
        return jsonify({"description": str(e), "status": False}), 500


# Route for sorting patients 
@hsptl.route('/sort/patient', methods=["POST"])
def sort_patient():
    try:
        # Get search parameters from request JSON
        rs = request.get_json()
        pname = rs.get("pname")

        patients = patientdetails.objects(patient_name__icontains=pname).order_by('patient_name').to_json()
        newdata = json.loads(patients)
        
        return jsonify({"description": "patient details sorted by name", "status": True, "data": newdata})

    except Exception as e:
        print(e)
        return jsonify({"description": str(e), "status": False}), 500


# Route for groupby patients 
@hsptl.route('/groupby/patient', methods=["POST"])
def group_patient():
    try:
        # Get search parameters from request JSON
        rs = request.get_json()
        pname = rs.get("pname")

        # Query patients matching the name and group by age
        pipeline = [
            {"$match": {"patient_name": {"$regex": pname, "$options": "i"}}},
            {"$group": {"_id": "$age", "patients": {"$push": "$$ROOT"}}},
            {"$sort": {"_id": 1}}  # Optionally sort by age, remove if you want natural grouping
        ]

        patients = patientdetails.objects.aggregate(pipeline)

        # Convert aggregation cursor to list
        grouped_patients = list(patients)

        return jsonify({"description": "Patients grouped by age", "status": True, "data": grouped_patients})

    except Exception as e:
        print(e)
        return jsonify({"description": str(e), "status": False}), 500

@hsptl.route('/combining/patient', methods=["POST"])
def combining_patient():
    try:
        # Get search parameters from request JSON
        rs = request.get_json()
        pname = rs.get("pname")
        min_age = 18
        patients = patientdetails.objects(Q(patient_name__icontains=pname) | Q(patient_age__gte=min_age)).order_by('patient_name').to_json()
        newdata = json.loads(patients)
        
        return jsonify({"description": "patient details combined by name ang age", "status": True, "data": newdata})

    except Exception as e:
        print(e)
        return jsonify({"description": str(e), "status": False}), 500


@hsptl.route('/count/patient', methods=["POST"])
def count_patient():
    try:
        # Get search parameters from request JSON
        rs = request.get_json()
        pname = rs.get("pname")

        # Count of patients matching pname
        patients = patientdetails.objects(patient_name__icontains=pname).count()
        print(patients)
        return jsonify({"description": "patient details sorted by name", "status": True, "data": patients})
    except Exception as e:
        print(e)
        traceback.print_exc()
        return jsonify({"description": str(e), "status": False}), 500

@hsptl.route('/exclude/patient', methods=["POST"])
def exclude_patient():
    try:
        # Get search parameters from request JSON
        rs = request.get_json()
        pname = rs.get("pname")

        # Example using exclude() to exclude specific fields
        patients = patientdetails.objects(patient_name__icontains=pname).exclude('address').order_by('patient_name').to_json()

        newdata = json.loads(patients)
        
        return jsonify({"description": "patient excluded details  (excluding address and phone_number)", "status": True, "data": newdata})

    except Exception as e:
        print(e)
        return jsonify({"description": str(e), "status": False}), 500

@hsptl.route('/include/patient', methods=["POST"])
def include_patient():
    try:
        # Get search parameters from request JSON
        rs = request.get_json()
        pname = rs.get("pname")

        # Example using include() to include specific fields
        patients = patientdetails.objects(patient_name__icontains=pname).only('patient_name', 'patient_age').order_by('patient_name').to_json()

        newdata = json.loads(patients)
        
        return jsonify({"description": "patient details sorted by name (including patient_name and age)", "status": True, "data": newdata})

    except Exception as e:
        print(e)
        return jsonify({"description": str(e), "status": False}), 500