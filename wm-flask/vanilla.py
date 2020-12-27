"""Verification of WM payments via Vanilla and associated Exception."""
from flask import Flask

import requests
from requests.auth import HTTPBasicAuth

from util import get_config

from werkzeug.exceptions import HTTPException

CONFIG = get_config()

app = Flask(__name__)

def prove(request):
    """Prove that a WM payment has occurred."""
    try:
        request_id = request.data.decode('utf-8')

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
        response = requests.post(
            CONFIG['vanilla']['APIURL'],
            json={'query': query},
            headers= {
                'Content-Type': 'application/json',
            },
            auth=HTTPBasicAuth(CONFIG['vanilla']['ID'], CONFIG['vanilla']['SECRET'])
        )
        response.raise_for_status()
        proof = response.json()
        if proof['data']['proof']['metadata']:
            return proof['data']['proof']
    except Exception as e:
        app.logger.info(e)
    return False
