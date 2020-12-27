"""The server & javascript file."""
from flask import Flask, request, session

from util import PaymentRequired, get_config
from vanilla import prove


app = Flask(__name__)

CONFIG = get_config()
app.config['SECRET_KEY'] = CONFIG['flask']['SECRET']


@app.route('/session', methods=['POST'])
def make_session():
    """Create a session if the client iw WM enabled."""
    proof = prove(request)
    if proof:
        session['clientId'] = proof['metadata']['clientId']
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
            var authz = new Request("/session", { method: "POST", body: requestId });
            fetch(authz)
        }
    })
}'''  # noqa: Q001


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # nosec
