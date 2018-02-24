import problemlist as prbList
import ErrorDef as errDef

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
    lstProb     = None
    lstSoln     = None
    objLstProblems = None
    
    def __init__(self):
        self.inds         = []
        self.words        = []
        self.synt         = []
        self.parse        = []
        self.lstProb      = []
        self.lstSoln      = []
        self.objLstProblems = prbList.ProblemList(self.words)
    
    def addItems(self,indval,wordval,syntval,parseval):
        #print(indval,syntval)
        self.inds.append(indval)
        self.words.append(wordval)
        self.synt.append(syntval)
        self.parse.append(parseval)
        #check for NN and NNS
        if (syntval in ['NN','NNS']):
            rArt = errDef.ErrorDef("ART")
            retVal = rArt.checkDeterminer(int(indval),syntval,self)
            if retVal != 0:
                probStart,probEnd,syntval,errorType = retVal
                self.objLstProblems.AddToProblemListTypewise(errorType,retVal)
            
    def getWords(self):
        return self.words
    
    def listProblems(self):
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
