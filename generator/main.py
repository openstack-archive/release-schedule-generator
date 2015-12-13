import argparse

import yaml


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('schedule')
    args = parser.parse_args()

    with open(args.schedule) as f:
        content = yaml.load(f)

    print(content)
