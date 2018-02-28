class GoogleSentList:
    
    allowLstBefore = None
    allowLstAfter  = None
    allowLstMid    = None
    reduceLstMid   = None
    
    wordLstBefore  = None
    wordLstAfter   = None
    wordLstmid     = None
    lstWords       = None
    errorType      = None
    chkMark        = False
    
    lstChecksentoptions = None
    
    start = 0
    end   = 0
    
    def __init__(self,allowLstBefore, allowLstAfter, allowLstMid, redLstMid, objProb ):
        self.allowLstBefore      = allowLstBefore
        self.allowLstAfter       = allowLstAfter
        self.allowLstMid         = allowLstMid
        self.reduceLstMid        = redLstMid
        
        self.wordLstBefore       = []
        self.wordLstAfter        = []
        self.wordLstmid          = []
        self.lstChecksentoptions = []
        self.lstWords            = objProb.lstWords
        self.start               = objProb.start
        self.end                 = objProb.end
        self.errorType           = objProb.errorType
        self.chkMark             = objProb.chkMarked
        
    def genSentlist(self,allowLeft,allowRight,typeProb):

        if self.reduceLstMid == True:
            startMid = self.start+1
            endMid   = self.end
        else:
            startMid = self.start
            endMid   = self.end

        if self.chkMark == True:
            startMid = startMid+1
            endMid   = self.end
        
        if self.allowLstBefore == True:
            self.wordLstBefore   = self.lstWords[self.start-allowLeft:self.start]            
        if self.allowLstAfter == True:
            self.wordLstAfter   = self.lstWords[self.end+1:self.end+allowRight+1]
        if self.allowLstMid == True:
            self.wordLstmid = self.lstWords[startMid:endMid+1]
            
            
            
        print(self.wordLstmid, startMid,self.start)
        if self.allowLstBefore == True:
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
    
    def genSentlistOther(self,allowLeft,allowRight,typeProb,currentWord,checkList):

        if self.reduceLstMid == True:
            startMid = self.start+1
            endMid   = self.end
        else:
            startMid = self.start
            endMid   = self.end

        if self.chkMark == True:
            startMid = startMid+1
            endMid   = self.end
        
        if self.allowLstBefore == True:
            self.wordLstBefore   = self.lstWords[self.start-allowLeft:self.start]            
        if self.allowLstAfter == True:
            self.wordLstAfter   = self.lstWords[self.end+1:self.end+allowRight+1]
        if self.allowLstMid == True:
            self.wordLstmid = self.lstWords[startMid:endMid+1]
            
            
        #basic case for not changing    
        self.lstChecksentoptions.append([" ".join(self.wordLstBefore + [currentWord] + self.wordLstAfter),'NA',""])
        
        for word in checkList:
            self.lstChecksentoptions.append([" ".join(self.wordLstBefore + [word] + self.wordLstAfter),'REP',word])
                        
        return (self.lstChecksentoptions)



