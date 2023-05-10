# Documentation

The [code_docs](code_docs) folder contains documentation generated from the code. The [gas](code_docs/gas) folder
contains all the documentation for the part of the server that processes requests, i.e. the server logic itself.
The [src](code_docs/src) folder then contains documentation for the preprocessor and evaluator modules and other utils
scripts for preprocessing of datasets.

The GASercher documentation is available in the [file Documentation](Documentation.md).

## Preprocessing new dataset

To preprocess the entire dataset, just use [the Preprocessor class](../src/preprocessor.py). Currently, the Preprocessor
is set to process videos from the "gasearcher/static/data/videos" folder along with using the generic
[nounlist dictionary](../nounlists/nounlist.txt). The results of all preprocessing will be stored in the
["gasearcher/static/data"](../gasearcher/static/data) folder. These settings can be easily changed at the end of
the file, where the Preprocessor is defined.

Beware that when processing a new dataset, the metadata is stored in files so that it can be used directly by GASearcher
without changing the settings. Therefore, they are stored in identically named files unless otherwise defined.
Therefore, clean the resulting folder from all such files before starting preprocessing.

## Log processing

[The Evaluator class](../src/evaluator.py) can be used to evaluate other models. In the current setup, it
processes [the log](../gasearcher/static/data/log.csv) used directly by GASearcher and stores the results in a folder
created directly by the helper scripts. A basic graph is then created that compares the basic six models.
All paths can be redefined at the end of the file containing [the Evaluator class](../src/evaluator.py).