import requests
import json
from qwen_agent.tools.base import BaseTool, register_tool

@register_tool('DuckDuckGo')
class DuckDuckGoTool(BaseTool):
    description = 'Access DuckDuckGo search and web content through MCP proxy'
    parameters = [{
        'name': 'operation',
        'type': 'string',
        'description': 'Operation to perform: web_search, fetch_url, url_metadata, felo_search',
        'required': True
    }, {
        'name': 'params',
        'type': 'object',
        'description': 'Parameters for the operation',
        'required': True
    }]

    def call(self, params: str | dict, **kwargs) -> str:
        # Handle both string and dictionary parameter formats
        if isinstance(params, str):
            try:
                params_dict = json.loads(params)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON string for parameters")
        else:
            params_dict = params
        
        # Extract operation
        if "operation" not in params_dict:
            raise ValueError("Missing 'operation' parameter")
        operation = params_dict['operation']
        
        operation_mapping = {
            'web_search': 'web-search',
            'fetch_url': 'fetch-url',
            'url_metadata': 'url-metadata',
            'felo_search': 'felo-search'
        }
        
        if operation not in operation_mapping:
            raise ValueError(f"Unsupported operation: {operation}")
        endpoint = operation_mapping[operation]
        
        # Extract parameters for the operation
        if 'params' in params_dict:
            payload = params_dict['params']
        else:
            # If there is no 'params' key, use all other parameters except 'operation'
            payload = {k: v for k, v in params_dict.items() if k != 'operation'}
        
        # For web-search operation, change 'q' to 'query'
        if operation == 'web_search' and 'q' in payload:
            payload['query'] = payload.pop('q')
        
        # Call MCP proxy endpoint
        url = f'http://host.docker.internal:8000/ddg-search/{endpoint}'
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.text
