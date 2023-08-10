import copy

import toml

PROJECTS = [
    "medtext-commons",
    "medtext-conv",
    "medtext-deid",
    "medtext-neg",
    "medtext-ner",
    "medtext-parse",
    "medtext-secsplit",
    "medtext-preprocess",
    "medtext-ssplit",
]

VERSION = '0.1.dev2'

if __name__ == '__main__':
    with open('pyproject-template.toml') as fp:
        data = toml.load(fp)

    for project in PROJECTS:
        print('Update', project)
        filepath = '../{}/pyproject.toml'.format(project)
        with open(filepath) as fp:
            data = toml.load(fp)
        data['project']['version'] = VERSION
        with open(filepath, 'w') as fp:
            toml.dump(data, fp)
