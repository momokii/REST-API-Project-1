template = {
    "swagger": "2.0",
    "info": {
        "title": "Kasir API",
        "description": "API buat proyek pemrograman mobile",
        "contact": {
            "responsibleOrganization": "",
            "responsibleDeveloper": "",
            "email": "",
            "url": "https://medium.com/@kelanach",
        },
        "termsOfService": "https://github.com/momokii/REST-API-Project-1",
        "version": "1.0"
    },
    "basePath": "/api",  # base bash for blueprint registration
    "schemes": [
        "http",
        "https"
    ],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    },
}

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/"
}