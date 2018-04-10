"""Main entry point into the MoonTracker application.

usage: start.py [-h] [-p PORT] [--prod]

optional arguments:
    -h, --help      show this help message and exit
    -p PORT         have Flask listen on the specified port number
                    [default: 5000]
    --prod          use production environment, as opposed to development
"""

import argparse

from moontracker.app import create_app
from moontracker.config import DevConfig, ProdConfig
from moontracker.extensions import db, socketio


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


def main():
    """Run the application with command line arguments."""
    args = parse()

    config = ProdConfig if args.prod else DevConfig
    config.set_recaptcha_keys()
    app = create_app(config)
    db.create_all()
    certfile = "/etc/letsencrypt/live/moontracker.xyz/fullchain.pem"
    keyfile = "/etc/letsencrypt/live/moontracker.xyz/privkey.pem"
    if not args.prod:
        socketio.run(
            app, 
            host='0.0.0.0', 
            port=args.port, 
            use_reloader=False)
    else:
        socketio.run(
            app, 
            host='0.0.0.0', 
            port=args.port, 
            use_reloader=False,
            certfile=certfile,
            keyfile=keyfile)


if __name__ == '__main__':
    main()
