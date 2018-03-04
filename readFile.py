import sentence as sent
import SentenceDetailsModified as sentModi
import pickle

#Saves a given object under a given name as a .pkl file
#input:
#	obj		the given object
#	name	a string containing the name the object is saved under
def save_obj(obj, name ):
    #with open('obj/'+ name + '.pkl', 'wb') as f:
        fh = open(name+'.pkl',"wb")
        pickle.dump(obj, fh, pickle.HIGHEST_PROTOCOL)

#Loads a .pkl file of a given name
#input:
#	name			the name of the .pkl file
#output:
#	pickle.load(fh)	the content of the .pkl file
def load_obj(name ):
    fh = open(name+'.pkl',"rb")
    return pickle.load(fh)

#Creats a list of objects of Sentence Details from a .pkl file
#input:
#	name			the name of the .pkl file
#output:
#	lstSentencedet	the list of Sentence Details
def readPickleFileSentdet(pickleFileName):    
    #create a list of object of Sentence details
    lstSentencedet = load_obj(pickleFileName)
    return lstSentencedet
          
#Creats a list of objects of Sentence Details from a text file and saving it as .pkl file
#input:
#	filename		the name of the text file
#	pickleFileName	the name of the .pkl file
#output:
#	lstSentencedet	the list of Sentence Details
def readRawFileSentdet(filename,pickleFileName):    
    #file of the test data
    fileTest  = open(filename,"r").read()
    #listing the values according to the sentences
    lTest  = fileTest.split('\n\n')
    #manually adding some 23
    lTest.insert(23,"1	4	2	0	''	''	-	-	*))")
    
    #read the other type error problem list
    lstOther = load_obj("lstOther")
        
    #create a list of object of Sentence details
    lstSentencedet = []
    
    #for i in range(0,len(lTest)):
    for i in range(0,1312):    
        lines = lTest[i].split('\n')
        sentDet = sentModi.SentenceDetailsModified(i,lstOther)    
        #Number of lines to go
        targetLines = len(lines)
        if i == 22:
            targetLines = len(lines)-1
        #getting the words 
        for j in range(0,targetLines):
            #seperate by tab        
            if len(lines[j])>0:
                elements = lines[j].split('\t')
                #print(elements[3],elements[4],elements[5],elements[8])
                sentDet.addItems(elements[3],elements[4],elements[5],elements[8],elements[6],elements[7])
           
        lstSentencedet.append(sentDet)
        
    #saving to a file for transport
    save_obj(lstSentencedet,pickleFileName)
    return lstSentencedet

def runOperationWise(Operation,picklefilename,optionRetag=False):
    #looping through the sentene details objects
    for Index in range(0,1312):
        sentDet = lstSentencedet[Index]
        #adding in the sentences                
        print(sentDet.words)
        #reinitiate the problem list and other related 
        sentDet.initiateLists()
        #Operation mode Spelling
        sentLib = sentModi.sentenceLibrary(sentDet,Operation)
        sentLib.getProblem()
        
        sentDet.listProblems()
        print(sentDet.lstProb)
        #getting the solution
        sentDet.solveProblem()
    
        sentDet.getSolutionInSentence()
        if optionRetag == True:
            sentDet.getSolutionInTag()
            
    #save the sentence details list
    save_obj(lstSentencedet,picklefilename)    

#Read the conll test data file and generate the pickle file containing corrections for spelling errors.
lstSentencedet = readRawFileSentdet("testdata1.con","sentDetlist")    
runOperationWise("SPEL","spel",True)

# Read the Spelling error pickle file and generate the pickle file containing corrections for Other errors.
lstSentencedet = readPickleFileSentdet("spel") 
runOperationWise("OTHER","other",True)
 
# Read the Other error pickle file and generate the pickle file containing corrections for SVA errors.
lstSentencedet = readPickleFileSentdet("other")   
runOperationWise("SVA","sva",True)

# Read the SVA error pickle file and generate the pickle file containing corrections for Article or determiner errors.
lstSentencedet = readPickleFileSentdet("sva")   
runOperationWise("ART","all")
