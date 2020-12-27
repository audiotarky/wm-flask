"""Utility functions for the server."""
import configparser
import os
from pathlib import Path

from werkzeug.exceptions import HTTPException


def norm_path(path):
    """Normalise a path relative to where the code lives."""
    return Path(__file__).resolve().parent.parent / path


def get_config():
    """Read the application config ini file."""
    config = configparser.ConfigParser()
    cfg_path = os.environ.get('WM_CONFIG_FILE', norm_path('server_config.ini'))
    print(cfg_path)
    config.read(cfg_path)
    return config


class PaymentRequired(HTTPException):
    """Exception that directs users to Coil if not enabled."""

    code = 402

    def get_body(self, environ):
        """Return a message that people should use Coil."""
        return (
            f'{super().get_body(environ)}'
            '<p>Please consider supporting this site via'
            '<a href="https://coil.com">Coil</a>.</p>'
        )
