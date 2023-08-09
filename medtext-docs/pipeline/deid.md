# De-identification

Radiology reports often contain the Protected Health Information 
([PHI](https://www.hhs.gov/hipaa/for-professionals/privacy/special-topics/de-identification/index.html#standard)).
This module uses [Philter](https://github.com/BCHSI/philter-ucsf) to remove PHI
from the reports.

## Options

| Option name | Default | Description          |
|:------------|:--------|:---------------------|
| --repl      | `X`     | PHI replacement char |

### Example Usage

```shell
$ medtext-deid --repl=X -i /path/to/input.xml -o /path/to/output.xml
```

```python
from medtext_deid.models.deid_philter import BioCDeidPhilter
processor = BioCDeidPhilter(argv['--repl'])
```