import problemlist as prbList
import ErrorDef as errDef

import os
import nltk

from nltk.tag import StanfordPOSTagger
os.environ['JAVAHOME'] = "C:/Program Files/Java/jre1.8.0_151/bin"



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
        
    def initiateLists(self):
        self.objLstProblems = prbList.ProblemList(self.words)
        self.lstProb        = []
        self.lstSoln        = []

    
    def addItems(self,indval,wordval,syntval,parseval,depnumval, depvalue):
        #print(indval,syntval)
        self.inds.append(indval)
        self.words.append(wordval)
        self.synt.append(syntval)
        self.parse.append(parseval)
        self.dep_ind.append(depnumval)
        self.dep_tag.append(depvalue)
             
    def getWords(self):
        return self.words

    
    def listProblems(self):
        #initiate
        self.lstProb = self.objLstProblems.getProbList()
                    
    def solveProblem(self):
        #initiate
        self.lstSoln = self.objLstProblems.getSolutions()
        print(self.lstSoln)
        
    def getSolutionInTag(self):
        english_postagger = StanfordPOSTagger("F:/Potsdam_courses/ANLP/project/grammar_error/stanford-postagger-2017-06-09/models/english-bidirectional-distsim.tagger","F:/Potsdam_courses/ANLP/project/grammar_error/stanford-postagger-2017-06-09/stanford-postagger.jar")
        print(self.synt)
        #retag the sentence again
        new_tag_values = english_postagger.tag(self.words)      
        for index in range(len(self.words)):
            print(index)
            word,tag = new_tag_values[index]
            self.synt[index] = tag
    
    def getSolutionInSentence(self):
        #sort the list of solutions
        self.lstSoln.sort(key=lambda x: x[0])
        for ind,Operation,Operand in self.lstSoln[::-1]:
            #print (ind,Operation,Operand)
            if Operation == 'INB':  
                #print("hello")
                self.words= self.words[0:ind]+[Operand]+self.words[ind:len(self.words)+1]
            elif Operation == 'REP':
                #print(self.words[0:ind],[Operand])
                if Operand == '':
                    self.words= self.words[0:ind]+self.words[ind+1:len(self.words)+1]
                else:
                    self.words= self.words[0:ind]+[Operand]+self.words[ind+1:len(self.words)+1]
                
        #print(self.lstSoln)
        
                        

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
        
    def getProblem(self):
        if self.OperationMode in ['SPEL','ART']:
            self.wordWiseAddProb()
        elif self.OperationMode in ['SVA','OTHER']:
            self.sentWiseAddProb()
    
    def wordWiseAddProb(self):
        
        for index in range(len(self.inds)):
            indval  = self.inds[index]
            wordval = self.words[index] 
            syntval = self.synt[index]
            
            if self.OperationMode == 'SPEL':
                #print("in lib")
                #checking for spell checking errors
                rSpel = errDef.ErrorDef("SPEL")
                retValSpel = rSpel.checkSpel(int(indval),wordval,self)
                #print(retValSpel)
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
    
    def sentWiseAddProb(self):        
        if self.OperationMode == 'SVA':
            self.get_subj_and_verb()
        
        if self.OperationMode == 'OTHER':
            #checking the mismatch for other error
            for prob in self.lstOther[self.sentenceIndex]:
                #print(prob)
                self.sentDetailobj.objLstProblems.AddToProblemListTypewise("OTHER",prob)
    
    def get_subj_and_verb(self):
        print("i am here")
        #add rules for conjunctions
        #verbs --> how does it work? #a lot -> look at how to detect this
        for index in range(len(self.inds)):
            subject_ind = -2
            subject_ref_ind = -3
            verb_ind = -4
            auxpass_ind = -5
            other_verbs = []
            and_subj = False    #needs plural verbs
            or_jubj = False     #last subject is relevant for SVA
            if self.dep_tag[index] in ["nsubj", "nsubjpass"]:
                subject_ind = int(self.inds[index])
                subject_ref_ind = int(self.dep_ind[index])
                #print (subject_ind)
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
                        
                for verb in range(len(self.inds)):
                    if self.dep_ind[verb] == str(subject_ref_ind):
                        if self.dep_tag[verb] in ["aux", "cop"]:
                            verb_ind=verb
                            break
                        elif self.dep_tag[verb] == "auxpass":
                            auxpass_ind = verb
                        #elif self.dep_tag[verb] == "conj":
                        #    other_verbs.append[verb]
                if verb_ind == -4:
                    if auxpass_ind == -5:
                        if self.dep_tag[subject_ref_ind] not in ["xcomp"]:
                            verb_ind = subject_ref_ind
                    else:
                        verb_ind = auxpass_ind
                        #other_verbs = []
                #print(self.words[verb_ind])	
                # if self.dep_tag[subject_ref_ind] not in ["xcomp"]:
                    # verb_ind = subject_ref_ind
                    # #print("not xcomp")
                # else:
                    # verb_ind = -4					
                    # #print("xcomp")
                #print(self.words[verb_ind])	
                syntverb = self.synt [verb_ind]	
                if and_subj and verb_ind != -4:
                    #give verb to function asking if it's plural
                    print(self.words[verb_ind])
                    #rComp = errDef.ErrorDef("X")
                    rComp = errDef.ErrorDef("SVACOMPplural")
                    retComp = rComp.checkSVACOMPplural(self.words[verb_ind],verb_ind,syntverb,self)
                    if retComp != 0:
                        self.sentDetailobj.objLstProblems.AddToProblemListTypewise("SVACOMPplural",retComp)
                elif subject_ind != -2 and verb_ind != -4:
                    #print(self.words[verb_ind])
                    rComp = errDef.ErrorDef("SVACOMP")
                    retComp = rComp.checkSVACOMP(self.words[subject_ind],subject_ind,self.words[verb_ind],verb_ind,syntverb,self)
                    print(retComp)
                    if retComp != 0:
                        self.sentDetailobj.objLstProblems.AddToProblemListTypewise("SVACOMP",retComp)

