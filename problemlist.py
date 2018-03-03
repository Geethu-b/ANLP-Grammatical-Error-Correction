import problemsolution as prbSoln

'''
Class ProblemTypeList is used to add error against a specific error type into a list.
Its attributed are :

lstProblem          A list of problems   
problemType         This variable specifes the type of problem 
probStartEar        Initialized to the word Index from where the problem/error starts
probEndEar          Initialized to the word Index to which the error spans
synErrorEar         Specifies the POS tag which identifies the error


Its methods are :

__init__            The initialization of a ProblemTypeList object. ProblemType is set to the type of error identified. All internal lists are empty.
addProb             Adds a problem to a list based on the error type.
updateLastProb      It updates the list for a specific error. 
getProblemList      Provides a list of errors based on the error type requested.

'''

class ProblemTypeList:
    lstProblem     = None
    problemType    = None
    probStartEar   = None
    probEndEar     = None
    synErrorEar    = None

    #Constructs the Object ProblemTypeList
    # Input: Error Type such as "ArtChk","SPEL","OTHER" etc.

    def __init__(self,typeProb):
        self.problemType = typeProb
        self.lstProblem  = []
    
    #addProb method takes prb as input which contain "Problem start","Problem End","Tag identifying the error ","Error Type"     
    def addProb(self,prb):
        probStart,probEnd,synError,errorType = prb
                
        if probStart ==self.probStartEar:
            self.updateLastProb(prb)
        else:
            self.lstProblem.append(prb)
        
        self.probStartEar = probStart
        self.probEndEar   = probEnd
        self.synErrorEar  = synError

    #updateLastProb method is used to update the problem list
        
    def updateLastProb(self,prb):
        self.lstProblem[len(self.lstProblem)-1]=prb
    
    # getProblemList method is used to get the complete problem list against an error type.
    def getProblemList(self):
        return self.lstProblem 


'''
#Class ProblemList contains all error lists.
Its attributes are 

lstProbSolnclassobj 
lstSolutions                solutions list
lstProb                     a combined list with all the problems for all error types    
lstWords                    list of words that forms the sentence with error.       
    
#different lists for different error types
lstArtChk                   Class object for problemtype Article where the determiner is present.
lstArt                      Class object for problemtype Article where the determiner is not present and needs to be determined.
lstSpel                     Class object for problemtype Spelling error.
lstSVABase                  Class object for problemtype Subject verb agreement error basic type.
lstSVAComp                  Class object for problemtype Subject verb agreemnet error complex type.
lstSVACompPlu               Class object for problemtype Subject verb agreemnet error complex  plural type.
lstOther                    Class object for problemtype Other Errors such as WFORM,VFORM, Noun Number.

Its methods are :


__init__                    The initialization of a ProblemList object. lstWordval is list of words in a sentence that has an error. It is given as an input. 
AddToProblemListTypewise    Based on the error type, it add the problems that are passed to it to the respective list 
getProblemList              Method to combine all the problem lists into a single list 
genProbSolnObj              generates a ProblemSolution object 
getSolutions                generates the solutions
'''

            
class ProblemList:
    lstProbSolnclassobj = None
    lstSolutions    = None
    lstProb         = None
    lstWords        = None
    
    #different lists for different error types
    lstArtChk       = None
    lstArt          = None
    lstSpel         = None
    lstSVABase      = None
    lstSVAComp      = None
    lstSVACompPlu   = None
    lstOther        = None


    #Constructs the Object ProblemList
    # Input: list of words that forms the sentence with error.
    def __init__(self,lstWordval):
        self.lstProb             = []
        self.lstProbSolnclassobj = []
        self.lstSolutions        = []
        self.lstWords            = lstWordval
        #initiate lists
        self.lstArtChk           = ProblemTypeList("ArtChk")
        self.lstArt              = ProblemTypeList("ART")
        self.lstSpel             = ProblemTypeList("SPEL")
        self.lstSVABase          = ProblemTypeList("SVABASE")
        self.lstSVAComp          = ProblemTypeList("SVACOMP")
        self.lstSVACompPlu       = ProblemTypeList("SVACOMPplural")
        self.lstOther            = ProblemTypeList("OTHER")


    #AddToProblemListTypewise method add the problems that are passed to it to the respective error list     
    def AddToProblemListTypewise(self, errorType,prb): 
        if errorType == "ART":
            self.lstArt.addProb(prb)
        elif errorType == "ArtChk":
            self.lstArtChk.addProb(prb)
        elif errorType == "SPEL":
            self.lstSpel.addProb(prb)
        elif errorType == "SVABASE":
            self.lstSVABase.addProb(prb)
        elif errorType == "SVACOMP":
            self.lstSVAComp.addProb(prb)
        elif errorType == "SVACOMPplural":
            self.lstSVACompPlu.addProb(prb)
        elif errorType == "OTHER":
            self.lstOther.addProb(prb)


    # getProbList Method combines all the problem lists into a single list        
    def getProbList(self):
        self.lstProb = self.lstArt.getProblemList() + self.lstArtChk.getProblemList() + self.lstSpel.getProblemList() + self.lstSVABase.getProblemList() +self.lstSVAComp.getProblemList() +self.lstSVACompPlu.getProblemList() +self.lstOther.getProblemList()
        self.genProbSolnObj()
        return self.lstProb


    #genProbSolnObj method generates a ProblemSolution object which hold all the solution for each problem identified.  
    def genProbSolnObj(self):
        #adding to problem list
        for start,end,typev,errorType in self.lstProb:
            #print(start,end,typev,errorType)
            self.lstProbSolnclassobj.append(prbSoln.ProblemSolution(start,end,typev,errorType,self.lstWords))
            
    #getSolutions method returns the list of solutions
    def getSolutions(self):
        for prob in self.lstProbSolnclassobj:
            self.lstSolutions.append(prob.getSolution())
        return self.lstSolutions