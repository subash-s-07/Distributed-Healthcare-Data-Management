from pymongo import MongoClient
from neo4j import GraphDatabase
import streamlit as st
from delete import delete_data
# Streamlit UI
st.markdown("<h1 style='text-align: ; color: orange;'>Delete Patient Record</h1>", unsafe_allow_html=True)

patient_id = st.number_input("Patient ID:")

if st.button("Delete_Patient"):
    if patient_id:
        delete_data('patient_id',patient_id,'patients','Patient','subject_id')
        st.success("Patient record deleted successfully.")
    else:
        st.error("Please provide the patient ID.")
patient_id = st.number_input("Hmadd ID:")

if st.button("Delete_Addmision"):
    if patient_id:
        delete_data('subejct_id',patient_id,'admissions','HospitalAdmission','hadm_id')
        st.success("Patient record deleted successfully.")
    else:
        st.error("Please provide the patient ID.")
