from py2neo import Graph
import pymongo
# Neo4j connection parameters
neo4j_host = 'bolt://localhost:7687'
neo4j_user = ''
neo4j_password = ''

# Connect to Neo4j
graph = Graph(neo4j_host, auth=(neo4j_user, neo4j_password))

# MongoDB connection parameters
mongo_uri = ''
mongo_dbname = 'healthcare_db'

# Connect to MongoDB
client = pymongo.MongoClient(mongo_uri)
db = client[mongo_dbname]

# Update operation for MongoDB and Neo4j
def update_data1(primary_id, primary_value, mongo_collection, update_data, node_label, neo4j_property):
    # Update in MongoDB
    collection = db[mongo_collection]
    result = collection.update_many({str(primary_id): primary_value}, {'$set': update_data})
    print(f'Data updated successfully in MongoDB. Modified count: {result.modified_count}')
    
    # Update in Neo4j
    cypher_query = f"MATCH (n:{node_label}) WHERE n.{neo4j_property} = {primary_value} SET n += {{ {', '.join([f'{k}: "{v}"' for k, v in update_data.items()])} }}"
    print(cypher_query)
    graph.run(cypher_query)
    print(f'Data updated successfully in Neo4j.')