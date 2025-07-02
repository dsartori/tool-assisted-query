import requests
import json
from qwen_agent.tools.base import BaseTool, register_tool

@register_tool('Wikipedia')
class WikipediaTool(BaseTool):
    description = 'Access Wikipedia information through MCPO proxy'
    parameters = [{
        'name': 'operation',
        'type': 'string',
        'description': 'Operation to perform: search, get_article, get_summary, etc.',
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
            # Parse input parameters if they come as a string
            params_dict = json.loads(params)
        else:
            params_dict = params
        
        # Extract operation and create payload from all other parameters
        operation = params_dict['operation']
        # Map the operation to the correct endpoint
        operation_mapping = {
            'search': 'search_wikipedia',
            'get_article': 'get_article',
            'get_summary': 'get_summary',
            'summarize_article_for_query': 'summarize_article_for_query',
            'summarize_article_section': 'summarize_article_section',
            'extract_key_facts': 'extract_key_facts',
            'get_related_topics': 'get_related_topics',
            'get_sections': 'get_sections',
            'get_links': 'get_links'
        }
        if operation not in operation_mapping:
            raise ValueError(f"Unsupported operation: {operation}")
        endpoint = operation_mapping[operation]
        
        # The 'params' key holds the parameters for the operation
        if 'params' in params_dict:
            payload = params_dict['params']
        else:
            # If there is no 'params' key, use all other parameters except 'operation'
            payload = {k: v for k, v in params_dict.items() if k != 'operation'}
        
        # Rename parameters to match proxy expectations
        if operation == 'search':
            if 'q' in payload:
                payload['query'] = payload.pop('q')
            if 'search' in payload:
                payload['query'] = payload.pop('search')
        
        # Call MCPO proxy endpoint
        url = f'http://host.docker.internal:8000/Wikipedia/{endpoint}'
        # Log the request for debugging
        print(f"Making request to: {url}")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.text
