#!/usr/bin/env python

import json
import random
from sys import stderr, exit
from os.path import isfile
from pprint import pprint

def main(args):
    if not isfile(args.ogs_snapshot):
        raise Exception(f'"{args.ogs_snapshot}" is not a file.')
    if not isfile(args.current_snapshot):
        raise Exception(f'"{args.current_snapshot}" is not a file.')
    buckets = list(filter(lambda x: isinstance(x, int) and x >= 0, args.buckets)) if args.buckets is not None else []
    if len(buckets) < 1:
        raise Exception('Must specify Buckets.')
    buckets.sort(reverse=True)

    with open(args.ogs_snapshot, 'r') as f:
        try:
            ogs_snapshot = json.loads(f.read())
        except:
            raise Exception(f'"{args.ogs_snapshot}" is not a valid JSON file.')
    with open(args.current_snapshot, 'r') as f:
        try:
            current_snapshot = json.loads(f.read())
        except:
            raise Exception(f'"{args.current_snapshot}" is not a valid JSON file.')
    
    ogs_owners = ogs_snapshot['owners']
    current_owners = current_snapshot['owners']
    ogs_addresses = ogs_owners.keys()

    owners_buckets = {}
    bucket_counts = {}

    for owner in ogs_addresses:
        original_count = len(ogs_owners[owner])
        current_count = len(current_owners.get(owner, []))
        for b in buckets:
            if original_count >= b and current_count >= b:
                owners_buckets[owner] = b
                bucket_counts[b] = bucket_counts.get(b, 0) + 1
                break
    if args.axis == 1:
        per_bucket = {}
        for b in buckets:
            per_bucket[b] = []
        for owner, bucket in owners_buckets.items():
            per_bucket[bucket].append(owner)
        return per_bucket, bucket_counts

    return owners_buckets, bucket_counts


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--ogs-snapshot", type=str, required=True)
    parser.add_argument("--current-snapshot", type=str, required=True)
    parser.add_argument("--buckets", type=int, action='append', required=True)
    parser.add_argument("--axis", type=int, default=0)
    parser.add_argument("-v" ,"--verbose", action='store_true')

    args = parser.parse_args()
    try:
        owners_buckets, bucket_counts = main(args)
        print('owners_buckets')
        pprint(owners_buckets)
        print('bucket_counts')
        pprint( bucket_counts)
        print('total ogs')
        pprint(sum(bucket_counts.values()))
    except Exception as e:
        stderr.write(f'{e}\n')
        exit(1)