import checkGoogle as cg
import inflect
p = inflect.engine()
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
    errorType           = ""  #Error types are SPEL / ART / SVACOMP /SVABASE / OTHER / SVACOMPplural
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
		

class SentenceDetails:
    inds = None
    words=None
    synt =None
    parse=None
    dep_ind = None
    dep_tag = None
    lstProb = None
    lstSoln = None
    
    def __init__(self):
        self.inds    = []
        self.words   = []
        self.synt    = []
        self.parse   = []
        self.dep_ind = []
        self.dep_tag = []
        self.lstProb = []
        self.lstSoln = []
    
    def addItems(self,indval,wordval,syntval,parseval,dep_indval,dep_tagval):
        #print(indval,syntval)
        self.inds.append(indval)		#index value
        self.words.append(wordval)		#word value
        self.synt.append(syntval)		#syntax (pos) value
        self.parse.append(parseval)		#parse tree value
        self.dep_ind.append(dep_indval)	#dependency index value
        self.dep_tag.append(dep_tagval)	#dependency tag value
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
        self.get_subj_and_verb()
        print(self.lstProb)
                
    def solveProblem(self):
        objLstProblems = ProblemList(self.lstProb,self.words)
        self.lstSoln = objLstProblems.getSolutions()
        print(self.lstSoln)

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
                print (subject_ind)
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
                syntval = self.synt [verb_ind]
                if and_subj and verb_ind != -4:
                    #give verb to function asking if it's plural
                    print(self.dep_tag[verb_ind],self.words[verb_ind])
                    rComp = ErrorDef("SVACOMPplural")
                    retComp = rComp.checkSVACOMPplural(self.words[verb_ind],verb_ind,syntval,self)
                    if retComp != 0:
                        self.lstProb.append(retComp)
                elif subject_ind != -2 and verb_ind != -4:
                    rComp = ErrorDef("SVACOMP")
                    retComp = rComp.checkSVACOMP(self.words[subject_ind],subject_ind,self.words[verb_ind],verb_ind,syntval,self)
                    if retComp != 0:
                        self.lstProb.append(retComp)
                    print(self.dep_tag[subject_ind],self.words[subject_ind])
                    print(self.dep_tag[verb_ind],self.words[verb_ind])
                


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
    
    def checkSVACOMP(self, subj, subjind, verb, verbind, syntval, sentDet):
        if str(p.singular_noun(subj)) == "False":#subj is singular
            print("singular")
            plural_verb = p.plural_verb(verb)
            if verb != plural_verb:
                return 0
                #print("good")
            else:
                print("SVA problem found")
                return [subjind,verbind,syntval,self.ErrorType]
                
        else:
            print("plural")
            plural_verb = p.plural_verb(verb)
            if verb == plural_verb:
                return 0
                #print("good")
            else:
                print("SVA problem found")
                return [subjind,verbind,syntval,self.ErrorType]
                #print("bad")
    
    def checkSVACOMPplural(self, verb, verbind, syntval, sentDet):
        plural_verb = p.plural_verb(verb)
        #print(plural_verb)
        if verb == plural_verb:
            return 0
        else:
            return [verbind,verbind,syntval,self.ErrorType]
		
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
            sentDet.addItems(elements[3],elements[4],elements[5],elements[8],elements[6],elements[7])
			#elements[3] == index
			#elements[4] == word
			#elements[5] == pos tag
			#elements[8] == part of tree
			#elements[6] == dependency
			#elements[7] == dependency tag
    
       
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