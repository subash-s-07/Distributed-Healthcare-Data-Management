import streamlit as st
from py2neo import Graph
import pandas as pd

# Neo4j connection parameters
neo4j_host = 'bolt://localhost:7687'
neo4j_user = 'neo4j'
neo4j_password = '12345678'

# Connect to Neo4j
graph = Graph(neo4j_host, auth=(neo4j_user, neo4j_password))

def run_cypher_query(query, params):
    result = graph.run(query, params)
    return result.data()

def display_patient_record_neo4j(data):
    query = "MATCH (P:Patient {subject_id: $subject_id}) RETURN P;"
    params = {"subject_id": data}
    return run_cypher_query(query, params)

def display_hospital_admission_record_neo4j(data):
    query = "MATCH (a:HospitalAdmission {hadm_id: $hadm_id}) RETURN a;"
    params = {"hadm_id": data}
    return run_cypher_query(query, params)

def display_icu_stay_record_neo4j(data):
    query = "MATCH (P:ICUStay {icustay_id: $icustay_id}) RETURN P;"
    params = {"icustay_id": data}
    return run_cypher_query(query, params)

def display_diagnosis_record_neo4j(data):
    query = "MATCH (d:Diagnosis {hadm_id: $hadm_id}) RETURN d;"
    params = {"hadm_id": data}
    return run_cypher_query(query, params)

def display_procedure_record_neo4j(data):
    query = "MATCH (p:Procedure {hadm_id: $hadm_id}) RETURN p;"
    params = {"hadm_id": data}
    return run_cypher_query(query, params)

def main():
    node_name = st.selectbox("Select Node Type", ["Patient", "HospitalAdmission", "ICUStay", "Diagnosis", "Procedure"])
    
    if node_name == "Patient":
        data = st.number_input("Subject ID")
        result = display_patient_record_neo4j(data)
    elif node_name == "HospitalAdmission":
        data = st.number_input("HADM ID")
        result = display_hospital_admission_record_neo4j(data)
    elif node_name == "ICUStay":
        data = st.number_input("ICUStay ID")
        result = display_icu_stay_record_neo4j(data)
    elif node_name == "Diagnosis":
        data = st.number_input("HADM ID")
        result = display_diagnosis_record_neo4j(data)
    elif node_name == "Procedure":
        data = st.number_input("HADM ID")
        result = display_procedure_record_neo4j(data)

    # Convert the dictionary result to a DataFrame
    if result:
        df = pd.DataFrame(result[0])
    else:
        df = pd.DataFrame({})
    # Display the DataFrame as a table
    st.table(df)

if __name__ == "__main__":
    main()
