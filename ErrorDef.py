import spelchek
import inflect
p = inflect.engine()

#Class containing sentences and their details.
#Its attributes are:
#    ErrorType				a string indicating the type of the error currently handled
#
#Its methods are:
#    __init__				the initialization of a ErrorDef object with its error type
#    checkDeterminer		determines the Article Determiner Error
#    checkSVACOMP			determines the Subject Verb Agreement Error in general cases
#    checkSVACOMPplural		determines if the verb is plural when it should be (SVA for subjects formed with "and")
#    checkSpel				determines if a word is spelled correctly
#    checkOther				x
class ErrorDef:
    #Error types are SPEL / ART / ArtChk / SVACOMP /SVABASE / OTHER
    ErrorType = ""
            
    #Initialize the ErrorDef object
	#input:
	#	etype	the error type
    def __init__(self,etype):
        self.ErrorType = etype

    #Checks whether or not a noun has a missing determiner by looking for determiners
	#input:
	#	indval			the index of the noun checked for Article Determiner Error
	#	syntval			the POS tag of the noun checked for Article Determiner Error
	#	sentDet			the Sentence Details Object containing information about the sentence the noun checked for Article Determiner Error is in
	#output:
	#	0				if no error has been detected
	#	probStart		the start index of the detected error
	#	probEnd			the end index of the detected error
	#	syntval			the POS tag of the noun checked for Article Determiner Error
	#	self.ErrorType	the ErrorType currently handled
    def checkDeterminer(self,indval,syntval,sentDet):
        ind = indval
        #checking Sibling items for NP so that and also finding Determiner
        condition = True
        foundDet  = False
        lstParse  = []
        lstWords  = []
        detText   = ""
        probEnd   = 0
        probStart = 0
    
        while (condition):
            condition = 'NP' not in sentDet.parse[ind]
            if(ind==0):
                condition = False
            lstWords.append(sentDet.words[ind])
            lstParse.append(sentDet.parse[ind])
            if (sentDet.synt[ind] in ['DT','PRP$']):
                foundDet = True
                detText  = sentDet.words[ind]
            probStart= ind
            ind= ind-1
            probEnd = indval
        if foundDet is False:
            return [probStart,probEnd,syntval,self.ErrorType]
        else:
            foundDet = False
            self.ErrorType = "ArtChk"
            if detText in ['a','an','the','']:
                return [probStart,probEnd,syntval,self.ErrorType]
        return 0
    
	#Checks whether a subject and a verb agree by comparing whether their forms are plural or singular (SVA Error)
	#input:
	#	subj			the word that is the subject
	#	subjind			the index of the subject
	#	verb			the word that is the verb
	#	verbind			the index of the verb
	#	syntverb		the POS tag of the verb
	#	sentDet			the Sentence Details Object containing information about the sentence checked for SVA Error
	#output:
	#	0				if no error has been detected
	#	subjind			the index of the subject
	#	verbind			the index of the verb
	#	CHANGE			a string indicating how the verb should be changed to correct the detected SVA Error
	#	self.ErrorType	the ErrorType currently handled
    def checkSVACOMP(self, subj, subjind, verb, verbind, syntverb, sentDet):
        IS_KNOWN_PLURAL = False
        CHANGE = "" #TO_3TH_PERSON, TO_PLURAL
        verb = verb.lower()
		
		#Checks whether noun is singular or plural
        if subj == "I":
            if p.plural(verb) == "are":
                if verb != "am":
                    return [subjind,verbind,"TO_AM",self.ErrorType]
                else:
                    return 0
            elif p.plural(verb) == "were":
                if verb != "was":
                    return [subjind,verbind,"TO_WAS",self.ErrorType]
                else:
                    return 0
            else:
                IS_KNOWN_PLURAL = True				
        elif subj.lower() in ["you", "they", "we", "both", "most"]:
            IS_KNOWN_PLURAL = True
        elif str(p.singular_noun(subj)) == "False":#subj is singular
            IS_KNOWN_PLURAL = False
        elif subj.lower() in ["nothing", "this"]:
            IS_KNOWN_PLURAL = False
        else:
            IS_KNOWN_PLURAL = True	#NNS NNPS

		#checks whether verb is singular or plural
        if IS_KNOWN_PLURAL:
            if syntverb in ["VBZ"]:
                CHANGE = "TO_PLURAL"
                return [subjind,verbind,CHANGE,self.ErrorType]
            elif verb in ["was"]:
                CHANGE = "TO_PLURAL"
                return [subjind,verbind,CHANGE,self.ErrorType]
            else:
                return 0
        else:
            if syntverb == "VBZ":
                return 0
            elif verb == "were":
                CHANGE = "TO_3TH_PERSON"
                return [subjind,verbind,CHANGE,self.ErrorType]
            elif syntverb in ["VBD", "VBN", "MD"]:
                return 0
            else:
                CHANGE = "TO_3TH_PERSON"
                return [subjind,verbind,CHANGE,self.ErrorType]
        print("This should not happen")
        return 0
	
	#determines if the verb is plural when it should be (SVA for subjects formed with "and")
	#input:
	#	subj			the word that is the subject
	#	subjind			the index of the subject
	#	verb			the word that is the verb
	#	verbind			the index of the verb
	#	syntverb		the POS tag of the verb
	#	sentDet			the Sentence Details Object containing information about the sentence checked for SVA Error
	#output:
	#	0				if no error has been detected
	#	verbind			the index of the verb
	#	self.ErrorType	the ErrorType currently handled
    def checkSVACOMPplural(self, verb, verbind, syntval, sentDet):
        plural_verb = p.plural_verb(verb)
        if verb == plural_verb:
            return 0
        else:
            return [verbind,verbind,"TO_PLURAL",self.ErrorType]

	#Determines if a word is spelled correctly by looking it up in spelcheck
	#If it is not it then generates a list of possible correction by getting the guesses from spelcheck
	#input:
	#	indval			the index of the current word
	#	word			the word that checked for spelling
	#	sentDet			the Sentence Details Object containing information about the sentence with the current word
	#output:
	#	0				if no error has been detected
	#	indval			the index of the incorrect spelled word
	#	suggList		a list containing suggestions of correct spellings for the incorrect word
	#	self.ErrorType	the ErrorType currently handled        
    def checkSpel(self, indval,word,sentDet):
        word = word.lower()
        checkedWord =spelchek.correct(word) 
        # not spell checked words
        if word in [',','.',"'",'?',"''",'-',':','(',')',';']:
            return 0
        
        if checkedWord == word:
            return 0
        else:
            suggList = spelchek.guesses(word)
            suggList.append(checkedWord)
            return [indval,indval,suggList,self.ErrorType]

	#Determines if there are other possible errors by checking whether the word is of a specific POS tag
	#input:
	#	indval			the index of the current word
	#	syntval			the POS tag of the current word
	#	sentDet			the Sentence Details Object containing information about the sentence with the current word
	#output:
	#	0				if the POS tag of the word is not among the specified ones
	#	indval			the index of the current word
	#	syntval			the POS tag of the current word
	#	self.ErrorType	the ErrorType currently handled        
    def checkOther(self,indval,syntval,sentDet):
        validtags = ['JJ','JJR','JJS','NNS','NN','NNP','NNPS','RB','RBR','RBS','VB','VBD','VBG','VBN','VBZ']
        if syntval in validtags:
            return [indval,indval+1,syntval,self.ErrorType]
        else:
            return 0    

