#!/usr/bin/env python
# coding: utf-8

"""
Parse isc-dhcpd leases file and provides filtering by:

  active state
  ip address
  mac address
"""

import argparse
from pprint import pprint

import isc_parser.parser as parser


FILTERS = ("macaddr", "ipaddr", "active")


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("FILE", help="input isc-dhcpd leases file")
    p.add_argument("-f", "--filter", choices=FILTERS,
                   help="filter type")
    p.add_argument("-q", "--query", type=str,
                   help="query for some filter types (ipaddr, macaddr)")
    return p.parse_args()


def filter_ipaddr(leases, query):
    result = []
    for section in leases:
        _, ipaddr = section[0]
        if query in ipaddr:
            result.append(section)
    return result


def filter_macaddr(leases, query):
    result = []
    for section in leases:
        for items in section:
            for item in items:
                if "hardware" in item and "ethernet" in item:
                    if query in item.values[2]:
                        result.append(section)
    return result


def filter_active(leases, query="active"):
    result = []
    for section in leases:
        for items in section:
            for item in items:
                if "binding" in item and "state" in item:
                    if item.values[2] == query:
                        result.append(section)
    return result


def main():
    args = parse_args()

    fn = None
    if args.filter == "macaddr":
        fn = filter_macaddr
    elif args.filter == "ipaddr":
        fn = filter_ipaddr
    elif args.filter == "active":
        fn = filter_active

    data = parser.parse_file(args.FILE)
    results = fn(data, args.query)

    for result in results:
        pprint(result)


if __name__ == "__main__":
    main()
