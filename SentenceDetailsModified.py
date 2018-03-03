import problemlist as prbList
import ErrorDef as errDef

import os
import nltk

from nltk.tag import StanfordPOSTagger
os.environ['JAVAHOME'] = "C:/Program Files/Java/jre1.8.0_151/bin"


#Class containing sentences and their details.
#Its attributes are:
#    inds			a list of the indeces of the words in the sentencs
#    words			a list of the words in the sentencs
#    synt			a list of the POS-tags of the words in the sentencs
#    parse			a list of the parse tree parts relevant for the words in the sentence
#    dep_ind			a list of the indices words of the sentence are refering to in their dependecy graph
#    dep_tag			a list of the dependecy tags of the words of the sentence
#    lstProb			a list of the problems a sentence has
#    lstSoln			a list of the solutions of the problems a sentence has
#    sentenceIndex	the index of the sentence itself
#    lstOther		a list containing other [Noun Number, VForm, WForm] errors 
#    objLstProblems	a class object referencing the class 'ProblemList'
#
#Its methods are:
#    __init__				the initialization of a SentenceDetailsModified object. All internal lists are empty
#    initiateLists			the initialization of the Problem List
#    addItems				the details of the words of the sentence are added
#    getWords				returns the list of the words
#    listProblems			returns the Problem List
#    solveProblem			generates the solutions and add them to the list of solutions
#    getSolutionInTag		updates the POS tags of the sentence (after a new solution)
#    getSolutionInSentence	corrects the sentence according to the solutions
class SentenceDetailsModified:
    inds           = None
    words          = None
    synt           = None
    parse          = None
    dep_ind        = None
    dep_tag        = None
    lstProb        = None
    lstSoln        = None
    sentenceIndex  = 0
    lstOther       = None
    objLstProblems = None
    
	#Constructs the Object SentenceDetailsModified
	#input:
	#	sentenceIndex	the number of the sentence
	#	lstOther		a list containing other [Noun Number, VForm, WForm] errors 
    def __init__(self,sentenceIndex, lstOther):
        self.inds           = []
        self.words          = []
        self.synt           = []
        self.parse          = []
        self.dep_ind        = []
        self.dep_tag        = []
        self.lstProb        = []
        self.lstSoln        = []
        self.sentenceIndex  = sentenceIndex
        self.lstOther       = lstOther
        self.objLstProblems = prbList.ProblemList(self.words)
        
	#Initializes the Problem List
    def initiateLists(self):
        self.objLstProblems = prbList.ProblemList(self.words)
        self.lstProb        = []
        self.lstSoln        = []

    #Adds the details regarding the words of the sentence
    def addItems(self,indval,wordval,syntval,parseval,depnumval, depvalue):
        self.inds.append(indval)
        self.words.append(wordval)
        self.synt.append(syntval)
        self.parse.append(parseval)
        self.dep_ind.append(depnumval)
        self.dep_tag.append(depvalue)
   
	#Returns the list of the words
    def getWords(self):
        return self.words

    #Returns the Problem List
    def listProblems(self):
        self.lstProb = self.objLstProblems.getProbList()
      
	#Generates the solutions and add them to the list of solutions
    def solveProblem(self):
        self.lstSoln = self.objLstProblems.getSolutions()
        
	#Retags the sentence with the StanfordPOSTagger and saves the new tags in self.synt
    def getSolutionInTag(self):
        english_postagger = StanfordPOSTagger("F:/Potsdam_courses/ANLP/project/grammar_error/stanford-postagger-2017-06-09/models/english-bidirectional-distsim.tagger","F:/Potsdam_courses/ANLP/project/grammar_error/stanford-postagger-2017-06-09/stanford-postagger.jar")
        
        #retag the sentence again
        new_tag_values = english_postagger.tag(self.words)      
        for index in range(len(self.inds)):
            word,tag = new_tag_values[index]
            self.synt[index] = tag
    
	#Depending on the solutions of the sentence, words are either inserted or replaced (in self.words)
    def getSolutionInSentence(self):
        #sort the list of solutions
        self.lstSoln.sort(key=lambda x: x[0])
        for ind,Operation,Operand in self.lstSoln[::-1]:
            if Operation == 'INB':  
                self.words= self.words[0:ind]+[Operand]+self.words[ind:len(self.words)+1]
            elif Operation == 'REP':
                if Operand == '':
                    self.words= self.words[0:ind]+self.words[ind+1:len(self.words)+1]
                else:
                    self.words= self.words[0:ind]+[Operand]+self.words[ind+1:len(self.words)+1]
        
                        
