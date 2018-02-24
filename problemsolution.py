import GoogleSentList as googSentList
import checkGoogle as cg

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
        if self.errorType in ['ArtChk','SPEL']:
            self.chkMarked       = True
            self.chkWord         = lstWordval[self.start]
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
            #print("Try to remove both wing")
            genSentence              = googSentList.GoogleSentList(False,False,True,False,self)
            self.lstChecksentoptions = genSentence.genSentlist(self.allowLeft,self.allowRight,self.typeProb)
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
            #setting threshold to 1000
            if outVal < 500:
                outVal =0
            #giving a extra score for ArtChk Checked Word
            if outVal !=0 and optval==self.chkWord and self.errorType in ['ArtChk']:
                outVal +=20000
            print(sent,opt,optval,self.chkWord)
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
            
        #checking for ArtChk 
        if self.errorType == 'ArtChk':
            if self.bestOpt=='NA':
                self.solution = [self.start,'REP','']
            elif self.bestOpt=='INB' and self.bestOptval == self.lstWords[self.start]:
                self.solution = [self.start,'NA','']
            else:
                self.solution = [self.start,'REP',self.bestOptval]
    def getSolution(self):
        return self.solution