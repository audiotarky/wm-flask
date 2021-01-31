"""The server & javascript file."""
from flask import Flask, request, session

from util import PaymentRequired, get_config
import json

app = Flask(__name__)

CONFIG = get_config()
app.config['SECRET_KEY'] = CONFIG['flask']['SECRET']
app.config['VERIFY_SERVICE'] = CONFIG['verification'].get('VERIFY_SERVICE', 'vanilla')

if app.config['VERIFY_SERVICE'] == 'vanilla':
    from vanilla import prove
else:
    from webmon_org import prove


@app.route('/session', methods=['POST'])
def make_session():
    """Create a session if the client iw WM enabled."""
    app.logger.info(f'Verifying payments with {app.config["VERIFY_SERVICE"]}')

    receipt = request.get_json()
    app.logger.info(f'receipt: {receipt}')

    proof = prove(receipt, app)

    if proof:
        app.logger.info(f'Payment proven: {proof}')
        session['has_wm_client'] = receipt['receipt']
        return 'session created'
    else:
        raise PaymentRequired()


@app.route('/create_session.js', methods=['GET'])
def session_js():
    """Serve up the front end code to create the session."""
    return '''let loaded = false;
if (document.monetization) {
    document.monetization.addEventListener("monetizationprogress", ({ detail }) => {
        if (!loaded) {
            loaded = true
            requestId = detail.requestId
            console.log(detail)
            var authz = new Request("/session", { method: "POST", body: JSON.stringify(detail), headers: { "Content-Type": "application/json" } });
            fetch(authz)
        }
    })
}'''  # noqa: Q001



@app.route('/demo/<service>', methods=['GET'])
def demo(service='vanilla'):
    if service == 'vanilla':
        ilp='$wm.vanilla.so/pay/e5a34e66-5b0e-408a-bdd2-89f483c54a1a'
    else:
        ilp='$webmonetization.org/api/receipts/%24ilp.uphold.com%2FWRPFhabhyrxF'
    return f'''<html>
    <head>
    <title>Hello from {service}</title>
    <meta name="monetization" content="{ilp}">
    </head>
    <body>
    <h1>Hello from {service}</h1>
    <h2>{ilp}</h2>
    </body>
    <script src="/create_session.js"></script>
    </html>'''


if __name__ == '__main__':
    import logging
    app.logger.setLevel(logging.DEBUG)
    app.run(host='0.0.0.0', port=5000, debug=True)  # nosec
