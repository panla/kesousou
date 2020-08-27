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

from model.models import Expert, Patent


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
            expert_dir = os.path.join(org_dir, expert)
            patent_dir = os.path.join(expert_dir, 'patents')
            if os.path.isdir(patent_dir):
                files = os.listdir(patent_dir)
                for file in files:
                    yield org, expert, file, os.path.join(patent_dir, file)


if __name__ == '__main__':
    for org, expert_name, file, path in get_names():
        dic = read_json(path)
        original_id = file.replace('.json', '')
        expert = Expert.objects.filter(organization=org, name=expert_name).first()
        patent = Patent.objects.filter(original_id=original_id).first()
        if patent:
            pass
        else:
            dic['original_id'] = original_id
            try:
                patent = Patent.objects.create(**dic)
            except Exception as exc:
                print(exc, org, expert_name, file)
        try:
            expert.patents.add(patent)
        except Exception as exc:
            print(exc, org, expert_name, file)
