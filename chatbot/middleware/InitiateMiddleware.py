import json
from urllib.parse import quote_plus
from middleware.DatabaseMiddleware import DatabaseMiddleware
from datetime import datetime, timezone

def load_config():
    # Load configuration from file
    with open("chatbot/config.json", "r") as config_file:
        config = json.load(config_file)
        print("config values are", config)
        print("uri from config is", config.get("mongo_config", {}).get("uri"))
    
    required_keys = ["database_type"]
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Key '{key}' is missing in the config.json file.")
    
    return config

def escape_credentials(config):
    # Escape the username and password if they exist
    escaped_username = quote_plus(config.get("mongo_config", {}).get("username", ""))
    escaped_password = quote_plus(config.get("mongo_config", {}).get("password", ""))
    
    if "mongo_config" in config:
        if "username" in config["mongo_config"]:
            config["mongo_config"]["uri"] = config["mongo_config"]["uri"].replace(
                config["mongo_config"]["username"], escaped_username
            )
        if "password" in config["mongo_config"]:
            config["mongo_config"]["uri"] = config["mongo_config"]["uri"].replace(
                config["mongo_config"]["password"], escaped_password
            )

def create_db_middleware(config):
    # Create an instance of DatabaseMiddleware based on the configuration
    return DatabaseMiddleware(
        config.get("database_type", ""), 
        config.get("mongo_config", {}).get("uri", "")
    )

def query_mongodb(db_middleware, keyword_field, keyword_value,client_id):
    # Example query
    print(f"query the mongodb database with field name - '{keyword_field}'  value - '{keyword_value}' for clientID '{client_id}")
    results = db_middleware.execute_query(keyword_field, keyword_value,client_id)       
    return results

def process_results(results):
    result_values = []
    print(f"Total results '{results}'")
    for product in results:
        print(product)
        value = product.get("name")  # Replace "value" with the actual field name
        result_values.append(product)
        print(value)
    return result_values

def close_connection(db_middleware):
    # Close the connection
    db_middleware.close_connection()

def initiate_query_lookup(keyword_field, keyword_value,client_id):
    config = load_config()
    escape_credentials(config)
    
    db_middleware = create_db_middleware(config)

    results = query_mongodb(db_middleware, keyword_field, keyword_value, client_id)

    result_values = process_results(results)

    close_connection(db_middleware)
    print(f"results from the service query '{result_values}'")

    return result_values
def write_mongodb_servicelog(db_middleware, keyword_field, keyword_value):
    # Example query
    print(f"insert the mongodb database with field name - '{keyword_field}' and value - '{keyword_value}'")
    results = db_middleware.execute_servicelog_insert(keyword_field, keyword_value)       
    return results

def insert_to_servicelog(keyword_field, keyword_value):
    config = load_config()
    escape_credentials(config)
    
    db_middleware = create_db_middleware(config)

    results = write_mongodb_servicelog(db_middleware, keyword_field, keyword_value)

    result_values = process_results(results)

    close_connection(db_middleware)

    return result_values

def write_mongodb_botrequestlog(db_middleware, user_id, user_input, user_intent):
    # Example query
    # Get the current UTC time
    current_utc_time = datetime.utcnow().replace(tzinfo=timezone.utc)

    # Example query
    print(f"Inserting into 'botrequestlog' collection - User ID: {user_id}, User Input: {user_input}, User Intent: {user_intent}, Timestamp: {current_utc_time}")
    
    # Modify the following line based on the structure of your 'botrequestlog' documents
    document = {
        "user_id": user_id,
        "user_input": user_input,
        "user_intent": user_intent,
        "timestamp": current_utc_time
    }
    
    results = db_middleware.execute_botrequestlog_insert(document)
    
    return results
    # Modify the following line based on the structure of your 'botrequestlog' documents
    document = {"user_id": user_id, "user_input": user_input, "user_intent": user_intent}
    
    results = db_middleware.execute_botrequestlog_insert(document)
    
    return results

def insert_to_botrequestlog(user_id, user_input, user_intent):
    config = load_config()
    escape_credentials(config)
    
    db_middleware = create_db_middleware(config)

    results = write_mongodb_botrequestlog(db_middleware, user_id, user_input, user_intent)

    # You can choose whether or not to process and return results based on your requirements
    # result_values = process_results(results)

    close_connection(db_middleware)

    # Return any relevant information based on your application needs
    return results

# If this script is run directly
if __name__ == "__main__":
    initiate_query_lookup("keyword", "leaves",1)
    insert_to_botrequestlog('keyword','leave',"leaves-test")

