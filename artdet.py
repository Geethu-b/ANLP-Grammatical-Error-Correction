import checkGoogle as cg

class Problem:
    start               = 0
    end                 = 0
    typeProb            = "" 
    errorType           = ""  #Error types are SPEL / ART / SVACOMP /SVABASE / OTHER
    lstWords            = None
    lstChecksentoptions = None
    #solution is an array which has 3 para
    #para 1 : start of the word list
    #para 2 : Solution type INB / INA /   NA / REP are the solutions
    #para 3 : for before insert the text to be inserted for NA and Replace option
    # the text will be blank
    solution            = None
    
    def __init__(self,startval,endval,typep,errorTypeval,lstWordval):
        self.start               = int(startval)
        self.end                 = int(endval)
        self.typeProb            = typep
        self.errorType           = errorTypeval
        self.lstWords            = lstWordval
        self.lstChecksentoptions = []
        self.solution            = []
        self.genChecklist()
        self.getNgramcount()

    
    def genChecklist(self):        
        
        problemCondition = True
        size = self.end-self.start+1
        
        if size<=2:
            mleft  = 1
            mRight = 1 
        elif size<=3:
            mleft  = 1
            mRight = 0
        else:
            problemCondition = False
            
        if mleft>self.start:
            allowLeft = int(self.start)
        else:
            allowLeft = int(mleft)
        
        if self.end<len(self.lstWords)-2:
            allowRight = mRight
        else:
            allowRight = 0
            
        # Going in the details of the problem
        if problemCondition == True:
            self.genSentlist(allowLeft,allowRight)
        else:
            #Solution  is none at this case
            
            self.solution=[self.start,"NA",""]
                
            
    def genSentlist(self,allowLeft,allowRight):
        #print("in prob",self.typeProb, allowLeft,allowRight, size,self.end+allowRight)
        wordLst1   = self.lstWords[self.start-allowLeft:self.start]            
        wordLst2   = self.lstWords[self.end+1:self.end+allowRight+1]
        wordLstmid = self.lstWords[self.start:self.end+1]
        #print(wordLst1)
        #print(wordLst2)
        self.lstChecksentoptions.append([" ".join(wordLst1+wordLstmid + wordLst2),'NA',""])
        if self.typeProb == "NN":
            #print("in prob",self.typeProb)
            #a , an ,the replace candidate
            self.lstChecksentoptions.append([" ".join(wordLst1+["a"]+wordLstmid + wordLst2),'IN','a'])
            self.lstChecksentoptions.append([" ".join(wordLst1+["an"]+wordLstmid + wordLst2),'IN','an'])
            self.lstChecksentoptions.append([" ".join(wordLst1+["the"]+wordLstmid + wordLst2),'IN','the'])
            #print(self.lstChecksent)
        else:
            #the replace candidate
            self.lstChecksentoptions.append([" ".join(wordLst1+["the"]+wordLstmid + wordLst2),'IN','the'])
            
        print(self.lstChecksentoptions)
        
    def getNgramcount(self):
        bestScore  = 0
        bestOpt    = ""
        bestOptval = ""
        # get the best value to determine the solution
        for sent,opt,optval in self.lstChecksentoptions:
            #print(sent,opt,optval)
            outVal = cg.qryGoogle(sent)
            print(outVal)
            if outVal>bestScore:
                bestScore  = outVal
                bestOpt    = opt
                bestOptval = optval
        #if no best score is found the solution is not applicable
        
        if bestScore ==0:
            self.solution = [self.start,"NA",""]
        else:
            self.solution = [self.start,bestOpt,bestOptval]
        
    def getSolution(self):
        return self.solution
            
