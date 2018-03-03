import GoogleSentList as googSentList
import checkGoogle as cg
from word_forms.word_forms import get_word_forms

#Class containing sentences and their details.
#Its attributes are:
#    start					the start of the problem
#    end					the end of the problem
#    size					the size of the problem
#    typeProb				a parameter containing additional information depending on the errorType
#    errorType				a string specifying the type of the error
#    lstWords				a list containing all words of a sentence
#    lstChecksentoptions	a list of checked sentences after adding required logics for ART or Spel, others type of error types 
#    allowLeft				number of words left to the problem can be used for evaluation
#    allowRight				number of words right to the problem can be used for evaluation
#    chkMarked				boolean that is true for Spelling and Article Determinator Errors
#    chkWord				the word if only a single word needs to be checked
#    currentWord			the word currently evaluated
#    optionList				a list of suggestions from SPEL Checking errorType
#    solution				the solution of the problem
#	 bestOpt				a string specifying the best option on how to solve the problem
#    bestOptval				the value of the best solution, i.e. the word
#	 bestScore				the best score of an ngram
#
#Its methods are:
#    __init__				the initialization of a ProblemSolution object
#    getSVASolution			gets the solution of Subject Verb Agreement Errors
#    getCorrectVerb			generates the correct verb form
#    to_plural				gives back the plural form of a verb
#    to_3th_person			gives back the 3rd person singular present of a verb
#    getOptionlist			takes the word and the option and then changes to that required category
#    getSpelSolution		gets the correct spelling for a incorrect spelled word
#    getOthersolution		gets other solutions
#    genChecklist			checks what boundaries an ngram containing the problem may have
#    reChkRedSize			tries different bounderies for the ngram of the problem to get scores different from zero for the possible solution
#    getNgramcount			gets the ngram count for a possible solution with Google ngram
#    scoreCheck				checks if the best score of the ngram is 0 to see if it is applicable as solution
#    getSolution			returns the solution
class ProblemSolution:
    start               = 0
    end                 = 0
    size                = 0
    typeProb            = "" 
    errorType           = ""  #Error types are SPEL / ART / ARTChk / SVACOMP /SVABASE / OTHER
    lstWords            = None
    lstChecksentoptions = None
    allowLeft           = 0
    allowRight          = 0
    chkMarked           = False
    chkWord             = ""
    currentWord         = ""
    optionList          = []
    #solution is an array which has 3 para
    #para 1 : start of the word list
    #para 2 : Solution type INB / INA /   NA / REP are the solutions
    #para 3 : for before insert the text to be inserted for NA and Replace option
    # the text will be blank
    solution            = None
    
	#Initializes the ProblemSolution object
	#input:
	#	startval		the start index of the problem
	#	endval			the end index of the problem
	#	typep			a parameter containing additional information depending on the errorType
	#	errorTypeval	the type of the error as a string
	#	lstWordval		a list containing all the words of the sentence
    def __init__(self,startval,endval,typep,errorTypeval,lstWordval):
        self.start               = int(startval)
        self.end                 = int(endval)
        self.typeProb            = typep
        self.problemCondition    = False
        self.errorType           = errorTypeval
        if self.errorType in ['ArtChk','SPEL']:
            self.chkMarked       = True
            self.chkWord         = lstWordval[self.start]
        self.lstWords            = lstWordval
        self.lstChecksentoptions = []
        self.solution            = [0,0,0]
        
        if self.errorType == 'OTHER':
            self.getOthersolution()
            self.getNgramcount()
            self.scoreCheck()

        if self.errorType == 'SPEL':
            self.getSpelSolution()
            self.getNgramcount()
            self.scoreCheck()

        if self.errorType in ['ART','ArtChk']:
            self.genChecklist()
            if self.problemCondition == True:
                self.getNgramcount()
                self.scoreCheck()
        if self.errorType in ['SVACOMP','SVACOMPplural']:
            self.getSVASolution()
            
	#Gets the solution of Subject Verb Agreement Errors by replacing the incorrect form with the correct form
    def getSVASolution(self):
        startPos        = self.end
        self.bestOpt    = "REP"
        self.bestOptval = self.getCorrectVerb(self.lstWords[startPos],self.typeProb)
        self.solution   = [startPos,self.bestOpt,self.bestOptval]
        
    #Generates the correct verb form depending on the parameter option
	#input:
	#	verb	the incorrect verb
	#	option	a string containing information about the correct form of the verb
	#output:
	#	retval	the corrected verb
    def getCorrectVerb(self,verb, option):
        retval = ""
        if option == 'TO_PLURAL':
            retval = self.to_plural(verb)
        elif option == 'TO_3TH_PERSON':
            retval = self.to_3th_person(verb)
        elif option == 'TO_WAS':
            retval = "was"
        elif option == 'TO_AM':
            retval = "am"
        
        return retval
            
	#Gives back the plural form of a verb by handwriten rules
	#input:
	#	verb	the verb in its singular form
	#output:
	#	""		a string of the plural form of the verb
	#	verb	the verb itself it doesn't fit the rules
    def to_plural(self,verb):
        if verb == "is":
            return "are"
        if verb == 'has':
            return 'have'
        if verb == 'was':
            return 'were'
    
        if verb[-3:] in ['ies']:
            return verb[:-3] + 'y'
        if verb[-2:] == 'es':
            return verb[:-2]
        if verb[-1] == 's':
            return verb[:-1]
        return verb

	#Gives back the 3rd person singular present of a verb by handwriten rules
	#input:
	#	verb	the verb in its other form
	#output:
	#	""		a string of the wnated form of the verb
    def to_3th_person(self,verb):
        if verb == 'are':
            return 'is'
        if verb == 'have':
            return 'has'
        if verb == 'were':
            return 'was'
    
        if verb[-2:] in ['ss', 'ch', 'sh']:
            return verb + 'es'
        if verb[-1:] in ['x', 'o']:
            return verb + 'es'
        if verb[-1:] in ['y'] and verb[-2:-1] not in ['a','e','i','o','u']:
            return verb[:-1] + 'ies'

        return verb + 's'

	#The function takes the word and the option and then changes to that required category. 
	#input:
	#	checkWord	 Input word 
	#	optionPass	 The required tag to be converted
	#output:
	#	list		it return a required value after changing to another type 
    def getOptionlist(self,checkWord,optionPass):   
        checkWord = checkWord.lower()
        outdic ={}
        outdic = get_word_forms(checkWord)
        
        if optionPass in ['NNS','NN','NNP','NNPS']:
            return list(outdic.get('n'))
        elif optionPass in ['JJ','JJR','JJS']:
            return list(outdic.get('a'))
        elif optionPass in ['RB','RBR','RBS']:
            return list(outdic.get('r'))
        elif optionPass in ['VB','VBD','VBG','VBN','VBZ']:
            return list(outdic.get('v'))
        
	#Gets the correct spelling for a incorrect spelled word by checking with the Google ngrams for the context in the sentence
    def getSpelSolution(self):
        mleft  = 1
        mRight = 1
        self.allowLeft  = mleft
        self.allowRight = mRight

        self.size = self.end-self.start+1

        genSentence   = googSentList.GoogleSentList(True,True,True,False,self)
        self.currentWord   = self.lstWords[self.start]
        self.chkWord       = self.currentWord

        #generate the list 
        self.optionList =self.typeProb
        
        self.lstChecksentoptions = genSentence.genSentlistOther(self.allowLeft,self.allowRight,self.typeProb,self.currentWord,self.optionList)

	#Gets other solutions by checking with the Google ngrams for the context in the sentence
    def getOthersolution(self):
        mleft  = 1
        mRight = 1
        self.allowLeft  = mleft
        self.allowRight = mRight
        
        self.size = self.end-self.start+1

        genSentence   = googSentList.GoogleSentList(True,True,True,False,self)
        self.currentWord   = self.lstWords[self.start]

        #generate the list 
        self.optionList =[]
        self.optionList = self.getOptionlist(self.currentWord,self.typeProb)
        
        self.lstChecksentoptions = genSentence.genSentlistOther(self.allowLeft,self.allowRight,self.typeProb,self.currentWord,self.optionList)
        
	#Checks what boundaries an ngram containing the problem may have
    def genChecklist(self):        
        
        self.problemCondition = True
        self.size = self.end-self.start+1
        
        mleft = 0
        
        if self.size<=2:
            mleft  = 1
            mRight = 1 
        elif self.size<=3:
            mleft  = 1
            mRight = 0
        else:
            self.problemCondition = False
            mRight = 0
            
        if mleft>self.start:
            self.allowLeft = int(self.start)
        else:
            self.allowLeft = int(mleft)
        
        if self.end<len(self.lstWords)-2:
            self.allowRight = mRight
        else:
            self.allowRight = 0
            
        # Going in the details of the problem
        if self.problemCondition == True:
            genSentence              = googSentList.GoogleSentList(True,True,True,False,self)
            self.lstChecksentoptions = genSentence.genSentlist(self.allowLeft,self.allowRight,self.typeProb)
        else:
            #Solution  is none at this case            
            self.solution=[self.start,"NA",""]
                
            
	#Tries different bounderies for the ngram of the problem to get scores different from zero for the possible solution
	#output:
	#	1		if there is a score higher than zero
	#	retval	has a value of 0 since no higher score has been found
    def reChkRedSize(self):
        retVal = 0 
        if self.size==3:                    
            #print("Reducing the Size for the Case of 3 ")
            genSentence              = googSentList.GoogleSentList(True,True,True,True,self)
            self.lstChecksentoptions = genSentence.genSentlist(self.allowLeft,self.allowRight,self.typeProb)
            self.getNgramcount()
            if self.bestScore>0:
                return 1
            #print("Try to remove Right wing")
            genSentence              = googSentList.GoogleSentList(True,False,True,True,self)
            self.lstChecksentoptions = genSentence.genSentlist(self.allowLeft,self.allowRight,self.typeProb)
            self.getNgramcount()
            if self.bestScore>0:
                return 1
            #print("Try to remove left wing")
            genSentence              = googSentList.GoogleSentList(False,True,True,True,self)
            self.lstChecksentoptions = genSentence.genSentlist(self.allowLeft,self.allowRight,self.typeProb)
            self.getNgramcount()
            if self.bestScore>0:
                return 1

            #print("Try to remove both wing")
            genSentence              = googSentList.GoogleSentList(False,False,True,True,self)
            self.lstChecksentoptions = genSentence.genSentlist(self.allowLeft,self.allowRight,self.typeProb)
            self.getNgramcount()
            if self.bestScore>0:
                return 1


        if self.size<=2:
            if self.errorType in ['ART','ArtChk']:
                #print("Try to remove Right wing")
                genSentence              = googSentList.GoogleSentList(True,False,True,False,self)
                self.lstChecksentoptions = genSentence.genSentlist(self.allowLeft,self.allowRight,self.typeProb)
                self.getNgramcount()
                if self.bestScore>0:
                    return 1
                #print("Try to remove left wing")
                genSentence              = googSentList.GoogleSentList(False,True,True,False,self)
                self.lstChecksentoptions = genSentence.genSentlist(self.allowLeft,self.allowRight,self.typeProb)
                self.getNgramcount()
                if self.bestScore>0:
                    return 1
            elif self.errorType in ['SPEL','OTHER']:
                #print("Try to remove Right wing")
                genSentence              = googSentList.GoogleSentList(True,False,True,False,self)
                self.lstChecksentoptions = genSentence.genSentlistOther(self.allowLeft,self.allowRight,self.typeProb,self.currentWord,self.optionList)
                self.getNgramcount()
                if self.bestScore>0:
                    return 1
                #print("Try to remove left wing")
                genSentence              = googSentList.GoogleSentList(False,True,True,False,self)
                self.lstChecksentoptions = genSentence.genSentlistOther(self.allowLeft,self.allowRight,self.typeProb,self.currentWord,self.optionList)
                self.getNgramcount()
                if self.bestScore>0:
                    return 1

                
            if self.errorType in ['ART','ArtChk']:
                #print("Try to remove both wing")
                genSentence              = googSentList.GoogleSentList(False,False,True,False,self)
                self.lstChecksentoptions = genSentence.genSentlist(self.allowLeft,self.allowRight,self.typeProb)
                self.getNgramcount()
                if self.bestScore>0:
                    return 1            
            elif self.errorType in ['SPEL']:
                genSentence              = googSentList.GoogleSentList(False,False,True,False,self)
                self.lstChecksentoptions = genSentence.genSentlistOther(self.allowLeft,self.allowRight,self.typeProb,self.currentWord,self.optionList)
                self.getNgramcount()
                if self.bestScore>0:
                    return 1            

        return retVal
        
	#Gets the ngram count for a possible solution with Google ngram
    def getNgramcount(self):
        self.bestScore  = 0
        self.bestOpt    = ""
        self.bestOptval = ""
        # get the best value to determine the solution
        for sent,opt,optval in self.lstChecksentoptions:
            try:
                outVal = cg.qryGoogle(sent)
                #setting threshold to 1000
                if outVal < 500:
                    outVal =0
                #giving a extra score for ArtChk Checked Word
                if outVal !=0 and optval==self.chkWord and self.errorType in ['ArtChk','SPEL']:
                    outVal +=20000
                
                if outVal>self.bestScore:
                    self.bestScore  = outVal
                    self.bestOpt    = opt
                    self.bestOptval = optval
            except:
                print("In the error")
                self.lstChecksentoptions.append([sent,opt,optval])
        #if no best score is found the solution is not applicable
     
	#If the best score of the ngrams is not zero, it will be the solution
	#If not, there is no solution except if it is an ArtChk error
	#Then it depends on the best option
    def scoreCheck(self):   
        if self.bestScore ==0:
            if self.reChkRedSize() == 0:
                self.solution=[self.start,"NA",""]
            else:
                self.solution = [self.start,self.bestOpt,self.bestOptval]
        else:
            self.solution = [self.start,self.bestOpt,self.bestOptval]
            
        #checking for ArtChk 
        if self.errorType == 'ArtChk':
            if self.bestOpt=='NA':
                self.solution = [self.start,'REP','']
            elif self.bestOpt=='INB' and self.bestOptval == self.lstWords[self.start]:
                self.solution = [self.start,'NA','']
            else:
                self.solution = [self.start,'REP',self.bestOptval]
				
	#Returns the solution
	#output:
	#	self.solution	the solution
    def getSolution(self):
        return self.solution