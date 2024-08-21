from pymongo import MongoClient
from neo4j import GraphDatabase
import streamlit as st
from update import update_data1

# Streamlit UI
st.markdown("<h1 style='text-align: ; color: orange;'>Update Patient Record</h1>", unsafe_allow_html=True)

import streamlit as st

# Streamlit UI for updating Patient node
def update_patient_ui():
    st.subheader("Update Patient Information")
    patient_id = st.number_input("Patient ID")
    update_data = {}
    if st.checkbox("Update Dob"):
        update_data["dob"] = str(st.date_input("New Dob:"))
    if st.checkbox("Update Ethinicity"):
        update_data["ethinicity"] = st.text_input("Enter ethinicity")
    if st.checkbox("Update gender"):
        update_data["gender"] = st.selectbox("New Gender", ["Male", "Female", "Other"])
    if st.checkbox("Update insurance"):
        update_data["insurance"] = st.text_input("New Insurance")
    if st.checkbox("Update Language"):
        update_data['language'] = st.text_input("New language")
    if st.checkbox("Update Martial_status"):
        update_data['marital_status'] = st.text_input("New status")
    return patient_id, update_data

# Streamlit UI for updating HospitalAdmission node
def update_hospital_admission_ui():
    st.subheader("Update Hospital Admission Information")
    hadm_id = st.number_input("HADM ID")
    update_data = {}
    if st.checkbox("Update Admission Type"):
        update_data["admission_type"] = st.text_input("New Admission Type")
    if st.checkbox("Update Diagnosis"):
        update_data["diagnosis"] = st.text_input("New Diagnosis")
    if st.checkbox("Update Hospital Expire Flag"):
        update_data["hospital_expire_flag"] = st.text_input("New Hospital Expire Flag")
    if st.checkbox("Update Admission Time"):
        update_data["admittime"] = st.date_input("New Admission Time")
    if st.checkbox("Update Discharge Time"):
        update_data["dischtime"] = st.date_input("New Discharge Time")
    return hadm_id, update_data


# Streamlit UI for updating ICUStay node
def update_icu_stay_ui():
    st.subheader("Update ICU Stay Information")
    icustay_id = st.number_input("ICUStay ID")
    update_data = {}
    if st.checkbox("Update Intime"):
        update_data["intime"] = st.text_input("New Intime")
    if st.checkbox("Update Outtime"):
        update_data["outtime"] = st.text_input("New Outtime")
    return icustay_id, update_data

# Streamlit UI for updating Diagnosis node
def update_diagnosis_ui():
    st.subheader("Update Diagnosis Codes Information")
    row_id = st.number_input("Row ID")
    subject_id = st.number_input("Subject ID")
    hadm_id = st.number_input("HADM ID")
    update_data = {}
    if st.checkbox("Update Sequence Number"):
        update_data["seq_num"] = st.text_input("New Sequence Number")
    if st.checkbox("Update ICD9 Code"):
        update_data["icd9_code"] = st.text_input("New ICD9 Code")
    return row_id, subject_id, hadm_id, update_data



# Streamlit UI for updating Procedure node
def update_procedure_ui():
    st.subheader("Update Diagnosis Codes Information")
    row_id = st.number_input("Row ID")
    subject_id = st.number_input("Subject ID")
    hadm_id = st.number_input("HADM ID")
    update_data = {}
    if st.checkbox("Update Sequence Number"):
        update_data["seq_num"] = st.text_input("New Sequence Number")
    if st.checkbox("Update ICD9 Code"):
        update_data["icd9_code"] = st.text_input("New ICD9 Code")
    return row_id, subject_id, hadm_id, update_data



def main():
    node_name = st.selectbox("Select Node Type", ["Patient", "HospitalAdmission", "ICUStay", "Diagnosis", "Procedure"])
    
    if node_name == "Patient":
        patient_id, update_data = update_patient_ui()
        if st.button("Submit Record"):
            print(type(patient_id),update_data)
            update_data1('patient_id',patient_id,'patients',update_data,'Patient','subject_id')
    elif node_name == "HospitalAdmission":
        hadm_id, update_data = update_hospital_admission_ui()
        if st.button("Submit Record"):
            update_data1('hadm_id',hadm_id,'admissions',update_data,'HospitalAdmission','hadm_id')
    elif node_name == "ICUStay":
        icustay_id, update_data = update_icu_stay_ui()
        if st.button("Submit Record"):
            update_data1('icustay_id',icustay_id,'icu',update_data,'ICUStay','icustay_id')
    elif node_name == "Diagnosis":
        hadm_id, update_data = update_diagnosis_ui()
        if st.button("Submit Record"):
            update_data1('hadm_id',hadm_id,'diagnoses',update_data,'Diagnosis','hadm_id')
    elif node_name == "Procedure":
        row_id, update_data = update_procedure_ui()
        if st.button("Submit Record"):
            update_data1('hadm_id',hadm_id,'procedures',update_data,'Procedure','hadm_id')

if __name__ == "__main__":
    main()