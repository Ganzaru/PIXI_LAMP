import numpy as np
import operator
from skimage.measure import label, regionprops
import cv2

class Contar:
	def __init__(self):

		self.rquadrats = [] 
		self.rcercles = []
		self.gquadrats = [] 
		self.gcercles = []
		self.bquadrats = []
		self.bcercles = []
		self.yquadrats = []
		self.ycercles = []
		self.pquadrats = []
		self.pcercles = []
		self.rrombo = []
		self.grombo = []
		self.brombo = []
		self.yrombo = []
		self.prombo = []


	def getKey(self, custom):
	    return custom.area

	def contar(self, hsv):

		# lower mask (0-10)
		lower_red = np.array([0,50,50])
		upper_red = np.array([20,255,255])
		mask0 = cv2.inRange(hsv, lower_red, upper_red)

		# upper mask (170-180)
		lower_red = np.array([160,50,50])
		upper_red = np.array([180,255,255])
		mask1 = cv2.inRange(hsv, lower_red, upper_red)

		# join my masks
		red=mask0 + mask1


		green = np.uint8([[[0,255,0]]])
		hsv_green = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)
		#print hsv_green
		lower_green = np.array([hsv_green[0][0][0]-20,100,100])
		upper_green = np.array([hsv_green[0][0][0]+30,255,255])


		blue = np.uint8([[[255,0,0]]])
		hsv_blue = cv2.cvtColor(blue,cv2.COLOR_BGR2HSV)
		#print hsv_blue
		lower_blue = np.array([hsv_blue[0][0][0]-20,100,100])
		upper_blue = np.array([hsv_blue[0][0][0]+20,255,255])

		yellow = np.uint8([[[0,255,255l]]])
		hsv_yellow = cv2.cvtColor(yellow,cv2.COLOR_BGR2HSV)
		lower_yellow = np.array([hsv_yellow[0][0][0]-10,100,100])
		upper_yellow = np.array([hsv_yellow[0][0][0]+10,255,255])
		#print hsv_yellow

		pink = np.uint8([[[255,0,255 ]]])
		hsv_pink = cv2.cvtColor(pink,cv2.COLOR_BGR2HSV)
		lower_pink = np.array([hsv_pink[0][0][0]-10,100,100])
		upper_pink = np.array([hsv_pink[0][0][0]+10,255,255])
		#print hsv_pink

		blue = cv2.inRange(hsv, lower_blue, upper_blue)
		green = cv2.inRange(hsv, lower_green, upper_green)
		red = cv2.inRange(hsv, lower_red, upper_red)
		yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)  
		pink = cv2.inRange(hsv, lower_pink, upper_pink)  

		kernelopen = np.ones((2,2),np.uint8)
		kernelclose = np.ones((5,5),np.uint8)

		red = cv2.morphologyEx(cv2.morphologyEx(red, cv2.MORPH_OPEN, kernelopen), cv2.MORPH_CLOSE, kernelclose)
		green = cv2.morphologyEx(cv2.morphologyEx(green, cv2.MORPH_OPEN, kernelopen), cv2.MORPH_CLOSE, kernelclose)
		blue = cv2.morphologyEx(cv2.morphologyEx(blue, cv2.MORPH_OPEN, kernelopen), cv2.MORPH_CLOSE, kernelclose)
		yellow = cv2.morphologyEx(cv2.morphologyEx(yellow, cv2.MORPH_OPEN, kernelopen), cv2.MORPH_CLOSE, kernelclose)
		pink = cv2.morphologyEx(cv2.morphologyEx(pink, cv2.MORPH_OPEN, kernelopen), cv2.MORPH_CLOSE, kernelclose)

		rgb=cv2.cvtColor(hsv,cv2.COLOR_HSV2RGB)		
		#cv2.imshow('rgb',rgb)
		#cv2.waitKey(0)
		#cv2.destroyAllWindows()
		
		#cv2.imshow('red',red)
		#cv2.waitKey(0)
		#cv2.destroyAllWindows()
		#cv2.imshow('green',green)
		#cv2.waitKey(0)
		#cv2.destroyAllWindows()
		#cv2.imshow('blue',blue)
		#cv2.waitKey(0)
		#cv2.destroyAllWindows()
		#cv2.imshow('yellow',yellow)
		#cv2.waitKey(0)
		#cv2.destroyAllWindows()
		#cv2.imshow('pink',pink)
		#cv2.waitKey(0)
		#cv2.destroyAllWindows()
		########################## LABELS ############################
		r_labels = label(red)                                   ###### RED LABEL
		rrps = regionprops(r_labels)
		#print "rojos", len(rrps)
		if len(rrps)>0:
			#print "rojoooooooo"
			maxi = max(rrps, key=operator.attrgetter('area'))#.area

		g_labels = label(green)                                 ###### GREEN LABEL
		grps = regionprops(g_labels)
		if len(grps)>0:
			maxi = max(grps, key=operator.attrgetter('area'))#.area

		b_labels = label(blue)                                  ###### BLUE LABEL
		brps = regionprops(b_labels)
		#print "azules", len(brps)
		if len(brps)>0:
			#print "azuuuuuuuuuuul"
			maxi = max(brps, key=operator.attrgetter('area'))#.area

		y_labels = label(yellow)                                  ###### YELLOW LABEL
		yrps = regionprops(y_labels)
		if len(yrps)>0:
		    maxi = max(yrps, key=operator.attrgetter('area'))#.area

		p_labels = label(pink)                                  ###### PINK LABEL
		prps = regionprops(p_labels)
		if len(prps)>0:
		    maxi = max(prps, key=operator.attrgetter('area'))#.area

		################### ORDENAR OBJECTES PER AREA #####################
		rarea = sorted(rrps, key=self.getKey, reverse=True)
		rarea = rarea[0:3]

		garea = sorted(grps, key=self.getKey, reverse=True)
		garea = garea[0:3]

		barea = sorted(brps, key=self.getKey, reverse=True)
		barea = barea[0:3]

		yarea = sorted(yrps, key=self.getKey, reverse=True)
		yarea = yarea[0:3]

		parea = sorted(prps, key=self.getKey, reverse=True)
		parea = parea[0:3]

		for obj in rarea:

			cercle=False
    			
			center = obj.centroid
		        aux=[obj.major_axis_length, obj.minor_axis_length]
		        diameter = np.mean(aux)
		        radii = diameter/2
		        area = obj.area
		        areacirculo = 3.1416*(radii**2)
		        rel=area/areacirculo
		        rel2 = ((obj.perimeter**2)/(4*3.1416*obj.area))
		       # print "red rel", rel2
		        if (rel2 > 1.1 and rel2 < 3 and obj.area>2000):
				#print "se ha metido un circulo rojo"
		            	self.rcercles.append(obj)
				cercle=True
	
		        #print obj.area
		        #print "red rect", (16*obj.area/obj.perimeter**2)
		        if ((16*obj.area/obj.perimeter**2)>0.96 and (16*obj.area/obj.perimeter**2)<1.05 and obj.area>20000 and cercle==False):
		            	self.rquadrats.append(obj)
				cercle=False
		            

		            
		        arearombo = (obj.area/obj.perimeter/2)/2
		#        print obj.area
		#        print area/arearombo

		for obj in garea:
			cercle=False
    			
			center = obj.centroid
		        aux=[obj.major_axis_length, obj.minor_axis_length]
		        diameter = np.mean(aux)
		        radii = diameter/2
		        area = obj.area
		        areacirculo = 3.1416*(radii**2)
		        rel=area/areacirculo
		        rel2 = ((obj.perimeter**2)/(4*3.1416*obj.area))
		        #print rel2
		        if (rel2 > 1.1 and rel2 < 3 and obj.area>2000):
				self.gcercles.append(obj)
				cercle=True
	
		        #print obj.area
		        #print (16*obj.area/obj.perimeter**2)
		        if ((16*obj.area/obj.perimeter**2)>0.96 and (16*obj.area/obj.perimeter**2)<1.05 and obj.area>20000 and cercle==False):
		          	self.gquadrats.append(obj)
				cercle=False

		for obj in barea:
			cercle=False
    			
			center = obj.centroid
		        aux=[obj.major_axis_length, obj.minor_axis_length]
		        diameter = np.mean(aux)
		        radii = diameter/2
		        area = obj.area
		        areacirculo = 3.1416*(radii**2)
		        rel=area/areacirculo
		        rel2 = ((obj.perimeter**2)/(4*3.1416*obj.area))
		        #print "blue rel", rel2
			#print "azul area" , obj.area
		        if (rel2 > 1.1 and rel2 < 3 and obj.area>2000):
				#print "se ha metido un circulo azul"
		            	self.bcercles.append(obj)
				cercle=True
	
		        #print obj.area
		        print "blue rect", (16*obj.area/obj.perimeter**2)
		        if ((16*obj.area/obj.perimeter**2)>0.96 and (16*obj.area/obj.perimeter**2)<1.05 and obj.area>20000 and cercle==False):
		           	self.bquadrats.append(obj)
				cercle=False
		            
		for obj in yarea:
			cercle=False
    			
			center = obj.centroid
		        aux=[obj.major_axis_length, obj.minor_axis_length]
		        diameter = np.mean(aux)
		        radii = diameter/2
		        area = obj.area
		        areacirculo = 3.1416*(radii**2)
		        rel=area/areacirculo
		        rel2 = ((obj.perimeter**2)/(4*3.1416*obj.area))
		        #print rel2
		        if (rel2 > 1.1 and rel2 < 3 and obj.area>2000):
		         	self.ycercles.append(obj)
				cercle=True
	
		        #print obj.area
		        #print (16*obj.area/obj.perimeter**2)
		        if ((16*obj.area/obj.perimeter**2)>0.96 and (16*obj.area/obj.perimeter**2)<1.05 and obj.area>20000 and cercle==False):
		            	self.yquadrats.append(obj)
				cercle=False
		            
		for obj in parea:
			cercle=False
    			
			center = obj.centroid
		        aux=[obj.major_axis_length, obj.minor_axis_length]
		        diameter = np.mean(aux)
		        radii = diameter/2
		        area = obj.area
		        areacirculo = 3.1416*(radii**2)
		        rel=area/areacirculo
		        rel2 = ((obj.perimeter**2)/(4*3.1416*obj.area))
		        #print rel2
		        if (rel2 > 1.1 and rel2 < 3 and obj.area>2000):
		            	self.pcercles.append(obj)	
				cercle=True
	
		        #print obj.area
		        #print (16*obj.area/obj.perimeter**2)
		        if ((16*obj.area/obj.perimeter**2)>0.96 and (16*obj.area/obj.perimeter**2)<1.05 and obj.area>20000 and cercle==False):
		           	self.pquadrats.append(obj)
				cercle=False
		    
		quadrats = [self.rquadrats,self.gquadrats,self.bquadrats,self.yquadrats,self.pquadrats]
		cercles = [self.rcercles,self.gcercles,self.bcercles,self.ycercles,self.pcercles]
		resultat = []

		n=0

		for q in quadrats:
		    if len(q)>0:
		        n=0
		        for qd in q:
		            n=n+1
		        print 'Hi ha ', n ,' quadrats'
		        resultat.append(n)
		    else:
		        print 'No ni ha quadrats'
		        resultat.append(0)
		        n=0

		for c in cercles:
		    if len(c)>0:
		        n=0
		        for cd in c:
		            n=n+1
		        print 'Hi ha ', n ,' cercles'
		        resultat.append(n)
		    else:
		        print 'No ni ha cercles'
		        resultat.append(0)
		            
		print resultat
		return resultat