class ProblemList:
    lstProbclassobj = None
    lstSolutions    = None
    lstProb         = None
    lstWords        = None
    
    def __init__(self,lstProbval,lstWordval):
        self.lstProb         = lstProbval
        self.lstProbclassobj = []
        self.lstSolutions    = []
        self.lstWords        = lstWordval
        self.genProbObj()
        
    def genProbObj(self):
        #adding to problem list
        for start,end,typev,errorType in self.lstProb:
            print(start,end,typev,errorType)
            self.lstProbclassobj.append(Problem(start,end,typev,errorType,self.lstWords))
    
    def getSolutions(self):
        for prob in self.lstProbclassobj:
            self.lstSolutions.append(prob.getSolution())
        return self.lstSolutions

class Sentences:
    lstSent =None
    def __init__(self):
        self.lstSent=[]
    
    def addSentence(self,words):
        #print(words)
        self.lstSent.append(" ".join(words))
    
    def printSentences(self):
        for i in range(0,len(self.lstSent)):
            print(self.lstSent[i])
    
class SentenceDetails:
    inds = None
    words=None
    synt =None
    parse=None
    lstProb = None
    lstSoln = None
    
    def __init__(self):
        self.inds    = []
        self.words   = []
        self.synt    = []
        self.parse   = []
        self.lstProb = []
        self.lstSoln = []
    
    def addItems(self,indval,wordval,syntval,parseval):
        #print(indval,syntval)
        self.inds.append(indval)
        self.words.append(wordval)
        self.synt.append(syntval)
        self.parse.append(parseval)
        #check for NN and NNS
        if (syntval in ['NN','NNS']):
            #print("hi")
            rArt = ErrorDef("ART")
            retVal = rArt.checkDeterminer(int(indval),syntval,self)
            if retVal != 0:
                self.lstProb.append(retVal)
            
    def getWords(self):
        return self.words
    
    def listProblems(self):
        print(self.lstProb)
                
    def solveProblem(self):
        objLstProblems = ProblemList(self.lstProb,self.words)
        self.lstSoln = objLstProblems.getSolutions()
        print(self.lstSoln)

class ErrorDef:
    #Error types are SPEL / ART / SVACOMP /SVABASE / OTHER
    ErrorType = ""
            
    def __init__(self,etype):
        self.ErrorType = etype
    
    #Determine the Article Determiner  error        
    def checkDeterminer(self,indval,syntval,sentDet):
        ind = indval
        #checking Sibling items for NP so that and also finding Determiner
        condition = True
        foundDet = False
        lstParse = []
        lstWords = []
        
        probEnd   = 0
        probStart = 0
    
        while (condition):
            condition = 'NP' not in sentDet.parse[ind]
            lstWords.append(sentDet.words[ind])
            lstParse.append(sentDet.parse[ind])
            if (sentDet.synt[ind] == 'DT'):
                foundDet = True
            probStart= ind
            #print(self.synt[ind],self.words[ind],self.parse[ind],condition)
            ind= ind-1
        if foundDet is False:
            print("problem found")
            probEnd = indval
            #self.lstProb.append([probStart,probEnd,syntval])
            return [probStart,probEnd,syntval,self.ErrorType]
        else:
            foundDet = False
        return 0
        
            
#function for generation of list of words
sentLst = Sentences()

#file of the test data
fileTest  = open("testdata1.con","r").read()
#listing the values according to the sentences
lTest  = fileTest.split('\n\n')
#print(lTest[2])


#for i in range(0,len(lTest)):
for i in range(8,9):
    
    lines = lTest[i].split('\n')
    sentDet = SentenceDetails()    
    #getting the words 
    for j in range(0,len(lines)):
        #seperate by tab        
        if len(lines[j])>0:
            elements = lines[j].split('\t')
            #print(elements[3],elements[4],elements[5],elements[8])
            sentDet.addItems(elements[3],elements[4],elements[5],elements[8])
    
       
    #adding in the sentences                
    print(sentDet.getWords())
    sentDet.listProblems()
    sentDet.solveProblem()
    sentLst.addSentence(sentDet.getWords())
    #print(synt)
    #print(parse)


sentLst.printSentences()