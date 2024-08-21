import pymongo
from py2neo import Graph, Node, Relationship
# Neo4j connection parameters
neo4j_host = 'bolt://localhost:7687'
neo4j_user = 'neo4j'
neo4j_password = '12345678'

# MongoDB connection parameters
mongo_uri = 'mongodb+srv://Subash:Subash123@subash.kyyfnyo.mongodb.net/?retryWrites=true&w=majority&appName=Subash'
mongo_dbname = 'healthcare_db'

# Connect to Neo4j
graph = Graph(neo4j_host, auth=(neo4j_user, neo4j_password))

# Connect to MongoDB
client = pymongo.MongoClient(mongo_uri)
db = client[mongo_dbname]

def insert_patient(data):
    collection = db['patients']
    result = collection.insert_one(data)
    print(f'Data inserted successfully into MongoDB collection patients. Inserted ID: {result.inserted_id}')

    patient_node = Node('Patient',
                        subject_id=data['patient_id'],
                        dob=data['dob'],
                        gender=data['gender'],
                        ethnicity=data['ethnicity'],
                        insurance=data['insurance'],
                        language=data['language'],
                        marital_status=data['marital_status'])
    graph.merge(patient_node, 'Patient', 'subject_id')

def insert_hospital_admission(data):
    collection = db['admissions']
    result = collection.insert_one(data)
    print(f'Data inserted successfully into MongoDB collection admissions. Inserted ID: {result.inserted_id}')

    admission_node = Node('HospitalAdmission',
                          hadm_id=data['hadm_id'],
                          subject_id=data['subject_id'],
                          admittime=data['admittime'],
                          dischtime=data['dischtime'],
                          admission_type=data['admission_type'],
                          diagnosis=data['diagnosis'],
                          hospital_expire_flag=data['hospital_expire_flag'])
    graph.merge(admission_node, 'HospitalAdmission', 'hadm_id')

    # Create relationship between Patient and HospitalAdmission
    patient_node = graph.nodes.match('Patient', subject_id=data['subject_id']).first()
    print(patient_node)
    print(admission_node)
    admission_relation = Relationship(patient_node, 'HAD_ADMISSION', admission_node)
    print(admission_relation)
    graph.merge(admission_relation)

def insert_icu_stay(data):
    collection = db['icu']
    result = collection.insert_one(data)
    print(f'Data inserted successfully into MongoDB collection icu. Inserted ID: {result.inserted_id}')

    icu_stay_node = Node('ICUStay',
                         icustay_id=data['icustay_id'],
                         hadm_id=data['hadm_id'],
                         subject_id=data['subject_id'],
                         intime=data['intime'],
                         outtime=data['outtime'])
    graph.merge(icu_stay_node, 'ICUStay', 'icustay_id')
    admission_node = graph.nodes.match('HospitalAdmission', hadm_id=data['hadm_id']).first()
    icu_stay_relation = Relationship(admission_node, 'HAD_ICU_STAY', icu_stay_node)
    print(icu_stay_relation)
    graph.merge(icu_stay_relation)

def insert_diagnosis(data):
    collection = db['diagnoses']
    result = collection.insert_one(data)
    print(f'Data inserted successfully into MongoDB collection diagnoses. Inserted ID: {result.inserted_id}')

    diagnosis_node = Node('Diagnosis',
                          row_id=data['row_id'],
                          subject_id=data['subject_id'],
                          hadm_id=data['hadm_id'],
                          seq_num=data['seq_num'],
                          icd9_code=data['icd9_code'])
    graph.merge(diagnosis_node, 'Diagnosis', 'row_id')

    # Create relationship between HospitalAdmission and Diagnosis
    admission_node = graph.nodes.match('HospitalAdmission', hadm_id=data['hadm_id']).first()
    diagnosis_relation = Relationship(admission_node, 'DIAGNOSED_WITH', diagnosis_node)
    graph.merge(diagnosis_relation)

def insert_procedure(data):
    collection = db['procedures']
    result = collection.insert_one(data)
    print(f'Data inserted successfully into MongoDB collection procedures. Inserted ID: {result.inserted_id}')

    procedure_node = Node('Procedure',
                          row_id=data['row_id'],
                          subject_id=data['subject_id'],
                          hadm_id=data['hadm_id'],
                          seq_num=data['seq_num'],
                          icd9_code=data['icd9_code'])
    graph.merge(procedure_node, 'Procedure', 'row_id')

    # Create relationship between HospitalAdmission and Procedure
    admission_node = graph.nodes.match('HospitalAdmission', hadm_id=data['hadm_id']).first()
    procedure_relation = Relationship(admission_node, 'PERFORMED_PROCEDURE', procedure_node)
    graph.merge(procedure_relation)
"""data_patient = {
    'patient_id': 'P003',
    'dob': '1990-01-01',
    'gender': 'Female',
    'ethnicity': 'Asian',
    'insurance': 'Aetna',
    'language': 'English',
    'marital_status': 'Married'
}

data_admission = {
    'hadm_id': 'A003',
    'subject_id': 'P003',
    'admittime': '2024-01-01',
    'dischtime': '2024-01-05',
    'admission_type': 'Emergency',
    'diagnosis': 'Pneumonia',
    'hospital_expire_flag': False
}
data_icu={
    "icustay_id":"I001",
                         "hadm_id":"A001",
                         "subject_id":"P001",
                         "intime":'2024-01-01',
                         "outtime": '2024-01-05'
}
data_diagnosis = {
    'row_id': 'D003',
    'subject_id': 'P003',
    'hadm_id': 'A003',
    'seq_num': 1,
    'icd9_code': '123.45'
}

data_procedure = {
    'row_id': 'PR003',
    'subject_id': 'P003',
    'hadm_id': 'A003',
    'seq_num': 1,
    'icd9_code': '678.90'
}

insert_patient(data_patient)
insert_icu_stay(data_icu)
insert_hospital_admission(data_admission)
insert_diagnosis(data_diagnosis)
insert_procedure(data_procedure)"""
