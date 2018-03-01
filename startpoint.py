import sentence as sent
import pickle

def save_obj(obj, name ):
    #with open('obj/'+ name + '.pkl', 'wb') as f:
        fh = open(name+'.pkl',"wb")
        pickle.dump(obj, fh, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    fh = open(name+'.pkl',"rb")
    return pickle.load(fh)
      
#function for generation of list of words
sentLst = sent.Sentences()

#file of the test data
fileTest  = open("testdata1.con","r").read()
#listing the values according to the sentences
lTest  = fileTest.split('\n\n')

#manually adding some 23
lTest.insert(23,"1	4	2	0	''	''	-	-	*))")

#read the other type error problem list
lstOther = load_obj("lstOther")
    
#for i in range(0,len(lTest)):
for i in range(91,92):
    
    lines = lTest[i].split('\n')
    sentDet = sent.SentenceDetails(i,lstOther)    
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
       
    #adding in the sentences                
    print(sentDet.words)
    sentDet.listProblems()
    print(sentDet.lstProb)
    sentDet.solveProblem()
    sentDet.getSolutionInSentence()

    sentLst.addSentence(sentDet.getWords())

sentLst.printSentences()
#writing to a file 
fileW = open("m2file.txt","w")
fileW.write(sentLst.outStr)
fileW.close()
