# ANLP-Grammatical-Error-Correction
ANLP-Grammatical-Error-Correction is a system to automatically detect grammar and spelling errors. It is a final project of the module Advanced Natural Language processing and was inspired by the CoNLL Shared Task 2014.

The input data has to be in the CoNLL format. Since this project has been tested on the testdata of the CoNLL Shared Task 2014, this has been included. Running the project with no modifiaction will give the scores of the error detection on the mentioned data.

To run this project, execute readFile.py with python 3.6 or higher on a Linux operating system.

readFile.py reads the test file[testdata1.con] which is in conll format.
This would invoke the other functions and generate Spelling[spel.pkl],Other error [other.pkl],subject verb agreemnt error[sva.pkl], and Article error pickle files.The final combined pickle file is named "all"

makeM2Sen.py takes the final pickle file[all.pkl] and generates M2file.txt. This is given to the m2 scorer as input to get the precision, recall and F-score. 

The scorer files are in the folder M2scorer and can be initiated with the file m2score_report.py.
The readme file in the examples folder has more details for processing using m2scorer.

The pickle files are provided in the results folder and if needed, can be used to execute the individual modules. M2file is also provided which can be used to run the m2scorer.

Links:
Treetagger installation : http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/
Spelcheck		: https://github.com/theodox/spelchek
Inflect			: http://pypi.python.org/pypi/inflect
WordNet			: http://wordnet.princeton.edu
difflib			: https://docs.python.org/2/library/difflib.html#
NLTK			: http://www.nltk.org/
word_forms		: https://github.com/gutfeeling/word_forms
PhraseFinder		: http://phrasefinder.io/api

