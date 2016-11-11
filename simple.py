from math import log

def format(read_data,rows):
	data=[[]]*rows
	word=""
	wordlist=[]
	index=0
	for i in read_data:
		if i != ',':
			word=word+i
		if i==',':
			wordlist.append(word)
			word=""
		if i=="\n":
			wordlist.append(word.replace('\n',''))
			data[index]=wordlist
			wordlist=[]
			index=index+1
			word=""
	return data

def getLen(data):
	rows=0
	for i in read_data:
		if i=='\n':
			rows+=1
	return rows

def get_data(fileName):
	with open(fileName,'r') as f:
		next(f)
		read_data=f.read()
	
	return read_data

def divideset(data,col,val):
	
	split=lambda row: row[col]==val
	set1=[x for x in data if split(x)]
	set2=[x for x in data if not split(x)]

	return (set1,set2)
	
def uniquecounts(data):
	results={}
	
	for row in data:
		r=row[len(row)-1]
		if r not in results:
			results[r]=0
		results[r]+=1
	return results
	
def entropy(data):
	log2=lambda x:log(x)/log(2)
	results=uniquecounts(data)
	ent=0.0
	for r in results.keys():
		p=float(results[r]/len(data))
		ent=ent-p*log2(p)
	return ent

class DecisionNode:
	def __init__(self,col=-1,value=None,results=None,tb=None,fb=None):
		self.col=col
		self.value=value
		self.results=results
		self.tb=tb
		self.fb=fb
		
def buildTree(data,scoref=entropy):
	if len(data)==0:
		return DecisionNode()
	
	score=scoref(data)
	
	best_sets=None
	best_criteria=None
	best_gain=0.0
	
	column_count=len(data[0])-1
	
	for column in range(0,column_count):
		column_values={}
		for row in data:
			column_values[row[column]]=1
			for col in column_values.keys():
				(set1,set2)=divideset(data,column,col)
				p=float(len(set1))/len(data)
				
				gain=score-p*entropy(set1)-(1-p)*entropy(set2)
				if gain>best_gain and len(set1)>0 and len(set2)>0:
					best_gain=gain
					best_sets=(set1,set2)
					best_criteria=(column,col)
	if best_gain>0:
		#print(best_gain)
		true=buildTree(best_sets[0])
		false=buildTree(best_sets[1])
		return DecisionNode(col=best_criteria[0],value=best_criteria[1],tb=true,fb=false)
	else:
		return DecisionNode(results=uniquecounts(data))
	
def printTree(tree,indent=''):
	if tree.results!=None:
		print(str(tree.results))
	else:
		print(str(tree.col)+':', str(tree.value)+'? ')
		print(indent+'T->',end=" ")
		printTree(tree.tb,indent+' ')
		print(indent+'F->',end=" ")
		printTree(tree.fb,indent+' ')
		
def classify(observation,tree):
	if tree.results!=None:
		return tree.results
	else:
		branch=None
		v=observation[tree.col]
		if tree.value==v:
			branch=tree.tb
		else:
			branch=tree.fb
	return classify(observation,branch)
		

def getwidth(tree):
  if tree.tb==None and tree.fb==None: return 1
  return getwidth(tree.tb)+getwidth(tree.fb)

def getdepth(tree):
  if tree.tb==None and tree.fb==None: return 0
  return max(getdepth(tree.tb),getdepth(tree.fb))+1


from PIL import Image,ImageDraw

def drawtree(tree,jpeg='tree.jpg'):
  w=getwidth(tree)*100
  h=getdepth(tree)*100+120

  img=Image.new('RGB',(w,h),(255,255,255))
  draw=ImageDraw.Draw(img)

  drawnode(draw,tree,w/2,20)
  img.save(jpeg,'JPEG')
  
def drawnode(draw,tree,x,y):
  if tree.results==None:
    # Get the width of each branch
    w1=getwidth(tree.fb)*100
    w2=getwidth(tree.tb)*100

    # Determine the total space required by this node
    left=x-(w1+w2)/2
    right=x+(w1+w2)/2

    # Draw the condition string
    draw.text((x-20,y-10),str(tree.col)+':'+str(tree.value),(0,0,0))

    # Draw links to the branches
    draw.line((x,y,left+w1/2,y+100),fill=(255,0,0))
    draw.line((x,y,right-w2/2,y+100),fill=(255,0,0))
    
    # Draw the branch nodes
    drawnode(draw,tree.fb,left+w1/2,y+100)
    drawnode(draw,tree.tb,right-w2/2,y+100)
  else:
    txt=' \n'.join(['%s:%d'%v for v in tree.results.items()])
    draw.text((x-20,y),txt,(0,0,0))

read_data=get_data("golf.csv")
rows=getLen(read_data)
data=format(read_data,rows)

print(data,"\n\n",divideset(data,1,"cool"))
tree=buildTree(data)
		
printTree(tree)
print(tree.value)
obs=['sunny','cool','normal','FALSE','yes']
print(classify(obs,tree))
drawtree(tree)
