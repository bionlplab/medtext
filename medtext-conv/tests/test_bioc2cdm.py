from medtext_conv.models.bioc_cdm_converter import convert_bioc_to_note_nlp
import bioc


XML_STR = """
<collection>
  <source></source>
  <date>2022-02-07</date>
  <key></key>
  <document>
    <id>00019248</id>
    <passage>
      <infon key="section_concept">findings_passage</infon>
      <offset>10</offset>
      <text>chest: four images:
right picc with tip within the upper svc.
probable enlargement of the main pulmonary artery.
mild cardiomegaly.
no evidence of focal infiltrate, effusion or pneumothorax.
dictating</text>
      <annotation id="a0">
        <infon key="note_nlp_concept_id">RID1243</infon>
        <infon key="note_nlp_concept">thorax</infon>
        <infon key="nlp_system">NER_Spacy:RadLex</infon>
        <infon key="nlp_date_time">02/11/2022, 01:13:39</infon>
        <infon key="lemma">thorax</infon>
        <infon key="section_concept">findings</infon>
        <location offset="10" length="5"/>
        <text>chest</text>
      </annotation>
      <annotation id="a1">
        <infon key="note_nlp_concept_id">RID1243</infon>
        <infon key="note_nlp_concept">thorax</infon>
        <infon key="nlp_system">NER_Spacy:RadLex</infon>
        <infon key="nlp_date_time">02/11/2022, 01:13:39</infon>
        <infon key="absent">True</infon>
        <location offset="10" length="5"/>
        <text>chest</text>
      </annotation>
      <annotation id="a2">
        <infon key="note_nlp_concept_id">RID1243</infon>
        <infon key="note_nlp_concept">thorax</infon>
        <infon key="nlp_system">NER_Spacy:RadLex</infon>
        <infon key="nlp_date_time">02/11/2022, 01:13:39</infon>
        <infon key="possible">True</infon>
        <location offset="10" length="5"/>
        <text>chest</text>
      </annotation>
    </passage>
  </document>
</collection>
"""


def test():
    collection = bioc.loads(XML_STR)
    df = convert_bioc_to_note_nlp(collection)
    assert len(df) == 3
    assert df.iloc[0]['offset'] == 10
    assert df.iloc[0]['note_nlp_concept_id'] == 'thorax'
    assert df.iloc[0]['section_concept_id'] == 'findings'

    assert df.iloc[1]['term_exists'] == 'Negation=True'
    assert df.iloc[1]['section_concept_id'] == 'findings_passage'

    assert df.iloc[2]['term_exists'] == 'Uncertain=True'


