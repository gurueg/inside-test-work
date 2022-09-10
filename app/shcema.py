
USER_CREATE = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
        },

        "password": {
            "type": "string",
            "pattern": "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
        }
    },
    "required": ["name", "password"]
}

MESSAGE_CREATE = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
        },
        "message": {
            "type": "string"
        }
    },
    "required": ["name", "message"]
}
