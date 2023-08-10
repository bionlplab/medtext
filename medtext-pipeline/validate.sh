export PYTHONPATH=$PYTHONPATH:src
examples='medtext-examples'
$output='$output'

[ -d $$output ] || mkdir $$output

# download models
python src/medtext/cmd/download.py all
# data preparation
medtext-csv2bioc -i $examples/ex1.csv -o $output/ex1.xml
medtext-cdm2bioc -i $examples/ex2.csv -o $output/ex2.xml
# deid
medtext-deid --repl=X -i $examples/ex3.xml -o $output/ex3.deid_philter.xml
# split section
medtext-secsplit reg -i $examples/ex4.xml -o $output/ex4.secsplit_regex.xml
medtext-secsplit medspacy -i $examples/ex4.xml -o $output/ex4.secsplit_medspacy.xml
# preprocess
medtext-preprocess spacy -i $examples/ex4.secsplit_medspacy.xml -o $output/ex4.preprocess_spacy.xml
medtext-preprocess stanza -i $examples/ex4.secsplit_medspacy.xml -o $output/ex4.preprocess_stanza.xml
# ssplit
medtext-ssplit -i $examples/ex4.secsplit_medspacy.xml -o $output/ex4.ssplit.xml
# parse
medtext-parse -i $examples/ex4.ssplit.xml -o $output/ex4.parse.xml
# convert constituency tree to dependencies
medtext-tree2dep -i $examples/ex4.parse.xml -o $output/ex4.depparse_billp.xml
# ner
medtext-ner regex --phrase medtext/resources/chexpert_phrases.yml -i $examples/ex4.secsplit_medspacy.xml -o $output/ex4.ner_regex.xml
medtext-ner spacy --radlex medtext/resources/Radlex4.1.xlsx -i $examples/ex4.secsplit_medspacy.xml -o $output/ex4.ner_radlex.xml
# neg
#medtext-neg --ngrex_negation medtext/resources/patterns/ngrex_negation.yml \
#  --regex_patterns medtext/resources/patterns/regex_patterns.yml \
#  -i $examples/ex4.secsplit_medspacy.xml \
#  -o $output/ex4.ner_radlex.xml
# convert bioc to note_nlp table
medtext-bioc2cdm -i $examples/ex4.depparse_billp.xml -o $output/ex4.deparser_billp.csv