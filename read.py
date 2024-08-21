from py2neo import Graph
import pandas as pd

# Neo4j connection parameters
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

# Example usage: Get diagnoses and procedures for patient with subject ID 41795
patient_subject_id = 41795
result = get_diagnoses_and_procedures(patient_subject_id)

# Convert result to DataFrame
df = pd.DataFrame(result)
df.to_csv('1.csv')
# Transform the DataFrame to display repeated column data once
transformed_df = df.groupby(['patient_id', 'admission_id','icu_id']).first().reset_index()
# Display the transformed DataFrame
print(transformed_df)
def get_corresponding_value_diag(col1_val, col2_val, col3_val):
    result = df[(df['patient_id'] == col1_val) & (df['admission_id'] == col2_val) & (df['icu_id'] == col3_val)]['diagnosis']
    nodes_dict_list = [dict(node) for node in result]
    d1 = pd.DataFrame(nodes_dict_list)
    d1= d1[['hadm_id', 'icd9_code', 'row_id', 'seq_num', 'subject_id']]
    return d1
def get_corresponding_value_proc(col1_val, col2_val, col3_val):
    result = df[(df['patient_id'] == col1_val) & (df['admission_id'] == col2_val) & (df['icu_id'] == col3_val)]['procedure']
    nodes_dict_list = [dict(node) for node in result]
    d1 = pd.DataFrame(nodes_dict_list)
    d1= d1[['hadm_id', 'icd9_code', 'row_id', 'seq_num', 'subject_id']]
    return d1
for i in range(len(transformed_df)):
    diag=get_corresponding_value_diag(transformed_df.iloc[i]['patient_id'],transformed_df.iloc[i]['admission_id'],transformed_df.iloc[i]['icu_id'])
    proc=get_corresponding_value_diag(transformed_df.iloc[i]['patient_id'],transformed_df.iloc[i]['admission_id'],transformed_df.iloc[i]['icu_id'])
    print(diag)
    print(proc)
# Export transformed DataFrame to CSV file
transformed_df.to_csv('diagnoses_and_procedures_transformed.csv', index=False)

# Close Neo4j connection
graph.close()
