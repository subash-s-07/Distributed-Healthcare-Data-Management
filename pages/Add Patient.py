from pymongo import MongoClient
from neo4j import GraphDatabase
from datetime import datetime
import random
import streamlit as st
from insert import insert_diagnosis,insert_hospital_admission,insert_icu_stay,insert_patient,insert_procedure

import streamlit as st

# Streamlit UI for Patient node
def patient_ui():
    st.subheader("Patient Information")
    subject_id = st.number_input("Subject ID")
    dob = st.text_input("Date of Birth")
    gender = st.text_input("Gender")
    ethnicity = st.text_input("Ethnicity")
    insurance = st.text_input("Insurance")
    language = st.text_input("Language")
    marital_status = st.text_input("Marital Status")
    return {
        "patient_id": subject_id,
        "dob": dob,
        "gender": gender,
        "ethnicity": ethnicity,
        "insurance": insurance,
        "language": language,
        "marital_status": marital_status
    }

# Streamlit UI for HospitalAdmission node
def hospital_admission_ui():
    st.subheader("Hospital Admission Information")
    hadm_id = st.number_input("HADM ID")
    subject_id = st.number_input("Subject ID")
    admittime = st.text_input("Admittime")
    dischtime = st.text_input("Dischtime")
    admission_type = st.text_input("Admission Type")
    diagnosis = st.text_input("Diagnosis")
    hospital_expire_flag = st.text_input("Hospital Expire Flag")
    return {
        "hadm_id": hadm_id,
        "subject_id": subject_id,
        "admittime": admittime,
        "dischtime": dischtime,
        "admission_type": admission_type,
        "diagnosis": diagnosis,
        "hospital_expire_flag": hospital_expire_flag
    }

# Streamlit UI for ICUStay node
def icu_stay_ui():
    st.subheader("ICU Stay Information")
    icustay_id = st.number_input("ICUStay ID")
    hadm_id = st.number_input("HADM ID")
    subject_id = st.number_input("Subject ID")
    intime = st.text_input("Intime")
    outtime = st.text_input("Outtime")
    return {
        "icustay_id": icustay_id,
        "hadm_id": hadm_id,
        "subject_id": subject_id,
        "intime": intime,
        "outtime": outtime
    }

# Streamlit UI for Diagnosis node
def diagnosis_ui():
    st.subheader("Diagnosis Information")
    row_id = st.text_input("Row ID")
    subject_id = st.number_input("Subject ID")
    hadm_id = st.number_input("HADM ID")
    seq_num = st.text_input("Seq Num")
    icd9_code = st.text_input("ICD9 Code")
    return {
        "row_id": row_id,
        "subject_id": subject_id,
        "hadm_id": hadm_id,
        "seq_num": seq_num,
        "icd9_code": icd9_code
    }

# Streamlit UI for Procedure node
def procedure_ui():

    st.subheader("Procedure Information")
    row_id = st.text_input("Row ID")
    subject_id = st.number_input("Subject ID")
    hadm_id = st.number_input("HADM ID")
    seq_num = st.text_input("Seq Num")
    icd9_code = st.text_input("ICD9 Code")
    return {
        "row_id": row_id,
        "subject_id": subject_id,
        "hadm_id": hadm_id,
        "seq_num": seq_num,
        "icd9_code": icd9_code
    }

# Example usage:
def main():
    node_name = st.selectbox("Select Node Type", ["Patient", "HospitalAdmission", "ICUStay", "Diagnosis", "Procedure"])
    
    if node_name == "Patient":
        data = patient_ui()
        if st.button("Submit Patients Record"):
            insert_patient(data)
    elif node_name == "HospitalAdmission":
        data = hospital_admission_ui()
        if st.button("Submit Hospital Admission Record"):
            insert_hospital_admission(data)
    elif node_name == "ICUStay":
        data = icu_stay_ui()
        # Insert data into MongoDB and Neo4j
        if st.button("Submit ICU Stay Record"):
            insert_icu_stay(data)
    elif node_name == "Diagnosis":
        data = diagnosis_ui()
        # Insert data into MongoDB and Neo4j
        if st.button("Submit Diagnosis Record"):
            insert_diagnosis(data)
    elif node_name == "Procedure":
        data = procedure_ui()
        # Insert data into MongoDB and Neo4j
        if st.button("Submit Procedure Record"):
            insert_procedure(data)

if __name__ == "__main__":
    main()
