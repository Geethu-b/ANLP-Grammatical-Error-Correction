from treetagger import TreeTagger
tt = TreeTagger(language='english')
outLst = tt.tag('Keeping the Secret of Genetic Testing')
wordLst =[]
tagLst  =[]
tagChangeDic ={'NP':'NNP','NPS':'NNPS','PP':'PRP','SENT':'.','(':'-LRB-', ')':'-RRB-'}
for word,tag,form in outLst:
    wordLst.append(word)	
    #print(tagChangeDic.keys())
    if tag in tagChangeDic.keys():
 	#print("hi")
        tagLst.append(tagChangeDic.get(tag))
    else:
        tagLst.append(tag)

print(wordLst)
print(tagLst)



