This module uses [Philter](https://github.com/BCHSI/philter-ucsf) or 
[bert-deid](https://github.com/alistairewj/bert-deid) to remove PHI
from the reports.

## Quickstart

```shell
$ medtext-deid -i /path/to/input.xml -o /path/to/output.xml
```

```python
from radtext.models.deid import BioCDeidPhilter
processor = BioCDeidPhilter(argv['--repl'])
```

## Links

* [Documentation](https://radtext.readthedocs.io/en/latest/index.html)
* [MedText homepage](https://github.com/bionlplab/radtext)

