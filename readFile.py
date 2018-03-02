import sentence as sent
import SentenceDetailsModified as sentModi
import pickle

def save_obj(obj, name ):
    #with open('obj/'+ name + '.pkl', 'wb') as f:
        fh = open(name+'.pkl',"wb")
        pickle.dump(obj, fh, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    fh = open(name+'.pkl',"rb")
    return pickle.load(fh)

def readPickleFileSentdet(pickleFileName):    
    #create a list of object of Sentence details
    lstSentencedet = load_obj(pickleFileName)
    return lstSentencedet
          

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


#function for generation of list of words
sentLst        = sent.Sentences()
#sentence details list
#lstSentencedet = readRawFileSentdet("testdata1.con","sentDetlist")    
lstSentencedet = readPickleFileSentdet("sentDetlist")   

#looping through the sentene details objects
for Index in range(0,12):
    sentDet = lstSentencedet[Index]
    #adding in the sentences                
    print(sentDet.words)
    #reinitiate the problem list and other related 
    sentDet.initiateLists()
    #Operation mode Spelling
    sentLib = sentModi.sentenceLibrary(sentDet,"SPEL")
    sentLib.getProblem()
    
    sentDet.listProblems()
    print(sentDet.lstProb)
    #getting the solution
    sentDet.solveProblem()

    sentDet.getSolutionInSentence()
    print(sentDet.words)

#save the sentence details list
save_obj(lstSentencedet,"sentDetlist")    
#
#    sentLst.addSentence(sentDet.getWords())
#
#sentLst.printSentences()
##writing to a file 
#fileW = open("m2file.txt","w")
#fileW.write(sentLst.outStr)
#fileW.close()