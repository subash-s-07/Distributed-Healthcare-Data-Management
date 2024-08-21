from py2neo import Graph
import pymongo

# Neo4j connection parameters
neo4j_host = 'bolt://localhost:7687'
neo4j_user = 'neo4j'
neo4j_password = '12345678'

# Connect to Neo4j
graph = Graph(neo4j_host, auth=(neo4j_user, neo4j_password))

# MongoDB connection parameters
mongo_uri = 'mongodb+srv://Subash:Subash123@subash.kyyfnyo.mongodb.net/?retryWrites=true&w=majority&appName=Subash'
mongo_dbname = 'healthcare_db'

# Connect to MongoDB
client = pymongo.MongoClient(mongo_uri)
db = client[mongo_dbname]

# Delete operation for MongoDB and Neo4j, including related nodes in Neo4j
def delete_data(primary_id, primary_value, mongo_collection, node_label, neo4j_property):
    # Delete in MongoDB
    collection = db[mongo_collection]
    result = collection.delete_many({str(primary_id): primary_value})
    print(f'Data deleted successfully in MongoDB. Deleted count: {result.deleted_count}')
    
    # Delete related nodes and relationships in Neo4j
    cypher_query = f"MATCH (n:{node_label}) WHERE n.{neo4j_property} = {primary_value} DETACH DELETE n"
    print(cypher_query)
    graph.run(cypher_query)
    print(f'Data deleted successfully in Neo4j.')
