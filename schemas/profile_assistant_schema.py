from config.mongodb_config import connect_mongodb

db = connect_mongodb()

profile_assistant_meta_data = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["_id", "assistantName", "dateOfBirth", "chatHistory"],
        "properties": {
            "_id": {
                "bsonType": "string",
                "description": "Assistant ID or UUID (must be a string)",
            },
            "assistantName": {
                "bsonType": "string",
                "description": "Name of the assistant bot",
            },
            "dateOfBirth": {
                "bsonType": "string",
                "description": "Date of birth in YYYY-MM-DD format",
            },
            "chatHistory": {
                "bsonType": "array",
                "description": "List of chat sessions",
                "items": {
                    "bsonType": "object",
                    "required": ["_id", "history"],
                    "properties": {
                        "_id": {
                            "bsonType": "string",
                            "description": "Session ID or UUID",
                        },
                        "history": {
                            "bsonType": "array",
                            "description": "List of interaction pairs within the session",
                            "items": {
                                "bsonType": "object",
                                "required": [
                                    "request_id",
                                    "request",
                                    "requestTime",
                                    "response_id",
                                    "response",
                                    "responseTime",
                                ],
                                "properties": {
                                    "request_id": {
                                        "bsonType": "string",
                                        "description": "Unique ID for the request",
                                    },
                                    "request": {
                                        "bsonType": "string",
                                        "description": "User input message string",
                                    },
                                    "requestTime": {
                                        "bsonType": "string",
                                        "description": "ISO 8601 formatted timestamp",
                                    },
                                    "response_id": {
                                        "bsonType": "string",
                                        "description": "Unique ID for the response",
                                    },
                                    "response": {
                                        "bsonType": "string",
                                        "description": "Assistant reply message string",
                                    },
                                    "responseTime": {
                                        "bsonType": "string",
                                        "description": "ISO 8601 formatted timestamp",
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    }
}

db.create_collection("profile_assistant", validator=profile_assistant_meta_data)