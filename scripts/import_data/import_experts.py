import argparse
import json
import os

import django

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', type=str, required=True, help='数据文件夹')
args = parser.parse_args()
input_dir = args.input
if not os.path.isdir(input_dir):
    raise Exception('input_dir is not a dir')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django.setup()

from model.models import Expert

def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.loads(f.read())


def get_names():
    data_dir = input_dir
    orgs = os.listdir(data_dir)
    for org in orgs:
        org_dir = os.path.join(data_dir, org)
        experts = os.listdir(org_dir)
        for expert in experts:
            yield org, expert


if __name__ == '__main__':
    for org, expert in get_names():
        Expert.objects.get_or_create(name=expert, organization=org)
