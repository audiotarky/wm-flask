import requests
from util import get_config
import json

CONFIG = get_config()
# Public API lives at https://webmonetization.org/api/receipts/verify
# Documentation https://webmonetization.org/docs/receipt-verifier/
# $webmonetization.org/api/receipts/%24ilp.uphold.com%2FWRPFhabhyrxF

def prove(receipt, app):
    try:
        response = requests.post(
            CONFIG.get('wm_org', 'API_URL', fallback='https://webmonetization.org/api/receipts/verify'),
            data=receipt['receipt'],
            headers= {
                'Content-Type': 'application/json',
            }
        )
        response.raise_for_status()
        proof = response.json()
        if proof['spspEndpoint'] == CONFIG.get('wm_org', 'TARGET_ILP'):
            return proof
    except requests.exceptions.HTTPError as e:
        app.logger.info(e)

    return False