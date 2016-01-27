import random
#import PIL
from matplotlib import pyplot as plt
from math import factorial as fact

l = 16
h = 16
m = 40
t = [[]]
tp= [[]]
colores=['blue','green','red','darkblue','brown','cyan','black','grey']

def generar(l,h,m):
	t = [[-1]*l for i in range(h)]
	x = [i for i in range(l*h)]
	random.shuffle(x)
	for i in range(m):
		t[x[i]/l][x[i]%l]=-2
	return t

def importar(arch):
	t=[]
	f = open(arch)
	for line in f:
		t.append([])
		for s in line.split():
			if   s == "O":t[-1].append(-1)
			elif s == "X":t[-1].append(-2)
			else :    t[-1].append(int(s))
	return (t,len(t),len(t[0]))

def printear(out):
	for i in put:
		for j in i:
			if type(j)==float:	print("%.2f" % j),
			elif j==-2 or j==-1: 	print "    ",
			else:			print j,"  ",
			print "|",
		print ""

def adyacentes(a):
	(f,c) = a
	res = []
	for i in range(max(0,f-1),min(h,f+2)):
		for j in range(max(0,c-1),min(l,c+2)):
			if (i,j) <> (f,c): res.append((i,j))
	return res

def abrir(f,c):
	if min([t[i][j]<0 for i in range(h) for j in range(l)])==1 and t[f][c]==-2: 
		for a in adyacentes((f,c)):
			if t[a[0]][a[1]]==-1: 
				t[a[0]][a[1]]=-2
				t[f][c]=-1
				return 0
	if t[f][c]==-2:
		t[f][c]='X'
		return 1
	else:
		mi = sum([t[i][j]==-2 for i in range(max(0,f-1),min(h,f+2)) for j in range(max(0,c-1),min(l,c+2))])
		t[f][c]=mi
		if mi == 0:
			for (i,j) in adyacentes((f,c)):
				if t[i][j]==-1:abrir(i,j)
	return 0

def esabierto(f,c):
	for (i,j) in adyacentes((f,c)):
		if t[i][j] >= 0: return True
	return False

def abiertos():
	res = []
	for f in range(len(t)):
		for c in range(len(t[f])):
			if t[f][c]<0:
				if esabierto(f,c): res.append((f,c))
	return res
				

def sedebeagregar(a,i,r):
	c = a[i]
	#no agregarlo rompe alguno de los numeros
	for (i2, j) in adyacentes(c):
		if t[i2][j] >= 0:
			#los lugares donde asumi que hay mina + los adyacentes que esten en a[i:]
			ab = len([1 for x in adyacentes((i2,j)) if x in a[i+1:] or x in r])
			if ab < t[i2][j]: return True

	#no agregarlo hace que la cantidad total de minas sea menor a la deseada
	ab = len([1 for x in range(h) for y in range(l) if ((x,y) not in a and t[x][y] < 0) or (x,y) in a[i+1:] or (x,y) in r])
	if ab<m:return True
	return False

def sepuedeagregar(c,r):
	#agregarlo no rompe ninguno de los numeros
	for (i, j) in adyacentes(c):
		if t[i][j] >= 0:
			mi = len([1 for x in adyacentes((i,j)) if x in r or x == c])
			if t[i][j] < mi: return False
	#agregarlo no hace que la cantidad total de minas sea mayor a la deseada
	if len(r) >= m : return False
	return True
	

def generarcomb(a,i,res):
	res2=[]
	res3=[]
	for r in res:
		if sedebeagregar(a,i,r):
			if sepuedeagregar(a[i],r): r.append(a[i])
			else: res3.append(r)
		elif sepuedeagregar(a[i],r):
			r2 = []
			r2[:] = r
			r2.append(a[i])
			res2.append(r2)
			if (len(res)+len(res2))>1999 and (len(res)+len(res2))%2000==0:
				N=raw_input("N para no seguir buscando ")
				if N == 'N': return -1
	res.extend(res2)
	for i in res3: res.remove(i)
	

def combinat(a,b):
	if a>=b and b>=0: 
		return float(fact(a)/fact(b)/fact(a-b))	
	else: return 0.0

