import sentence as sent

        
#function for generation of list of words
sentLst = sent.Sentences()

#file of the test data
fileTest  = open("testdata1.con","r").read()
#listing the values according to the sentences
lTest  = fileTest.split('\n\n')



#for i in range(0,len(lTest)):
for i in range(0,4):
    
    lines = lTest[i].split('\n')
    sentDet = sent.SentenceDetails()    
    #getting the words 
    for j in range(0,len(lines)):
        #seperate by tab        
        if len(lines[j])>0:
            elements = lines[j].split('\t')
            #print(elements[3],elements[4],elements[5],elements[8])
            sentDet.addItems(elements[3],elements[4],elements[5],elements[8])
    
       
    #adding in the sentences                
    print(sentDet.words)
    sentDet.listProblems()
    sentDet.solveProblem()
    sentDet.getSolutionInSentence()

    sentLst.addSentence(sentDet.getWords())

sentLst.printSentences()
#writing to a file 
fileW = open("m2file.txt","w")
fileW.write(sentLst.outStr)
fileW.close()