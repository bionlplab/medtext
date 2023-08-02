from io import StringIO

import pandas as pd

from medtext_conv.models import csv2bioc

CSV_STR = """
note_id,note_text
00000086,"findings: pa and lat cxr at 7:34 p.m.. heart and mediastinum are
stable. lungs are unchanged. air- filled cystic changes. no
pneumothorax. osseous structures unchanged scoliosis
impression: stable chest.
dictating"
00019248,"findings:
chest: four images:
right picc with tip within the upper svc.
probable enlargement of the main pulmonary artery.
mild cardiomegaly.
no evidence of focal infiltrate, effusion or pneumothorax.
dictating"
,x
x,
,
"""


def test_csv2bioc():
    df = pd.read_csv(StringIO(CSV_STR), dtype=str)
    collection = csv2bioc.csv2bioc(df, 'note_id', 'note_text')
    assert len(collection.documents) == 2

    for i in range(0, 2):
        assert collection.documents[i].passages[0].text == df['note_text'][i]
