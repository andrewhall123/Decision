from math import log

def divideset(rows,column,value):
	split_function=None
	if isinstance(value,int) or isinstance(value,float):
		split_function=lambda row: row[column]>=value
	else:
		split_function=lambda row:row[column]==value
	set1=[row for row in rows if split_function(row)]
	set2=[row for row in rows if not split_function(row)]
	
	return (set1,set2)

def uniquecounts(rows):
	results={}
	for row in rows:
		r=row[len(row)-1]
		print("This is r:",r,"\n\n\n")
		if r not in results: results[r]=0
		results[r]+=1
	return results


def entropy(rows):
	log2=lambda x:log(x)/log(2)
	results=uniquecounts(rows)
	ent=0.0
	for r in results.keys():
		p=float(results[r])/len(rows)
		ent=ent-p*log2(p)
	return ent
	
class DecisionNode:
	def __init__(self,col=-1,value=None,results=None,tb=None,fb=None):
		self.col=col
		self.value=value
		self.results=results
		self.tb=tb
		self.fb=fb
		
def buildtree(rows, scoref=entropy):
	if len(rows)==0: 		
		return DecisionNode()


	current_score=scoref(rows)

	best_gain=0.0
	best_criteria=None
	best_sets=None
	column_count=len(rows[0])-1
	
	for col in range(0,column_count):
		column_values={}
		for row in rows:
			#print(row,col)
			column_values[row[col]]=1
		for value in column_values.keys():
			(set1,set2)=divideset(rows,col,value)
			print("\n\n\n",set1,set2,"\n\n\n\n")
			p=float(len(set1)/len(rows))
			gain=current_score-p*scoref(set1)-(1-p)*scoref(set2)
			if gain>best_gain and len(set1)>0 and len(set2)>0:
				best_gain=gain
				best_criteria=(col,value)
				best_sets=(set1,set2)		
	if best_gain>0:
		print("gaiiiiiiiiiiiiiiiiiii  n   "  ,best_gain)
		truebranch=buildtree(best_sets[0])
		falsebranch=buildtree(best_sets[1])
		return DecisionNode(col=best_criteria[0],value=best_criteria[1],tb=truebranch,fb=falsebranch)
		
	else:
		return DecisionNode(results=uniquecounts(rows))


def printTree(tree,indent=''):
	if tree.results!=None:
		print(str(tree.results))
	else:
		print(str(tree.col)+':', str(tree.value)+'? ')
		print(indent+'T->',end=" ")
		printTree(tree.tb,indent+' ')
		print(indent+'F->',end=" ")
		printTree(tree.fb,indent+' ')


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


def classify(observation,tree):
	print("\n")
	if tree.results!=None:
		print("res",tree.results)
		return tree.results
	else:
		v=observation[tree.col]
		branch=None
		print(v," ",tree.col)
		if isinstance(v,int) or isinstance(v,float):
			if v>=tree.value:
				branch=tree.tb
			else:
				branch=tree.fb
		else:
			if v==tree.value:
				branch=tree.tb
			else:
				branch=tree.fb
		return classify(observation,branch)


my_data=[['slashdot','USA','yes',18,'None'],
        ['google','France','yes',23,'Premium'],
        ['digg','USA','yes',24,'Basic'],
        ['kiwitobes','France','yes',23,'Basic'],
        ['google','UK','no',21,'Premium'],
        ['(direct)','New Zealand','no',12,'None'],
        ['(direct)','UK','no',21,'Basic'],
        ['google','USA','no',24,'Premium'],
        ['slashdot','France','yes',19,'None'],
        ['digg','USA','no',18,'None'],
        ['google','UK','no',18,'None'],
        ['kiwitobes','UK','no',19,'None'],
        ['digg','New Zealand','yes',12,'Basic'],
        ['slashdot','UK','no',21,'None'],
        ['google','UK','yes',18,'Basic'],
        ['kiwitobes','France','yes',19,'Basic']]

tree=buildtree(my_data)
printTree(tree)
print("\n\n",classify(['(direct)','USA','yes',5],tree))
print(type(tree.tb))
