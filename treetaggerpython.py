from treetagger import TreeTagger
import sentence as sent        
tt = TreeTagger(language='english')

#reading from the file
#function for generation of list of words
# sentLst = sent.Sentences()

#file of the test data
fileTest  = open("testdata1.con","r").read()
#listing the values according to the sentences
lTest  = fileTest.split('\n\n')

#manually adding some 23
lTest.insert(23,"1	4	2	31	''	''	-	-	*))")


#for i in range(0,len(lTest)):
for i in range(0,1):
    
    lines = lTest[i].split('\n')
    sentDet = sent.SentenceDetails()   
    #Number of lines to go
    targetLines = len(lines)

    if i == 22:
        targetLines = len(lines)-1
    #getting the words 
    for j in range(0,targetLines):
        #seperate by tab        
        if len(lines[j])>0:
            # print(len(lines[j]))
            elements = lines[j].split('\t')
            #print(elements[3],elements[4],elements[5],elements[8])
            sentDet.addItems(elements[3],elements[4],elements[5],elements[8])


       
    #adding in the sentences 
                 
    print(sentDet.words)
    print(sentDet.synt)
    testSentence = " ".join(sentDet.words)
    print(testSentence)

    outLst = tt.tag(testSentence)
    wordLst =[]
    tagLst  =[]
    tagChangeDic ={'NP':'NNP','NPS':'NNPS','PP':'PRP','SENT':'.','(':'-LRB-', ')':'-RRB-'}

    for word,tag,form in outLst:
        wordLst.append(word)
        if tag in tagChangeDic.keys():
            tagLst.append(tagChangeDic.get(tag))
        else:
            tagLst.append(tag)
    print(wordLst)
    print(tagLst)