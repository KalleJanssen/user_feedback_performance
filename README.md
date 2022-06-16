# Performance of Automatically Processing User Feedback

Test the performance and energy consumption of text classification, topic modeling, sentiment analysis, and similarity measurements.

## Installation
### Requirements
* R
  * [RStudio](https://www.rstudio.com)
  * Packages
    * glue
    * plyr
    * pastecs
    * ggplot2
    * tidyverse
    * gridExtra
    * pracma
    * hash
* SQL
  * [MySQL Workbench](https://www.mysql.com/products/workbench/)
    * Replace passwords and databases in all files in `all_algorithms/` and `everything_data/`
    * Create a new schema called
* Python 3.8
* Python 2.7
* Java 8
* Java 1.8

### Pip
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the following packages.

```bash
# python2
pip install requirements_2.txt

# python3
pip3 install requirements_3.txt
```

### External algorithms:
Download the following algorithms and place them in the corresponding locations
* SentiStrength
  * Location: `ALERTme_approach/sentistrength/`
    * [SentiStrength.jar](http://sentistrength.wlv.ac.uk/jkpop/)
    * [SentiStrength_Data](http://sentistrength.wlv.ac.uk/jkpop/)
* STTM: A Library of Short Text Topic Modeling
  * Location: `topic_modeling/`
    * [STTM](https://github.com/qiang2100/STTM)
  * Location: `topic_modeling/STTM-master/`
    * [glove.6B.zip](https://nlp.stanford.edu/projects/glove/)
* SIMBA
  * Location: `all_algorithms/`
    * [SIMBA](https://doi.org/10.1109/RE48521.2020.00017)
* Senti4SD
  * Location: `all_algorithms/`
    * [Senti4SD](https://github.com/collab-uniba/Senti4SD)
    * Location to the Senti4SD folder has to be edited in `all_algorithms/sentiment_senti4SD.py`

## Usage
To prepare the data, each `.sql` file in `everything_data/labeled_data/` should be run in a previously created SQL schema. 

Each algorithm can be run separately in the `all_algorithms` folder or all automatically by running `all_algorithms/random_run.py`. To run any of these algorithms, the passwords and databases of the SQL database should be changed in each algorithm file. Furthermore, for testing reasons, each algorithm is run n times. This can be changed if energy does not need to be measured. Energy can be measured by running `webserver_stress_DAE.py` in a separate terminal.

Finally, results can be analyzed and visualized using the `statistics.R` file.

## License
[MIT](https://choosealicense.com/licenses/mit/)
