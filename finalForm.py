import glob,os,csv,math
from collections import namedtuple

def dictionaryOfCentres(centresPath):
	centrDirs=glob.glob(centresPath) # list of centre csv files

	centre = namedtuple('centre', 'X, Y, Major, Minor, Angle') 

	centresDict={}

	for x in centrDirs:
		# generate name of centre using filename
		head, tail = os.path.split(x)
		tail=tail[7:-4]
		tail=tail.translate(None, '_') # label in signals is 4950 and name of centre file is 40_50

		# make dictionary
		with open(x) as csvfile:
			readCSV = csv.reader(csvfile, delimiter=',')
			next(readCSV)

			for row in readCSV:
				centresDict[tail] = centre(X=float(row[0]), Y=float(row[1]), Major=float(row[2]), Minor=float(row[3]), Angle=float(row[4])*math.pi/180)

	return centresDict
'''
a=dictionaryOfCentres()
for x in a:
	print (x, a[x])
'''

def listOfSignals(signalsPath):
	a=glob.glob(signalsPath)
	signalsPath=a[0]

	signal = namedtuple('signal', 'X, Y, Label')
	ss=map(signal._make, csv.reader(open(signalsPath, "rb")))
	return ss
'''
a= listOfSignals()
for x in a:
	print x
'''

# compute radius of ellipse on theta angle
def ellipseRadiusOnTheta(minor, major, theta):
	return minor*major/math.sqrt(major**2 * math.sin(theta)**2 + minor**2 * math.cos(theta)**2)

# get distance between tho points
def getPointRadius(Xc, Yc, Xp, Yp):
	return math.sqrt((Yc-Yp)**2 + (Xc-Xp)**2)

# get angle in radians between two points relative to X axis
def getPointTheta(Xc, Yc, Xp, Yp):
	if (Xc-Xp)==0: #tan on 1.5708 radians (90 degrees) is undefined
		return 1.5708
	else:
		return math.atan((Yc-Yp)/(Xc-Xp))

# generate list of n zeros
def zeroListMaker(n):
	listofzeros = [0] * n
	return listofzeros

# given point Ds distance from centre and with As angle relative to major axis
# return order of layer, where this point was found
def findLayer(Ds, As, Majc, Minc, Angc, n):
	#print  Ds, As, Majc, Minc, Angc, n
	mi=Minc/math.sqrt(n)
	ma=Majc/math.sqrt(n)
	an=As+Angc
	#print  Ds, As, Majc, Minc, Angc, n, mi, ma, an
	for i in xrange(1,n+1):
		#print(Ds,ellipseRadiusOnTheta(mi*math.sqrt(i), ma*math.sqrt(i), an), i, Majc, Minc)
		if(ellipseRadiusOnTheta(mi*math.sqrt(i), ma*math.sqrt(i), an)>=Ds):
			return i-1
	return n

# find cyclic layer
def findLayerCy(Ds, R, n):
	r=R/n
	for x in xrange(1,n+1):
		if(x*r>=Ds):
			return x-1
	return n

def mainLoop(cens, sigs, n, exp):
	ans={}
	for i in cens:
		Labc=i # label of ellipse
		Xc=cens[Labc].X # x coordinate of ellipse centre
		Yc=cens[Labc].Y # y coordinate of ellipse centre
		Majc=cens[Labc].Major/2 # major of ellipse
		Minc=cens[Labc].Minor/2 # minor of ellipse
		#print Majc, Minc, Labc
		Angc=cens[Labc].Angle # angle of major relative to x axis
		ls=zeroListMaker(n+1)

		for x in sigs:
			if(x.Label==Labc):
				Xs=float(x.X) # x coordinate of signal
				Ys=float(x.Y) # y coordinate of signal
				Ds=getPointRadius(Xc, Yc, Xs, Ys) # distance from signal to ellipse centre
				As=getPointTheta(Xc, Yc, Xs, Ys) # angle between centre and signal relative to x axis
				if(exp==0):
					#print findLayer(Ds, As, Majc, Minc, Angc, n), Ds, As, Majc, Minc, Angc, n
					ls[findLayer(Ds, As, Majc, Minc, Angc, n)]+=1
				elif(exp==1):
					Rs=ellipseRadiusOnTheta(Minc, Majc, As + Angc) # radius of ellipse on As angle
					percent=Ds/Rs # distance to signal divided by full radius
					x=int(percent*n)
					if(x<n):
						ls[x]+=1
					else:
						ls[n]+=1
				else:
					ls[findLayerCy(Ds, Majc, n)]+=1
		ans[Labc]=ls
	return ans

# from {x:[x[0],x[1]...] ...} get {x:x[i] ...}
def dictOfIth(dict, i):
	di={}
	for x in dict:
		di[x]=dict[x][i]
	return di

# from {x:[x[0],x[1]...] ...} get {x:x[i]/sum(x:[...]) ...}
def dictOfIthProbab(dict, i, total):
	di={}
	for x in dict:
		if(total[x]>0):
			di[x]=round(float(dict[x][i])/total[x],4)
		else:
			di[x]=0
	return di

# export dictionary of answers as csv files
def exportAsCsv(dict,n,path,experiment):
	hh, tt = os.path.split(path)

	# export count results
	completeName = os.path.join(path, 'sgnal_distriubution_count_'+tt+str(experiment)+'.csv')
	with open(completeName, 'w') as csvfile:
		fieldnames=[]
		total={}
		for x in dict:
			fieldnames.append(x)
			sum=0
			for i in dict[x]:
				sum+=i
			total[x]=sum

		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()

		writer.writerow(total)

		for x in xrange(n+1):
			writer.writerow(dictOfIth(dict,x))

	# export probabilistic results
	completeName = os.path.join(path, 'sgnal_distriubution_probabilistic_'+tt+str(experiment)+'.csv')
	with open(completeName, 'w') as csvfile:
		fieldnames=[]
		total={}
		for x in dict:
			fieldnames.append(x)
			sum=0
			for i in dict[x]:
				sum+=i
			total[x]=sum

		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()

		writer.writerow(total)

		for x in xrange(n+1):
			writer.writerow(dictOfIthProbab(dict,x,total))


# sets paths for centre files, signals.csv and sets number of layers
# then run script and compute answer and export as csv
def main():
	path='/home/kdufla/Downloads/drive-download-20170710T160942Z-001'
	n=5
	
	cens=dictionaryOfCentres(path+'/Centre*.csv')
	sigs=listOfSignals(path+'/signals_labels*.csv')

	# x 0 = ellipse layers with same area
	# x 1 = ellipse layers with same change in radius (distance/total distance)
	# x 2 = cycle layers with same change in radius
	for x in xrange(3):
		exportAsCsv(mainLoop(cens, sigs, n,x),n,path,x)


if __name__ == '__main__':
	main()
