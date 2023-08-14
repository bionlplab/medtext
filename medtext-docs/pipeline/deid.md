# De-identification

Clinical notes often contain the Protected Health Information 
([PHI](https://www.hhs.gov/hipaa/for-professionals/privacy/special-topics/de-identification/index.html#standard)).
medtext provides two sub-modules for de-idenficiation.

```shell
Usage:
    medtext-deid philter [options] -i FILE -o FILE
    medtext-deid bert [options] -i FILE -o FILE
    medtext-deid download

Options:
    --overwrite     Overwrite the existing file
    -o FILE         Input file
    -i FILE         Output file
    --repl CHAR     PHI replacement char [default: X]
```

* `philter` - This module uses [Philter](https://github.com/BCHSI/philter-ucsf) to remove PHI
from the reports.
* `bert` - This module uses [Robust DeID](https://pypi.org/project/robust-deid/) to remove PHI
from the reports.

## Example Usage

```python
# philter
from medtext_deid.models.deid_philter import BioCDeidPhilter
processor = BioCDeidPhilter(repl=argv['--repl'])

# robust-deid
from medtext_deid.models.deid_robust_deid import BioCRobustDeid
processor = BioCRobustDeid(repl=argv['--repl'])
```