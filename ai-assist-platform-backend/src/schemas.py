from jsonschema import validate, ValidationError


schema_external = {
    "type": "object",
    "properties": {
        "nodes": {"type": "array"},
        "edges": {"type": "array"},
        "startNodeID": {"type": "string"}
    },
    "required": ["nodes", "edges", "startNodeID"]
}

schema_undefined = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "type": {"type": "string"},
        "data": {
            "type": "object",
            "properties": {
                "meta": {"type": "object"}
            },
            "required": ["meta"]
        }
    },
    "required": ["id", "type", "data"]
}

schema_var = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "type": {"type": "string"},
        "data": {
            "type": "object",
            "properties": {
                "meta": {
                    "type": "object",
                    "properties": {
                        "sourceOutputID": {"type": "string"}
                    },
                    "required": ["sourceOutputID"]
                },
                "var": {"type": "string"}
            },
            "required": ["meta", "var"]
        }
    },
    "required": ["id", "type", "data"]
}

schema_chain = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "type": {"type": "string"},
        "data": {
            "type": "object",
            "properties": {
                "meta": {
                    "type": "object",
                    "properties": {
                        "sourceOutputID": {"type": "string"},
                        "targetModelID": {"type": "string"},
                        "targetPromptID": {"type": "string"}
                    },
                    "required": ["sourceOutputID", "targetModelID", "targetPromptID"]
                }
            },
            "required": ["meta"]
        }
    },
    "required": ["id", "type", "data"]
}

schema_model = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "type": {"type": "string"},
        "data": {
            "type": "object",
            "properties": {
                "meta": {
                    "type": "object",
                    "properties": {
                        "sourceOutputID": {"type": "string"}
                    },
                    "required": ["sourceOutputID"]
                },
                "temperature": {"type": "number"},
                "top_p": {"type": "number"},
                "max_tokens": {"type": "integer"},
                "freq_penalty": {"type": "number"},
                "pres_penalty": {"type": "number"},
                "stop_seq": {"type": "string"},
                "api_key": {"type": "string"},
                "model_name": {"type": "string"}
            },
            "required": [
                "meta", "temperature", "top_p", "max_tokens",
                "freq_penalty", "pres_penalty", "stop_seq", "api_key", "model_name"
            ]
        }
    },
    "required": ["id", "type", "data"]
}

schema_visual = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "type": {"type": "string"},
        "data": {
            "type": "object",
            "properties": {
                "meta": {
                    "type": "object",
                    "properties": {
                        "targetInputID": {"type": "string"}
                    },
                    "required": ["targetInputID"]
                }
            },
            "required": ["meta"]
        }
    },
    "required": ["id", "type", "data"]
}

schema_websearch = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "type": {"type": "string"},
        "data": {
            "type": "object",
            "properties": {
                "meta": {
                    "type": "object",
                    "properties": {
                        "sourceOutputID": {"type": "string"}
                    },
                    "required": ["sourceOutputID"]
                },
                "api_key": {"type": "string"}
            },
            "required": ["meta", "api_key"]
        }
    },
    "required": ["id", "type", "data"]
}

schema_prompt = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "type": {"type": "string"},
        "data": {
            "type": "object",
            "properties": {
                "meta": {
                    "type": "object",
                    "properties": {
                        "sourceOutputID": {"type": "string"}
                    },
                    "patternProperties": {
                        "^[a-z0-9-_]+$": {"type": "string"}
                    },
                    "additionalProperties": False,
                    "required": ["sourceOutputID"]
                },
                "template": {"type": "string"},
                "prompt_values": {
                    "type": "object",
                    "patternProperties": {
                        "^[a-z0-9-_]+$": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "string"},
                                "name": {"type": "string"},
                                "value": {"type": "string"}
                            },
                            "required": ["id", "name", "value"]
                        }
                    },
                    "additionalProperties": False
                }
            },
            "required": ["meta", "template", "prompt_values"]
        }
    },
    "required": ["id", "type", "data"]
}

schema_edge = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "source": {"type": "string"},
        "target": {"type": "string"},
        "sourceHandle": {"type": "string"},
        "targetHandle": {"type": "string"}
    },
    "required": ["id", "source", "target", "sourceHandle", "targetHandle"]
}

# Словарь всех схем
schemas = {"external": schema_external, "undefined": schema_undefined, "var": schema_var, "chain": schema_chain, 
           "model": schema_model, "visual": schema_visual, "websearch": schema_websearch, "prompt": schema_prompt, "edge": schema_edge}

# Проверяет, соответствует ли json схеме
def is_valid_json(data, schema):
    try:
        validate(instance=data, schema=schema)
        return True
    except ValidationError as e:
        return "Incorrect data format: " + str(e.message) + "; Double-check this part of the data: " + str(data)
