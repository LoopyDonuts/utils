#!/usr/bin/env python

import json
import random
from sys import stderr, exit
from os.path import isfile

def main(args):
    if args.max_tokenid < 1:
        raise Exception(f'Max TokeId must be greater than 0.')
    if args.num_draws < 1:
        raise Exception(f'Number of draws must be greater than 0.')
    if args.num_shuffles < 1:
        raise Exception(f'Number of shuffles must be greater than 0.')
    if not isfile(args.snapshot_file):
        raise Exception(f'"{args.snapshot_file}" is not a file.')
    with open(args.snapshot_file, 'r') as f:
        try:
            snapshot = json.loads(f.read())
        except:
            raise Exception(f'"{args.snapshot_file}" is not a valid JSON file.')
    drawn = set()
    owners = snapshot['owners'].copy()
    for i in range(args.num_draws):
        entries_pool = []
        for holder, tokens in owners.items():
            for tokenid in tokens:
                if tokenid <= args.max_tokenid:
                    entries_pool.append(holder)
                    if args.equal_chance:
                        break
                else:
                    if args.verbose:
                        stderr.write(f'Skipping tokenId {tokenid} of holder {holder}\n')
        stderr.write(f'Shuffling entries {args.num_shuffles} times for draw #{i+1}\n')
        for j in range(args.num_shuffles):
            random.shuffle(entries_pool)
        choice = random.choice(entries_pool)
        print(f'Draw #{i+1} - {choice}')
        drawn.add(choice)
        owners.pop(choice)
    print('Drawn:', drawn)
    return drawn
        

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--max-tokenid", type=int, required=True)
    parser.add_argument("-n", "--num-draws", type=int, required=True)
    parser.add_argument("--num-shuffles", type=int, required=True)
    parser.add_argument("-s" ,"--snapshot-file", type=str, required=True)
    parser.add_argument("-v" ,"--verbose", action='store_true')
    parser.add_argument("-e" ,"--equal-chance", action='store_true')

    args = parser.parse_args()
    try:
        main(args)
    except Exception as e:
        stderr.write(f'{e}\n')
        exit(1)