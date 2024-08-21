from pymongo import MongoClient
from py2neo import Graph, Node, Relationship
import pymongo
mongo_uri = 'mongodb+srv://Subash:Subash123@subash.kyyfnyo.mongodb.net/?retryWrites=true&w=majority&appName=Subash'
mongo_db = 'healthcare_db'
mongo_patient_collection = 'patients'
mongo_admission_collection = 'admissions'
mongo_icu_collection = 'icu'
mongo_diagnosis_collection = 'diagnoses'
mongo_procedure_collection = 'procedures'

# Neo4j connection parameters
neo4j_host = 'bolt://localhost:7687'
neo4j_user = 'neo4j'
neo4j_password = '12345678'

# Connect to MongoDB
mongo_client = pymongo.MongoClient(mongo_uri)
mongo_db = mongo_client[mongo_db]
patients_collection = mongo_db[mongo_patient_collection]
admissions_collection = mongo_db[mongo_admission_collection]
icu_stays_collection = mongo_db[mongo_icu_collection]
diagnoses_collection = mongo_db[mongo_diagnosis_collection]
procedures_collection = mongo_db[mongo_procedure_collection]

# Connect to Neo4j
graph = Graph(neo4j_host, auth=(neo4j_user, neo4j_password))

# Retrieve data from MongoDB collections
patients_data = patients_collection.find()
admissions_data = admissions_collection.find()
icu_stays_data = icu_stays_collection.find()
diagnoses_data = diagnoses_collection.find()
procedures_data = procedures_collection.find()
print(icu_stays_data )
print(procedures_data)
"""# Create nodes in Neo4j for patients, hospital admissions, ICU stays, diagnoses, procedures
for patient in patients_data:
    patient_node = Node('Patient',
                        subject_id=patient['patient_id'],
                        dob=patient['dob'],
                        gender=patient['gender'],
                        ethnicity=patient['ethnicity'],
                        insurance=patient['insurance'],
                        language=patient['language'],
                        marital_status=patient['marital_status'])
    graph.merge(patient_node, 'Patient', 'subject_id')

for admission in admissions_data:
    admission_node = Node('HospitalAdmission',
                          hadm_id=admission['hadm_id'],
                          subject_id=admission['subject_id'],
                          admittime=admission['admittime'],
                          dischtime=admission['dischtime'],
                          admission_type=admission['admission_type'],
                          diagnosis=admission['diagnosis'],
                          hospital_expire_flag=admission['hospital_expire_flag'])
    graph.merge(admission_node, 'HospitalAdmission', 'hadm_id')

for icu_stay in icu_stays_data:
    icu_stay_node = Node('ICUStay',
                         icustay_id=icu_stay['icustay_id'],
                         hadm_id=icu_stay['hadm_id'],
                         subject_id=icu_stay['subject_id'],
                         intime=icu_stay['intime'],
                         outtime=icu_stay['outtime'],)
    graph.create(icu_stay_node)

for diagnosis in diagnoses_data:
    diagnosis_node = Node('Diagnosis',
                          row_id=diagnosis['row_id'],
                          subject_id=diagnosis['subject_id'],
                          hadm_id=diagnosis['hadm_id'],
                          seq_num=diagnosis['seq_num'],
                          icd9_code=diagnosis['icd9_code'])
    graph.create(diagnosis_node)

for procedure in procedures_data:
    procedure_node = Node('Procedure',
                          row_id=procedure['row_id'],
                          subject_id=procedure['subject_id'],
                          hadm_id=procedure['hadm_id'],
                          seq_num=procedure['seq_num'],
                          icd9_code=procedure['icd9_code'])
    graph.create(procedure_node)
"""
# Create relationships in Neo4j
"""for admission in admissions_data:
    patient_node = graph.nodes.match('Patient', subject_id=admission['subject_id']).first()
    admission_node = graph.nodes.match('HospitalAdmission', hadm_id=admission['hadm_id']).first()
    admission_relation = Relationship(patient_node, 'HAD_ADMISSION', admission_node)
    graph.merge(admission_relation)
"""
"""for icu_stay in icu_stays_data:
    admission_node = graph.nodes.match('HospitalAdmission', hadm_id=icu_stay['hadm_id']).first()
    icu_stay_node = graph.nodes.match('ICUStay', icustay_id=icu_stay['icustay_id']).first()
    if admission_node and icu_stay_node and admission_node['hadm_id'] == icu_stay_node['hadm_id']:
        icu_stay_relation = Relationship(admission_node, 'HAD_ICU_STAY', icu_stay_node)
        graph.merge(icu_stay_relation)"""

"""for diagnosis in diagnoses_data:
    admission_node = graph.nodes.match('HospitalAdmission', hadm_id=diagnosis['hadm_id']).first()
    diagnosis_node = graph.nodes.match('Diagnosis', hadm_id=diagnosis['hadm_id'],seq_num=diagnosis['seq_num']).first()
    print(diagnosis_node)
    if admission_node and diagnosis_node and admission_node['hadm_id'] == diagnosis['hadm_id']:
        diagnosed_with_relation = Relationship(admission_node, 'DIAGNOSED_WITH', diagnosis_node)
        graph.merge(diagnosed_with_relation)"""

for procedure in procedures_data:
    admission_node = graph.nodes.match('HospitalAdmission', hadm_id=procedure['hadm_id']).first()
    procedure_node = graph.nodes.match('Procedure', hadm_id=procedure['hadm_id'],seq_num=procedure['seq_num']).first()
    if admission_node and procedure_node and admission_node['hadm_id'] == procedure['hadm_id']:
        performed_procedure_relation = Relationship(admission_node, 'PERFORMED_PROCEDURE', procedure_node)
        graph.merge(performed_procedure_relation)

# Commit changes
graph.commit()

# Close connections
mongo_client.close()
