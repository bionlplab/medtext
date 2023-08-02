from io import StringIO

import pytest

from medtext_conv.models.bioc_cdm_converter import convert_note_nlp_table_to_bioc, NOTE_TABLE_HEADERS
import pandas as pd


CSV_STR = """
note_id,person_id,note_date,note_datetime,note_type_concept_id,note_class_concept_id,note_title,note_text,encoding_concept_id,language_concept_id,provider_id,visit_occurrence_id,visit_detail_id,note_source_value
1,1,7/1/2039,7/1/2039 0:00,32834,0,0,The nail was then obtained.,0,0,0,1,0,Progress Note
2,1,7/2/2039,7/2/2039 0:00,32835,0,0,There is no pneumothorax.,0,0,0,2,0,XRAY CHEST 1 VIEW PORTABLE
3,1,7/3/2039,7/3/2039 0:00,32836,0,0,"The left internal jugular, subclavian, axillary and brachial veins are patent and compressible and have normal flow.",0,0,0,3,0,US VAS VEIN UP EXT LT
4,1,7/4/2039,7/4/2039 0:00,32837,0,0,The posterior fossa and brainstem are within normal limits.,0,0,0,4,0,NEURO CT HEAD BRAIN W/O CONTR
5,2,7/5/2039,7/5/2039 0:00,32838,0,0,NO GROWTH TO DATE,0,0,0,5,0,PRELIMINARY
6,2,7/6/2039,7/6/2039 0:00,32839,0,0,The liver is normal in size and contour.,0,0,0,6,0,FINAL REPORT
7,2,7/7/2039,7/7/2039 0:00,32840,0,0,The liver is normal in size and contour.,0,0,0,7,0,CT CHEST WO CONTRAST
8,2,7/8/2039,7/8/2039 0:00,32841,0,0,Normal GE junction was noted.,0,0,0,8,0,EGD PROCEDURE REPORT
"""


def test():
    df = pd.read_csv(StringIO(CSV_STR), dtype=str)
    collection = convert_note_nlp_table_to_bioc(df)
    assert len(collection.documents) == 8

    for i in range(8):
        print(collection.documents[i])
        assert collection.documents[i].text == df['note_text'][i]
        assert collection.documents[i].id == df['note_id'][i]

        for k in NOTE_TABLE_HEADERS:
            if k not in ('note_id', 'note_text'):
                assert collection.documents[i].infons[k] == df[k][i]


def test2():
    df = pd.read_csv(StringIO(CSV_STR), dtype=str)

    df1 = df.drop(['note_text'], axis=1)
    with pytest.raises(KeyError):
        convert_note_nlp_table_to_bioc(df1)

    df1 = df.drop(['note_type_concept_id'], axis=1)
    collection = convert_note_nlp_table_to_bioc(df1)
    assert len(collection.documents) == 8
