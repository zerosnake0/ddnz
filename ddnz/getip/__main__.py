from __future__ import print_function
import sys
from .base import getip


def main(argv=sys.argv):
    import logging
    logging.basicConfig(level=logging.INFO)
    try:
        external_port, internal_port = map(int, argv[1:3])
    except Exception as e:
        print(e)
        print("Usage:", argv[0], "external_port", "internal_port")
        return

    d = getip(external_port, internal_port)
    print("The public IP is:")
    for k, v in d.items():
        print("{}: {}".format(k, v))


if __name__ == '__main__':
    main()
