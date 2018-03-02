#!/usr/bin/env python


#Class enabling access to the Google ngrams
#Its method is:
#    qryGoogle	gives the Google ngram count for the specified ngram

from __future__ import print_function
import phrasefinder as pf

#Gives the Google ngram count for the specified ngram
#input:
#	qryStr	the specified ngram as string
#output:
#	retval	the Google ngram count for qryStr; 0 if none
#	-		no return value if request was not successful
def qryGoogle(qryStr):
    """Requests the PhraseFinder web service and prints out the result."""
    # Set up your query.
    query = qryStr

    # Optional: set the maximum number of phrases to return.
    options = pf.SearchOptions()
	#options.format='tsv'
    options.topk = 1
    retval =0

    # Send the request.
    try:
        result = pf.search(pf.Corpus.AMERICAN_ENGLISH, query, options)
        if result.status != pf.Status.OK:
            print('Request was not successful: {}'.format(result.status))
            return
        if len(result.phrases)==0:
            retval = 0
        else:
            retval = result.phrases[0].match_count


    except Exception as error:
        print('Some error occurred: {}'.format(error))
        raise
    
    return retval
  
