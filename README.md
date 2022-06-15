# Performance of Automatically Processing User Feedback

Test the performance and energy consumption of text classification, topic modeling, sentiment analysis, and similarity measurements.

## Installation
### External:
* SentiStrength
  * Location: `ALERTme_approach/sentistrength/`
    * [SentiStrength.jar](http://sentistrength.wlv.ac.uk/jkpop/)
    * [SentiStrength_Data](http://sentistrength.wlv.ac.uk/jkpop/)
* STTM: A Library of Short Text Topic Modeling
  * Location:
    * [STTM](https://github.com/qiang2100/STTM)
  * Location: `STTM-master/`
    * [enwiki-latest-pages-articles.xml.bz2](https://dumps.wikimedia.org/enwiki/latest/)
    * [glove.6B.zip](https://nlp.stanford.edu/projects/glove/)
* BERT
  * Location: `current_approach/data`
    * [bert_en_uncased_preprocess](https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3)
    * [bert_en_uncased_L-12_H-768_A-12](https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/4)

To compute topic coherence for topic modeling the previously downloaded Wikipedia dataset has to be transformed from html to text.
```bash
# This can take up to 10 hours depending on the hardware
python2 STTM-master/process_wiki.py enwiki-latest-pages-articles.xml.bz2 wiki.en.text
```
### SQL
Install [MySQL Workbench](https://www.mysql.com/products/workbench/) or equivalent and start a new schema.

### RStudio
Install [RStudio](https://www.rstudio.com) and the following libraries in R.
```R
Placeholder
```

### Pip
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the following packages.

```bash
pip install sentistrength
```

## Usage
To compute topic coherence for topic modeling the previously downloaded Wikipedia dataset has to be transformed from html to text.
```bash
placeholder
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
