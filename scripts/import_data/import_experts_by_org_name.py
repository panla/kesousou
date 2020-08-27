import argparse
import json
import os
import sys

import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', type=str, required=True)
args = parser.parse_args()
input_dir = args.input
if not os.path.isdir(input_dir):
    sys.exit(1)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from model.models import Expert


def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.loads(f.read())


def get_names(input_dir):
    data_dir = input_dir
    orgs = os.listdir(data_dir)
    for org in orgs:
        org_dir = os.path.join(data_dir, org)
        experts = os.listdir(org_dir)
        for expert in experts:
            yield org, expert


if __name__ == '__main__':
    if not os.path.isdir(input_dir):
        raise Exception('input_dir is not a dir')
    for org, expert in get_names(input_dir):
        expert = Expert.objects.get_or_create(name=expert, organization=org)
        print(f'完成创建expert, id:{expert[0].id}')
