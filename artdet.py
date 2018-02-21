import checkGoogle as cg

class GoogleSentList:
    
    allowLstBefore = None
    allowLstAfter  = None
    allowLstMid    = None
    reduceLstMid   = None
    
    wordLstBefore  = None
    wordLstAfter   = None
    wordLstmid     = None
    lstWords       = None
    
    lstChecksentoptions = None
    
    start = 0
    end   = 0
    
    def __init__(self,allowLstBefore, allowLstAfter, allowLstMid, redLstMid, lstWords, prbStart, prbEnd ):
        self.allowLstBefore      = allowLstBefore
        self.allowLstAfter       = allowLstAfter
        self.allowLstMid         = allowLstMid
        self.reduceLstMid        = redLstMid
        
        self.wordLstBefore       = []
        self.wordLstAfter        = []
        self.wordLstmid          = []
        self.lstChecksentoptions = []
        self.lstWords            = lstWords
        self.start               = prbStart
        self.end                 = prbEnd
        
    def genSentlist(self,allowLeft,allowRight,typeProb):
        if self.reduceLstMid == True:
            startMid = self.start+1
            endMid   = self.end
        else:
            startMid = self.start
            endMid   = self.end
        
        if self.allowLstBefore == True:
            self.wordLstBefore   = self.lstWords[self.start-allowLeft:self.start]            
        if self.allowLstAfter == True:
            self.wordLstAfter   = self.lstWords[self.end+1:self.end+allowRight+1]
        if self.allowLstMid == True:
            self.wordLstmid = self.lstWords[startMid:endMid+1]
        self.lstChecksentoptions.append([" ".join(self.wordLstBefore+self.wordLstmid + self.wordLstAfter),'NA',""])
        if typeProb == "NN":
            #a , an ,the replace candidate
            self.lstChecksentoptions.append([" ".join(self.wordLstBefore+["a"]+self.wordLstmid + self.wordLstAfter),'INB','a'])
            self.lstChecksentoptions.append([" ".join(self.wordLstBefore+["an"]+self.wordLstmid + self.wordLstAfter),'INB','an'])
            self.lstChecksentoptions.append([" ".join(self.wordLstBefore+["the"]+self.wordLstmid + self.wordLstAfter),'INB','the'])
            #print(self.lstChecksent)
        else:
            #the replace candidate
            self.lstChecksentoptions.append([" ".join(self.wordLstBefore+["the"]+self.wordLstmid + self.wordLstAfter),'INB','the'])
            
        return (self.lstChecksentoptions)
    

class Problem:
    start               = 0
    end                 = 0
    size                = 0
    typeProb            = "" 
    errorType           = ""  #Error types are SPEL / ART / SVACOMP /SVABASE / OTHER
    lstWords            = None
    lstChecksentoptions = None
    allowLeft           = 0
    allowRight          = 0
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
        self.problemCondition    = False
        self.errorType           = errorTypeval
        self.lstWords            = lstWordval
        self.lstChecksentoptions = []
        self.solution            = []
        self.genChecklist()
        if self.problemCondition == True:
            self.getNgramcount()
            self.scoreCheck()

    
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
            genSentence              = GoogleSentList(True,True,True,False,self.lstWords,self.start,self.end)
            self.lstChecksentoptions =  genSentence.genSentlist(self.allowLeft,self.allowRight,self.typeProb)
        else:
            #Solution  is none at this case            
            self.solution=[self.start,"NA",""]
                
            
        
    def reChkRedSize(self):
        retVal = 0 
        if self.size==3:                    
            print("Reducing the Size for the Case of 3 ")
            genSentence              = GoogleSentList(True,True,True,True,self.lstWords,self.start,self.end)
            self.lstChecksentoptions =  genSentence.genSentlist(self.allowLeft,self.allowRight,self.typeProb)
            self.getNgramcount()
            if self.bestScore>0:
                return 1
            print("Try to remove Right wing")
            genSentence              = GoogleSentList(True,False,True,True,self.lstWords,self.start,self.end)
            self.lstChecksentoptions =  genSentence.genSentlist(self.allowLeft,self.allowRight,self.typeProb)
            self.getNgramcount()
            if self.bestScore>0:
                return 1
            print("Try to remove left wing")
            genSentence              = GoogleSentList(False,True,True,True,self.lstWords,self.start,self.end)
            self.lstChecksentoptions =  genSentence.genSentlist(self.allowLeft,self.allowRight,self.typeProb)
            self.getNgramcount()
            if self.bestScore>0:
                return 1

            print("Try to remove both wing")
            genSentence              = GoogleSentList(False,False,True,True,self.lstWords,self.start,self.end)
            self.lstChecksentoptions =  genSentence.genSentlist(self.allowLeft,self.allowRight,self.typeProb)
            self.getNgramcount()
            if self.bestScore>0:
                return 1


        if self.size<=2:
            print("Try to remove Right wing")
            genSentence              = GoogleSentList(True,False,True,False,self.lstWords,self.start,self.end)
            self.lstChecksentoptions =  genSentence.genSentlist(self.allowLeft,self.allowRight,self.typeProb)
            self.getNgramcount()
            if self.bestScore>0:
                return 1
            print("Try to remove left wing")
            genSentence              = GoogleSentList(False,True,True,False,self.lstWords,self.start,self.end)
            self.lstChecksentoptions =  genSentence.genSentlist(self.allowLeft,self.allowRight,self.typeProb)
            self.getNgramcount()
            if self.bestScore>0:
                return 1
            print("Try to remove both wing")
            genSentence              = GoogleSentList(False,False,True,False,self.lstWords,self.start,self.end)
            self.lstChecksentoptions =  genSentence.genSentlist(self.allowLeft,self.allowRight,self.typeProb)
            self.getNgramcount()
            if self.bestScore>0:
                return 1
            
        return retVal
        
    def getNgramcount(self):
        self.bestScore  = 0
        self.bestOpt    = ""
        self.bestOptval = ""
        # get the best value to determine the solution
        for sent,opt,optval in self.lstChecksentoptions:
            #print(sent,opt,optval)
            outVal = cg.qryGoogle(sent)
            print(outVal)
            if outVal>self.bestScore:
                self.bestScore  = outVal
                self.bestOpt    = opt
                self.bestOptval = optval
        #if no best score is found the solution is not applicable
     
    def scoreCheck(self):   
        if self.bestScore ==0:
            if self.reChkRedSize() == 0:
                self.solution=[self.start,"NA",""]
            else:
                self.solution = [self.start,self.bestOpt,self.bestOptval]
        else:
            self.solution = [self.start,self.bestOpt,self.bestOptval]
        
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
for i in range(11,12):
    
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
    #print(sentDet.getWords())
    print(sentDet.words)
    print(sentDet.synt)
    print(sentDet.parse)
    sentDet.listProblems()
    sentDet.solveProblem()
    sentLst.addSentence(sentDet.getWords())
    #print(synt)
    #print(parse)


sentLst.printSentences()