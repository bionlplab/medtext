# Negation Detection

```shell
Usage:
    medtext-neg negbio [--regex-patterns FILE --ngrex-patterns FILE --overwrite --sort-anns] -i FILE -o FILE
    medtext-neg prompt [--model-dir DIR --overwrite] -i FILE -o FILE
    medtext-neg download negbio [--regex-patterns FILE --ngrex-patterns FILE]
    medtext-neg download prompt [--model FILE --model-dir DIR]

Options:
    -i FILE                 Inpput file
    -o FILE                 Output file
    --overwrite             Overwrite the existing file
    --regex-patterns FILE   Regular expression patterns [default: ~/.medtext/resources/patterns/regex_patterns.yml]
    --ngrex-patterns FILE   Nregex-based expression patterns [default: ~/.medtext/resources/patterns/ngrex_patterns.yml]
    --sort-anns             Sort annotations by its location
    --model FILE            Pretrained model file [default: ~/.medtext/resources/medtext_neg_prompt/models/negation_detection_model_checkpoint.zip]
    --model-dir DIR         [default: ~/.medtext/resources/medtext_neg_prompt/models/negation_detection_model_checkpoint]
```

## Prompt-based model

This model uses a [prompt-based learning approach](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9378721/) to identify the assertion 
status of an entity in the unstructured clinical notes.
The outcomes are Present, Absent, Possible, Conditional, Hypothetical, and 
Not Associated.

```python
from medtext_neg.models.prompt.neg_prompt import BioCNegPrompt

model_dir = Path(argv['--model-dir']).expanduser()
neg_actor = BioCNegPrompt(pretrained_model_dir=model_dir)
```

## NegBio

For negation detection, medtext employs
[NegBio](https://github.com/bionlplab/negbio2), which utilizes universal
dependencies for pattern definition and subgraph matching for graph traversal
search so that the scope for negation/uncertainty is not limited to the fixed
word distance.

```python
from medtext_neg.models.match_ngrex import NegGrexPatterns
from medtext_neg.models.neg import NegRegexPatterns
from medtext_neg.models.neg import NegCleanUp
from medtext_neg.models.neg import BioCNeg

regex_actor = NegRegexPatterns()
regex_actor.load_yml2(argv['--regex_patterns'])
ngrex_actor = NegGrexPatterns()
ngrex_actor.load_yml2(argv['--ngrex_patterns'])
neg_actor = BioCNeg(regex_actor=regex_actor, ngrex_actor=ngrex_actor)
cleanup_actor = NegCleanUp(argv['--sort_anns'])
```

### Nregex

A Nregex pattern is a regular expression-like pattern that is designed to match node and edge configurations within a
graph. The Nregex pattern allows matching on the attributes of nodes (e.g., lemma) and edges (e.g., dependency type). 
The Nregex follows [Semgrex](https://nlp.stanford.edu/software/tregex.shtml) but only supports "immediate domination"
operations (`>` and`<`).

```{warning}
Like Tregex, there is no pre-indexing of the data to be searched. 
Rather there is a linear scan through the all nodes in
the graph. As a result, matching is **slower**.
```

#### Nodes and relations

A node or relation is represented by a set of attributes and their values contained by curly braces:
`{attr1:value1;attr2:value2;...}`. `{}` represents any node in the graph. Attributes must be plain strings;
values can ONLY be regular expressions blocked off by "`/`". Regular expressions must match the whole attribute
value. For example, `{lemma:/structure/}` matches any nodes with "structure" as their lemma, while
`{lemma:/structure.*/}` matches "structure" and "structures".

```{warning}
Currently, supported node attribute is `lemma`. Supported relation attribute is `dependency`.
```

#### Nregex pattern language

| Symbol          | Meaning                                      |
|:----------------|:---------------------------------------------|
| A <reln B       | A is the dependent of a relation reln with B |
| A >reln B       | A is the governor of a relation reln with B  |

#### Boolean relational operators

Relations can be combined using the '&' and '|' operators

#### Naming nodes

Nodes can be given names (a.k.a. handles) using '='. A named node will be stored in a map that maps names to nodes so
that if a match is found, the node corresponding to the named node can be extracted from the map. For example,
`{lemma:/no/}=k2` will match a node with lemma "no" and assign the name "k2". After a match is found, the map can be
queried with the name to retrieved the matched node using `match.node('k2')`