def calcularProbs():
	a = abiertos()
	c=[[]]
	for i in range(len(a)):
		N=generarcomb(a,i,c)
		if N ==-1 : break
	p = [0]*(m+1)
	for i in c: 
		p[len(i)]+=1
	
	cerrados = [(x, y) for x in range(h) for y in range(l) if ((x,y) not in a and t[x][y] < 0)]

	#la probabilidad de cada combinacion es un escalamiento de las probabilidades dadas por la cantidad de minas que tiene
	p2=[0]*(m+1)
	for i in range(len(p)):
		p2[i] = (combinat(len(a),i)/combinat(len(a)+len(cerrados),m)*combinat(len(cerrados),m-i)) if p[i]>0 else 0.0

	s = float(sum(p2))
	p2 = [i/s for i in p2]
	
	#la probabilidad de cada casilla es la suma de las combinaciones en las que esta
	res = [[0]*l for i in range(h)]
	for i in a:
		res[i[0]][i[1]]= float(sum([p2[len(j)]/p[len(j)] for j in c if i in j]))

	#la probabilidad de las que no estan en a es la densidad de minas esperada
	esp = sum([p2[j]*j for j in range(len(p))])
	for i in cerrados:
		res[i[0]][i[1]]= (m-esp)/len(cerrados)
	return res

def rgb(el):
	if 1-el < 0.5:
		a=0xff
		b=int((1-el)*512)

	else:
		a=int(el*511)
		b=0xff

	a=(('0' if a<16 else '') +hex(a)[2:])
	b=(('0' if b<16 else '') +hex(b)[2:])

	return "#"+a+b+'00'

def mostrar(t,tp,exito):
#	plt.axes()
	for i in range(len(t)):
		for j in range(len(t[i])):
			el = t[i][j]
			if el < 0:
				rectangle = plt.Rectangle((j-.5, i-.5), 1, 1, fc=rgb(tp[i][j]))
#				plt.text(j+0.5, i+0.5, str("%.2f" % tp[i][j]),verticalalignment='center', horizontalalignment='center')
			if el == -2 and exito == 1:
				plt.gca().add_patch(rectangle)
				rectangle = plt.Rectangle((j-.25, i-.25), .5, .5, fc='red')
			if el == 'X':
				rectangle = plt.Rectangle((j-.5, i-.5), 1, 1, fc='red')
			elif el >=0:
				rectangle = plt.Rectangle((j-.5, i-.5), 1, 1, fc='gray')
				if el>0:plt.text(j, i, str(el),verticalalignment='center', horizontalalignment='center', color=colores[el-1],fontweight='bold')#fontsize

			plt.gca().add_patch(rectangle)

	plt.axis('scaled')
	plt.xlim(-.5,l-.5)
	plt.ylim(-.5,h-.5)
	plt.gca().invert_yaxis()
	plt.savefig("Tablero.png")
	plt.clf()

def is_int(i):
	try:
		int(i)
		return True
	except ValueError: return False

def pedirno(s,mn,mx):
	res = raw_input(s)
	while not is_int(res) or int(res)>mx or int(res)<mn:
		print "Error"
		res = raw_input(s)
	return int(res)

#(t,h,l)=importar("blabl2")

h = pedirno("Filas:    ",1,1000)
l = pedirno("Columnas: ",1,1000/float(h))
m = pedirno("Minas:    ",1,h*l-1)

t = generar(l,h,m)
tp = [[0]*l for i in range(h)]
exito=0
while (1):
	mostrar(t,tp,exito)
	if max([t[i][j]==-1 for i in range(h) for j in range(l)])==0 or exito == 1: break
	a1 = pedirno("Fila:    ",0,h-1)
	a2 = pedirno("Columna: ",0,l-1)
	if t[a1][a2]<0:
		exito = abrir(a1,a2)
	else:
		for (a3, a4) in adyacentes((a1,a2)):
			if tp[a3][a4]==0:
				exito = abrir(a3, a4) or exito
	if exito==0: tp = calcularProbs()
