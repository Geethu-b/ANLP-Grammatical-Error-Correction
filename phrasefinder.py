# This file is part of PhraseFinder.  http://phrasefinder.io
#
# Copyright (C) 2016-2017  Martin Trenkmann
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
The phrasefinder module provides routines for querying the PhraseFinder web service at
http://phrasefinder.io.
"""
import sys
from enum import Enum, unique

if sys.version_info[0] < 3:
    # Python 2.
    import urllib as urllibx
    from urllib import urlencode as urlencode
else:
    # Python 3.
    import urllib.request as urllibx
    from urllib.parse import urlencode as urlencode

VERSION_MAJOR = 0
VERSION_MINOR = 4
VERSION_BUILD = 0
VERSION = VERSION_MAJOR * 1000000 + VERSION_MINOR * 1000 + VERSION_BUILD
"""Defines the version number as one integer."""

@unique
class Corpus(Enum):
    """Corpus contains numeric constants that represent corpora to be searched.

    All corpora belong to version 2 of the Google Books Ngram Dataset
    (http://storage.googleapis.com/books/ngrams/books/datasetsv2.html).
    """
    NULL = 0
    AMERICAN_ENGLISH = 1
    BRITISH_ENGLISH = 2
    CHINESE = 3
    FRENCH = 4
    GERMAN = 5
    RUSSIAN = 6
    SPANISH = 7

    def short_name(self):
        """Returns the short name of this enum constant."""
        return {
            0: "null",
            1: "eng-us",
            2: "eng-gb",
            3: "chi",
            4: "fre",
            5: "ger",
            6: "rus",
            7: "spa"
        }[self.value]


@unique
class Status(Enum):
    """Status contains numeric constants that report whether a request was successful.

    The value is derived from the HTTP status code sent along with a response. Note that the numeric
    value does not correspond to the original HTTP code.
    """
    OK = 0
    BAD_REQUEST = 1
    BAD_GATEWAY = 2

class Token(object):
    """Token represents a single token (word, punctuation mark, etc.) as part of a phrase."""

    @unique
    class Tag(Enum):
        """Tag denotes the role of a token with respect to the query."""
        GIVEN = 0
        INSERTED = 1
        ALTERNATIVE = 2
        COMPLETED = 3

    def __init__(self):
        self.text = ""
        self.tag = Token.Tag.GIVEN

class Phrase(object):
    """Phrase represents a phrase, also called n-gram.

    A phrase consists of a sequence of tokens and metadata.
    """
    def __init__(self):
        self.tokens = []       # The tokens of the phrase.
        self.match_count = 0   # The absolute frequency in the corpus.
        self.volume_count = 0  # The number of books it appears in.
        self.first_year = 0    # Publication date of the first book it appears in.
        self.last_year = 0     # Publication date of the last book it appears in.
        self.score = 0.0       # The relative frequency it matched the given query.
        self.id = 0            # See the API documentation on the website.

class SearchOptions(object):
    """SearchOptions represents optional parameters that can be sent along with a query."""

    DEFAULT_NMIN = 1    # read-only
    DEFAULT_NMAX = 5    # read-only
    DEFAULT_TOPK = 100  # read-only

    def __init__(self):
        self.nmin = SearchOptions.DEFAULT_NMIN
        self.nmax = SearchOptions.DEFAULT_NMAX
        self.topk = SearchOptions.DEFAULT_TOPK

class SearchResult(object):
    """SearchResult represents the outcome of a search request."""
    def __init__(self):
        self.status = Status.OK
        self.phrases = []  # List of Phrase instances.

def search(corpus, query, options=SearchOptions()):
    """Sends a search request to the server.

    Returns:
      A SearchResult object whose status attribute is equal to Status.Ok if the request was
      successful. In this case other attributes of the object have valid data and can be read. Any
      status other than Status.Ok indicates a failed request. In that case other attributes in the
      result have unspecified data. Critical errors are reported throwing an exception.
    """
    http_response_code_to_status = {
        200: Status.OK,
        400: Status.BAD_REQUEST,
        502: Status.BAD_GATEWAY
    }
    result = SearchResult()
    context = urllibx.urlopen(_make_url(corpus, query, options))
    result.status = http_response_code_to_status[context.getcode()]
    if result.status == Status.OK:
        for line in context.readlines():
            line = line.decode('utf-8')
            phrase = Phrase()
            parts = line.split("\t")
            for token_with_tag in parts[0].split(" "):
                token = Token()
                token.text = token_with_tag[:-2]
                token.tag = int(token_with_tag[-1])
                phrase.tokens.append(token)
            phrase.match_count = int(parts[1])
            phrase.volume_count = int(parts[2])
            phrase.first_year = int(parts[3])
            phrase.last_year = int(parts[4])
            phrase.id = int(parts[5])
            phrase.score = float(parts[6])
            result.phrases.append(phrase)
    context.close()
    return result

def _make_url(corpus, query, options):
    params = [
        ("format", "tsv"),
        ("corpus", corpus.short_name()),
        ("query", query)
    ]
    if options.nmin != SearchOptions.DEFAULT_NMIN:
        params.append(("nmin", options.nmin))
    if options.nmax != SearchOptions.DEFAULT_NMAX:
        params.append(("nmax", options.nmax))
    if options.topk != SearchOptions.DEFAULT_TOPK:
        params.append(("topk", options.topk))
    return "http://phrasefinder.io/search?" + urlencode(params)
