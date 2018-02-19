import checkGoogle as cg

class Problem:
    start               = 0
    end                 = 0
    typeProb            = "" 
    lstWords            = None
    lstChecksentoptions = None
    
    def __init__(self,startval,endval,typep,lstWordval):
        self.start    = int(startval)
        self.end      = int(endval)
        self.typeProb = typep
        self.lstWords = lstWordval
        self.lstChecksentoptions = []
        self.genChecklist()
        self.getNgramcount()

    
    def genChecklist(self):        
        size = self.end-self.start+1
        mleft  = 5-size-1
        mRight = 1
        if mleft>self.start:
            allowLeft = int(self.start)
        else:
            allowLeft = int(mleft)
        
        if self.end<len(self.lstWords)-2:
            allowRight = mRight
        else:
            allowRight = 0
        print("in prob",self.typeProb)

        wordLst1   = self.lstWords[self.start-allowLeft:self.start]            
        wordLst2   = self.lstWords[self.end:self.end+allowRight]
        wordLstmid = self.lstWords[self.start:self.end+1]
        
        self.lstChecksentoptions.append([" ".join(wordLst1+wordLstmid + wordLst2),'NA','NA'])
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
            
        #print(self.lstChecksent)
        
    def getNgramcount(self):
        #print(self.lstChecksentoptions)
        for sent,opt,optval in self.lstChecksentoptions:
            #print(sent,opt,optval)
            print(cg.qryGoogle(sent))
        
            
class ProblemList:
    lstProbclassobj = None
    lstProb = None
    lstWords = None
    
    def __init__(self,lstProbval,lstWordval):
        self.lstProb = lstProbval
        self.lstProbclassobj=[]
        self.lstWords = lstWordval
        self.genProbObj()
        
    def genProbObj(self):
        #adding to problem list
        for start,end,typev in self.lstProb:
            print(start,end,typev)
            self.lstProbclassobj.append(Problem(start,end,typev,self.lstWords))
 

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
    
    def __init__(self):
        self.inds    = []
        self.words   = []
        self.synt    = []
        self.parse   = []
        self.lstProb = []
    
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
            retVal = rArt.checkDeterminer(int(indval),syntval)
            if retVal != 0:
                self.lstProb.append(retVal)
            
    def getWords(self):
        return self.words
                
    def solveProblem(self):
        objLstProblems = ProblemList(self.lstProb,self.words)

class ErrorDef:
    #Error types are SPEL / ART / SVACOMP /SVABASE / OTHER
    ErrorType = ""
            
    def __init__(self,etype):
        self.ErrorType = etype
    
    #Determine the Article Determiner  error        
    def checkDeterminer(self,indval,syntval):
        ind = indval
        #checking Sibling items for NP so that and also finding Determiner
        condition = True
        foundDet = False
        lstParse = []
        lstWords = []
        
        probEnd   = 0
        probStart = 0
    
        while (condition):
            condition = 'NP' not in self.parse[ind]
            lstWords.append(self.words[ind])
            lstParse.append(self.parse[ind])
            if (self.synt[ind] is 'det'):
                foundDet = True
            probStart= ind
            #print(self.synt[ind],self.words[ind],self.parse[ind],condition)
            ind= ind-1
        if foundDet is False:
            print("problem found")
            probEnd = indval
            #self.lstProb.append([probStart,probEnd,syntval])
            return [probStart,probEnd,syntval,etype]
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
for i in range(1,2):
    
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
    sentDet.solveProblem()
    sentLst.addSentence(sentDet.getWords())
    #print(synt)
    #print(parse)


sentLst.printSentences()