USER_SCHEMA = {
    "type": "object",
    "required": ["data"],
    "properties": {
        "data": {
            "type": "object",
            "required": ["id", "email", "first_name", "last_name"],
            "properties": {
                "id": {"type": "integer"},
                "email": {"type": "string", "format": "email"},
                "first_name": {"type": "string"},
                "last_name": {"type": "string"},
                "avatar": {"type": "string"}
            }
        }
    }
}

USERS_LIST_SCHEMA = {
    "type": "object",
    "required": ["data", "page", "per_page", "total"],
    "properties": {
        "page": {"type": "integer"},
        "per_page": {"type": "integer"},
        "total": {"type": "integer"},
        "data": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "email", "first_name", "last_name"]
            }
        }
    }
}

CREATE_USER_SCHEMA = {
    "type": "object",
    "required": ["name", "job", "id", "createdAt"],
    "properties": {
        "name": {"type": "string"},
        "job": {"type": "string"},
        "id": {"type": "string"},
        "createdAt": {"type": "string"}
    }
}

LOGIN_SCHEMA = {
    "type": "object",
    "required": ["token"],
    "properties": {
        "token": {"type": "string"}
    }
}
