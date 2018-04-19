from start import parse, main
from flask import current_app
from moontracker.extensions import scheduler
import sys

def test_parse_default():
    sys.argv = ['start.py']
    args = parse()

    assert args.port == 5000
    assert not args.prod


def test_parse_port():
    sys.argv = ['start.py', '-p', '50']
    args = parse()

    assert args.port == 50


def test_parse_prod():
    sys.argv = ['start.py', '--prod']
    args = parse()

    assert args.prod
