This module offers a tool to convert from [OMOP CDM NOTE
table](https://www.ohdsi.org/web/wiki/doku.php?id=documentation:cdm:note) (in
the CSV format) to the BioC collection. By default, column `note_id` stores
the report ids, and column `note_text` stores the reports.

## Quickstart

```shell
# Convert from csv to BioC
$ medtext-csv2bioc -i /path/to/csv_file.csv -o /path/to/bioc_file.xml
```

## Links

* [Documentation](https://radtext.readthedocs.io/en/latest/index.html)
* [MedText homepage](https://github.com/bionlplab/radtext)

