import problemlist as prbList
import ErrorDef as errDef
from treetagger import TreeTagger

class Sentences:
    lstSent = None
    outStr  = None
    def __init__(self):
        self.lstSent = []
        self.outStr  = ""
    
    def addSentence(self,words):
        #print(words)
        self.lstSent.append(" ".join(words))
    
    def printSentences(self):
        for i in range(0,len(self.lstSent)):
            self.outStr = self.outStr +self.lstSent[i] + "\n"
            
        print(self.outStr)
    
    
class SentenceDetails:
    inds        = None
    words       = None
    synt        = None
    parse       = None
    dep_ind     = None
    dep_tag     = None
    lstProb     = None
    lstSoln     = None
    objLstProblems = None
    
    def __init__(self):
        self.inds         = []
        self.words        = []
        self.synt         = []
        self.parse        = []
        self.dep_ind      = []
        self.dep_tag      = []
        self.lstProb      = []
        self.lstSoln      = []
        self.objLstProblems = prbList.ProblemList(self.words)
    
    def addItems(self,indval,wordval,syntval,parseval,depnumval, depvalue):
        #print(indval,syntval)
        self.inds.append(indval)
        self.words.append(wordval)
        self.synt.append(syntval)
        self.parse.append(parseval)
        self.dep_ind.append(depnumval)
        self.dep_tag.append(depvalue)
#        #checking for spell checking errors
#        rSpel = errDef.ErrorDef("SPEL")
#        retValSpel = rSpel.checkSpel(int(indval),wordval,self)
#        if retValSpel != 0:
#            self.objLstProblems.AddToProblemListTypewise("SPEL",retValSpel)
#        #check for NN and NNS
#        if (syntval in ['NN','NNS']):
#            rArt = errDef.ErrorDef("ART")
#            retVal = rArt.checkDeterminer(int(indval),syntval,self)
#            if retVal != 0:
#                probStart,probEnd,syntval,errorType = retVal
#                self.objLstProblems.AddToProblemListTypewise(errorType,retVal)
            
    def getWords(self):
        return self.words
    
    def listProblems(self):
        #self.get_subj_and_verb()
        #checking the mismatch for other error
        self.getOtherError()
        #problem listing
        self.lstProb = self.objLstProblems.getProbList()

        #print(self.lstProb)
                
    def solveProblem(self):
        self.lstSoln = self.objLstProblems.getSolutions()
        print(self.lstSoln)
    
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
        
    def get_subj_and_verb(self):
        #add rules for conjunctions
        #verbs --> how does it work?
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
                if self.dep_tag[subject_ref_ind]=="rcmod":
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
                        verb_ind = subject_ref_ind
                    else:
                        verb_ind = auxpass_ind
                        #other_verbs = []
                syntverb = self.synt [verb_ind]	
                if and_subj and verb_ind != -4:
                    #give verb to function asking if it's plural
                    #print(self.words[verb_ind])
                    #rComp = errDef.ErrorDef("X")
                    rComp = errDef.ErrorDef("SVACOMPplural")
                    retComp = rComp.checkSVACOMPplural(self.words[verb_ind],verb_ind,syntverb,self)
                    if retComp != 0:
                        self.objLstProblems.AddToProblemListTypewise("SVACOMPplural",retComp)
                elif subject_ind != -2 and verb_ind != -4:
                    #print(self.words[verb_ind])
                    rComp = errDef.ErrorDef("SVACOMP")
                    retComp = rComp.checkSVACOMP(self.words[subject_ind],subject_ind,self.words[verb_ind],verb_ind,syntverb,self)
                    #print(retComp)
                    if retComp != 0:
                        self.objLstProblems.AddToProblemListTypewise("SVACOMP",retComp)


    def getOtherError(self):
        print("we are here pleas print")
        tt = TreeTagger(language='english')
        #getting the Stanford parse list
        testSentence = " ".join(self.words)
        print(len(self.words))
        # print(sentDet.words)
        print(self.synt)
        StanParserLst = []
        StanParserLst = self.synt
        # print(StanParserLst)
        
        outLst = tt.tag(testSentence)
        tagLst  =[]
        tagChangeDic ={'NP':'NNP','NPS':'NNPS','PP':'PRP','SENT':'.','(':'-LRB-', ')':'-RRB-'}

        for word,tag,form in outLst:
            if tag in tagChangeDic.keys():
                tagLst.append(tagChangeDic.get(tag))
            else:
                tagLst.append(tag)
        print(tagLst)
        print(len(StanParserLst))
        print(len(tagLst))
        if len(self.synt)==len(tagLst):
            SPlst = []
            TTlst = []
            i = 0
            while(i < len(self.synt)):
                print(self.synt[i],tagLst[i])
                if self.synt[i] != tagLst[i]:
                    print("i am ahere")
                    #create object for the error def
                    objOthererr = errDef.ErrorDef("OTHER")
                    retVal = objOthererr.checkOther(i,self.synt[i],self)
                    print(retVal)
                    if retVal != 0:
                        self.objLstProblems.AddToProblemListTypewise("OTHER",retVal)
                i += 1


                
