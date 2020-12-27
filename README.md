# wm-flask

This simple server provides a route to a `/session` endpoint & a `/session.js` to present the necessary session creation javascript.

## Setup

```
python3 -m venv venv
pip install -r requirements.txt
# For development
pre-commit install
```

This will set up a pre-commit hook, whichis equivalent to running `pre-commit run -a`.

## Configuration

The server is configured in `server_config.ini`. It has two sections, one `[vanilla]` to hold your information about your [Vanilla proxy](https://vanilla.so/). You should only need change `ID` & `SECRET`. The other holds a long `SECRET` used to seed the encrypted session data. This can be any long string - a UUID is a good choice which requires little thought.

```ini
[vanilla]
ID = YOURID
SECRET = YOURSECRET
POINTER_ROOT = $wm.vanilla.so/pay/
API_URL = https://wm.vanilla.so/graphql

[flask]
SECRET = SESSION_SECRET
```

## Coming soo

Supporting the [WM.org receipt verifier](https://webmonetization.org/docs/receipt-verifier).
