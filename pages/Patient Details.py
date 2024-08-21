import streamlit as st
from neo4j import GraphDatabase
import pandas as pd
from py2neo import Graph
st.markdown("<h1 style='text-align:; color: orange;'>Patient Viewer</h1>", unsafe_allow_html=True)
neo4j_host = 'bolt://localhost:7687'
neo4j_user = 'neo4j'
neo4j_password = '12345678'

# Connect to Neo4j
graph = Graph(neo4j_host, auth=(neo4j_user, neo4j_password))

def get_diagnoses_and_procedures(patient_subject_id):
    cypher_query = """
    MATCH (patient:Patient{subject_id: $subject_id})-[:HAD_ADMISSION]->(admission:HospitalAdmission)
    OPTIONAL MATCH (admission)-[:DIAGNOSED_WITH]->(diagnosis:Diagnosis)
    OPTIONAL MATCH (admission)-[:PERFORMED_PROCEDURE]->(procedure:Procedure)
    OPTIONAL MATCH (admission)-[:HAD_ICU_STAY]->(i:ICUStay)
    RETURN patient.subject_id AS patient_id, admission.hadm_id AS admission_id, diagnosis, procedure,i.icustay_id AS icu_id
    """
    result = graph.run(cypher_query, subject_id=patient_subject_id).data()
    return result
patient_id = st.number_input("Enter Patient ID:")
patient_subject_id =int(patient_id)


# Input field for patient ID

if st.button("Fetch Relations"):
    result = get_diagnoses_and_procedures(patient_subject_id)
    if result:
        df = pd.DataFrame(result)
        transformed_df = df.groupby(['patient_id', 'admission_id','icu_id']).first().reset_index()
        def get_corresponding_value_diag(col1_val, col2_val, col3_val):
            result = df[(df['patient_id'] == col1_val) & (df['admission_id'] == col2_val) & (df['icu_id'] == col3_val)]['diagnosis']
            if result is None:
                return pd.DataFrame() 
            nodes_dict_list = []
            for node in result:
                try:
                    nodes_dict_list.append(dict(node))
                except:
                    pass
            d1 = pd.DataFrame(nodes_dict_list)
            try:
                d1= d1[['hadm_id', 'icd9_code', 'row_id', 'seq_num', 'subject_id']]
            except:
                pass
            return d1
        def get_corresponding_value_proc(col1_val, col2_val, col3_val):
            result = df[(df['patient_id'] == col1_val) & (df['admission_id'] == col2_val) & (df['icu_id'] == col3_val)]['procedure']
            if result is None:
                return pd.DataFrame() 
            nodes_dict_list = []
            for node in result:
                try:
                    nodes_dict_list.append(dict(node))
                except:
                    pass
            d1 = pd.DataFrame(nodes_dict_list)
            try:
                d1= d1[['hadm_id', 'icd9_code', 'row_id', 'seq_num', 'subject_id']]
            except:
                pass
            return d1
        for i in range(len(transformed_df)):
            diag=get_corresponding_value_diag(transformed_df.iloc[i]['patient_id'],transformed_df.iloc[i]['admission_id'],transformed_df.iloc[i]['icu_id'])
            proc=get_corresponding_value_proc(transformed_df.iloc[i]['patient_id'],transformed_df.iloc[i]['admission_id'],transformed_df.iloc[i]['icu_id'])
            st.write(f"Patient ID: {transformed_df.iloc[i]['patient_id']}, Admission ID: {transformed_df.iloc[i]['admission_id']}, ICU ID: {transformed_df.iloc[i]['icu_id']}")
            st.subheader("Diagnosis Data")
            st.table(diag)
            st.subheader("Procedure Data")
            st.table(proc)
    else:
        st.write('No Data Found')