#Class containing sentences and their details.
#Its attributes are:
#	inds			a list of the indeces of the words in the sentencs
#	words			a list of the words in the sentencs
#	synt			a list of the POS-tags of the words in the sentencs
#	parse			a list of the parse tree parts relevant for the words in the sentence
#	dep_ind			a list of the indices words of the sentence are refering to in their dependecy graph
#	dep_tag			a list of the dependecy tags of the words of the sentence
#	lstProb			a list of the problems a sentence has
#	lstSoln			a list of the solutions of the problems a sentence has
#	sentenceIndex	the index of the sentence itself
#	lstOther		a list containing other [Noun Number, VForm, WForm] errors 
#	sentDetailobj	a class object referencing the class 'SentenceDetailsModified', containing all the details regarding a sentece
#	OperationMode	a flag on how to procede: can be 'SPEL', 'ART', 'SVA' or 'OTHER'
#
#Its methods are:
#	__init__			constructs the object sentenceLibrary
#	getProblem			detects the error of a given sentence in the given mode
#	wordWiseAddProb		prepares error detection when errors depend on single words and gets errors accordingly
#	sentWiseAddProb		prepares error detection when errors depend on whole sentece and gets errors accordingly
#	get_subj_and_verb	indetifies relevant subject and verb and their missmatches as errors
class sentenceLibrary:
    inds           = None
    words          = None
    synt           = None
    parse          = None
    dep_ind        = None
    dep_tag        = None
    lstProb        = None
    lstSoln        = None
    sentenceIndex  = 0
    lstOther       = None
    
    sentDetailobj  = None
    OperationMode  = ""    #Operation modes are SPEL / OTHER / ART / SVA 
    
	#Constructs the object sentenceLibrary
    def __init__(self,sentDetails,OperationMode):
        self.inds           = sentDetails.inds
        self.words          = sentDetails.words
        self.synt           = sentDetails.synt
        self.parse          = sentDetails.parse
        self.dep_ind        = sentDetails.dep_ind
        self.dep_tag        = sentDetails.dep_tag
        self.lstProb        = sentDetails.lstProb
        self.lstSoln        = sentDetails.lstSoln
        self.sentenceIndex  = sentDetails.sentenceIndex
        self.lstOther       = sentDetails.lstOther
        self.sentDetailobj  = sentDetails
        
        self.OperationMode  = OperationMode
    
	#Decides depending on 'OperationMode' if the problems depend only on single words or on the whole sentence
    def getProblem(self):
        if self.OperationMode in ['SPEL','ART']:
            self.wordWiseAddProb()
        elif self.OperationMode in ['SVA','OTHER']:
            self.sentWiseAddProb()
    
	#Checks the sentence word by word and and then prepares them for error detection of the type given in OperationMode
    def wordWiseAddProb(self):        
        for index in range(len(self.inds)):
            indval  = self.inds[index]
            wordval = self.words[index] 
            syntval = self.synt[index]
            
            if self.OperationMode == 'SPEL':
                #checking for spell checking errors
                rSpel = errDef.ErrorDef("SPEL")
                retValSpel = rSpel.checkSpel(int(indval),wordval,self)
                if retValSpel != 0:
                    self.sentDetailobj.objLstProblems.AddToProblemListTypewise("SPEL",retValSpel)
            
            if self.OperationMode == 'ART':
                #check for NN and NNS
                if (syntval in ['NN','NNS']):
                    rArt = errDef.ErrorDef("ART")
                    retVal = rArt.checkDeterminer(int(indval),syntval,self)
                    if retVal != 0:
                        probStart,probEnd,syntval,errorType = retVal
                        self.sentDetailobj.objLstProblems.AddToProblemListTypewise(errorType,retVal)
    
	#Prepares the error detection according to 'OperationMode' when it depends on the sentence as a whole
    def sentWiseAddProb(self):        
        if self.OperationMode == 'SVA':
            self.get_subj_and_verb()
        
        if self.OperationMode == 'OTHER':
            #checking the mismatch for other error
            for prob in self.lstOther[self.sentenceIndex]:
                self.sentDetailobj.objLstProblems.AddToProblemListTypewise("OTHER",prob)
				
    #Indetifies subject and verb relevant for SVA and their missmatches as errors
    def get_subj_and_verb(self):
        for index in range(len(self.inds)):
            subject_ind = -2
            subject_ref_ind = -3
            verb_ind = -4
            auxpass_ind = -5
            other_verbs = []
            and_subj = False    #needs plural verbs
            or_jubj = False     #only last subject is relevant for SVA
            if self.dep_tag[index] in ["nsubj", "nsubjpass"]:
                #identifying the subject
                subject_ind = int(self.inds[index])
                subject_ref_ind = int(self.dep_ind[index])
                if self.dep_tag[subject_ref_ind] in ["rcmod", "acl:relcl"]:
                    subject_ind = int(self.dep_ind[subject_ref_ind])
                
                for conj in range(len(self.inds)):
                    if self.dep_ind[conj] == str(subject_ind) and self.dep_tag[conj]=="cc":
                        if self.words[conj]=="and":
                            and_subj = True
                        elif self.words[conj]=="or":
                            or_jubj = True
                    if self.dep_ind[conj] == str(subject_ind) and self.dep_tag[conj]=="conj" and or_jubj:
                        subject_ind = conj
                #identifying verb candidates
                for verb in range(len(self.inds)):
                    if self.dep_ind[verb] == str(subject_ref_ind):
                        if self.dep_tag[verb] in ["aux", "cop"]:
                            verb_ind=verb
                            break
                        elif self.dep_tag[verb] == "auxpass":
                            auxpass_ind = verb
                #selecting verb candidate
                if verb_ind == -4:
                    if auxpass_ind == -5:
                        if self.dep_tag[subject_ref_ind] not in ["xcomp"]:
                            verb_ind = subject_ref_ind
                    else:
                        verb_ind = auxpass_ind

                #error detectin
                syntverb = self.synt [verb_ind]	
                if and_subj and verb_ind != -4:
                    #give verb to function asking if it's plural
                    rComp = errDef.ErrorDef("SVACOMPplural")
                    retComp = rComp.checkSVACOMPplural(self.words[verb_ind],verb_ind,syntverb,self)
                    if retComp != 0:
                        self.sentDetailobj.objLstProblems.AddToProblemListTypewise("SVACOMPplural",retComp)
                elif subject_ind != -2 and verb_ind != -4:
                    rComp = errDef.ErrorDef("SVACOMP")
                    retComp = rComp.checkSVACOMP(self.words[subject_ind],subject_ind,self.words[verb_ind],verb_ind,syntverb,self)
                    if retComp != 0:
                        self.sentDetailobj.objLstProblems.AddToProblemListTypewise("SVACOMP",retComp)

