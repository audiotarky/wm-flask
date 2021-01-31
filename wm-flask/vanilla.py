"""Verification of WM payments via Vanilla and associated Exception."""
from flask import Flask

import requests
from requests.auth import HTTPBasicAuth

from util import get_config

from werkzeug.exceptions import HTTPException

CONFIG = get_config()

def prove(request, app):
    """
    Prove that a WM payment has occurred.

    request is the deserialised JSON WM receipt object
    """
    try:
        request_id = request['requestId']
        query = f'''{{
        proof(requestId: "{request_id}") {{
            total
            rate
            metadata{{
            requestId
            clientId
            contentId
            }}
        }}
    }}'''  # noqa: Q001
        app.logger.info(f'query: {query}')

        response = requests.post(
            CONFIG['vanilla']['API_URL'],
            json={'query': query},
            headers= {
                'Content-Type': 'application/json',
            },
            auth=HTTPBasicAuth(CONFIG['vanilla']['ID'], CONFIG['vanilla']['SECRET'])
        )
        response.raise_for_status()
        proof = response.json()
        app.logger.info(f'proof: {proof}')
        if proof['data']['proof']['metadata']:
            return proof['data']['proof']
    except Exception as e:
        app.logger.info(e)
    return False
