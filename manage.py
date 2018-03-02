"""Main entry point into the MoonTracker application.

usage: manage.py [-h] [-p PORT] [--prod]

optional arguments:
    -h, --help      show this help message and exit
    -p PORT         have Flask listen on the specified port number
                    [default: 5000]
    --prod          use production environment, as opposed to development
"""

import argparse

from moontracker.app import create_app
from moontracker.config import DevConfig, ProdConfig


def parse():
    """Parse system arguments."""
    parser = argparse.ArgumentParser(description="Main entry point into \
                                     the MoonTracker application")
    parser.add_argument('-p', dest='port', action='store', default=5000,
                        type=int, help='have Flask listen on the specified \
                        port number [default: 5000]')
    parser.add_argument('--prod', action='store_true', help='use production \
                        environment, as opposed to development')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse()

    config = ProdConfig if args.prod else DevConfig

    app = create_app(config)
    app.run(host='0.0.0.0', port=args.port)
