import pymongo
import pandas as pd
import numpy as np
from update import update_data
from delete import delete_data
from read import read_patient

# MongoDB connection parameters
mongo_uri = 'mongodb+srv://Subash:Subash123@subash.kyyfnyo.mongodb.net/?retryWrites=true&w=majority&appName=Subash'
mongo_dbname = 'healthcare_db'
mongo_collection = 'procedures'

# Connect to MongoDB
client = pymongo.MongoClient(mongo_uri)
db = client[mongo_dbname]
collection = db[mongo_collection]

# Load data from CSV files
data = pd.read_csv(r'mimic-iii-clinical-database-demo-1.4\PROCEDURES_ICD.csv')
data.drop('row_id',axis=1)
"""data1 = pd.read_csv(r'mimic-iii-clinical-database-demo-1.4\PATIENTS.csv')

# Merge dataframes on 'subject_id'
merged_data = pd.merge(data, data1, on='subject_id', how='left')

# Insert data into MongoDB
for i in range(len(merged_data)):
    patient_data = {
        'patient_id': int(merged_data.iloc[i]['subject_id']),  # Convert numpy.int64 to int
        'dob': merged_data.iloc[i]['dob'],
        'gender': merged_data.iloc[i]['gender'],
        'ethnicity': merged_data.iloc[i]['ethnicity'],
        'insurance': merged_data.iloc[i]['insurance'],
        'language': merged_data.iloc[i]['language'],
        'marital_status': merged_data.iloc[i]['marital_status']
    }
    collection.insert_one(patient_data)

print('Patient data inserted successfully.')"""
def create_patient(subject_id, dob, gender, ethnicity, insurance, language, marital_status, dod=None):
    return {
        'subject_id': subject_id,
        'dob': dob,
        'gender': gender,
        'ethnicity': ethnicity,
        'insurance': insurance,
        'language': language,
        'marital_status': marital_status,
        'dod': dod
    }
def create_admission(hadm_id, subject_id, admittime, dischtime, admission_type, diagnosis, hospital_expire_flag):
    return {
        'hadm_id': hadm_id,
        'subject_id': subject_id,
        'admittime': admittime,
        'dischtime': dischtime,
        'admission_type': admission_type,
        'diagnosis': diagnosis,
        'hospital_expire_flag': hospital_expire_flag
    }
def create_icu_stay(icustay_id, hadm_id, subject_id, intime,outtime):
    return {
        'icustay_id': icustay_id,
        'hadm_id': hadm_id,
        'subject_id': subject_id,
        'intime': intime,
        'outtime': outtime,
    }
query_result = collection.find_one({'patient_id': 10006})
print('Query Result:')
print(query_result)
patient_data_2  = {
    'patient_id': 'P001',
    'dob': '1990-01-01',
    'gender': 'Female',
    'ethnicity': 'Asian',
    'insurance': 'Aetna',
    'language': 'English',
    'marital_status': 'Married'
}

#insert_data(patient_data_2,"patients",'Patients')

delete_data('patient_id','P001',"patients",'Patient','subject_id')
"""
delete_patient('patient_id',199998,"patients")
query_result = read_patient('patient_id',199998,"patients")
print('Query Result:')
print(query_result)
# Close MongoDB connection"""
diagnoses_data = data.to_dict(orient='records')

collection.insert_many(diagnoses_data)
client.close()
