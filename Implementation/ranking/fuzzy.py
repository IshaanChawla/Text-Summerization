import numpy as np
import skfuzzy as fuzz
import random


def num_category(numerical,num_l,num_m,num_h,num_in):
	num_cat_l = fuzz.interp_membership(numerical,num_l,num_in) # Depends from Step 1
	num_cat_m = fuzz.interp_membership(numerical,num_m,num_in) # Depends from Step 1
	num_cat_h = fuzz.interp_membership(numerical,num_h,num_in) # Depends from Step 1
	return dict(num_low = num_cat_l , num_med = num_cat_m , num_high = num_cat_h)

def len_category(length,len_l,len_m,len_h,len_in):
	len_cat_l = fuzz.interp_membership(length,len_l,len_in) # Depends from Step 1
	len_cat_m = fuzz.interp_membership(length,len_m,len_in) # Depends from Step 1
	len_cat_h = fuzz.interp_membership(length,len_h,len_in) # Depends from Step 1
	return dict(len_low = len_cat_l , len_med = len_cat_m , len_high = len_cat_h)

def titl_category(title,titl_l,titl_m,titl_h,titl_in):
	titl_cat_l = fuzz.interp_membership(title,titl_l,titl_in) # Depends from Step 1
	titl_cat_m = fuzz.interp_membership(title,titl_m,titl_in) # Depends from Step 1
	titl_cat_h = fuzz.interp_membership(title,titl_h,titl_in) # Depends from Step 1
	return dict(titl_low = titl_cat_l , titl_med = titl_cat_m , titl_high = titl_cat_h)

def them_category(thematic,them_l,them_m,them_h,them_in):
	them_cat_l = fuzz.interp_membership(thematic,them_l,them_in) # Depends from Step 1
	them_cat_m = fuzz.interp_membership(thematic,them_m,them_in) # Depends from Step 1
	them_cat_h = fuzz.interp_membership(thematic,them_h,them_in) # Depends from Step 1
	return dict(them_low = them_cat_l , them_med = them_cat_m , them_high = them_cat_h)


def inference(matrix):
	numerical1 = matrix[0]
	length1 = matrix[1]
	title1 = matrix[2]
	thematic1 = matrix[3]
	
	numerical = np.arange(0,1.001,0.001)
	length = np.arange(0,1.001,0.001)
	title  = np.arange(0,1.001,0.001)
	thematic  = np.arange(0,1.001,0.001)
	
	sen = np.arange(0,1.001,0.001)

	num_l = fuzz.trimf(numerical, [0.0,0.054,0.076])
	num_m = fuzz.trimf(numerical, [0.076,0.293,0.466])
	num_h = fuzz.trimf(numerical, [0.466,0.576,1.001])
	
	len_l = fuzz.trimf(length, [0.0,0.022,0.057])
	len_m = fuzz.trimf(length, [0.057,0.332,0.484])
	len_h = fuzz.trimf(length, [0.484,0.582,1.001])

	titl_l = fuzz.trimf(title, [0.0,0.044,0.049])
	titl_m = fuzz.trimf(title, [0.049,0.376,0.438])
	titl_h = fuzz.trimf(title, [0.438,0.569,1.001])

	them_l = fuzz.trimf(thematic, [0.0,0.044,0.049])
	them_m = fuzz.trimf(thematic, [0.049,0.376,0.438])
	them_h = fuzz.trimf(thematic, [0.438,0.569,1.001])


	sen_unimp  = fuzz.trimf(sen, [0.0,0.022,0.056])
	sen_ave = fuzz.trimf(sen, [0.056,0.105,0.555])
	sen_imp = fuzz.trimf(sen, [0.555,0.888,1.001])
	result = []

	for i in range(len(numerical1)):
		k = numerical1[i]
		l = length1[i]
		m = title1[i]
		n = thematic1[i]
		s= False
		r= False
		t= False
		u = False
		if k == 0.0:
			r = True 
		if l == 0.0:
			s = True 
		if m == 0.0:
			t = True
		if n == 0.0:
			u = True
		
		if r & s & t & u:
			numerical1[i] = 0.001
			num_in = num_category(numerical,num_l,num_m,num_h,numerical1[i])
			len_in = len_category(length,len_l,len_m,len_h,length1[i])
			titl_in = titl_category(title,titl_l,titl_m,titl_h,title1[i])
			them_in = them_category(thematic,them_l,them_m,them_h,thematic1[i])
		else:
			num_in = num_category(numerical,num_l,num_m,num_h,numerical1[i])
			len_in = len_category(length,len_l,len_m,len_h,length1[i])
			titl_in = titl_category(title,titl_l,titl_m,titl_h,title1[i])
			them_in = them_category(thematic,them_l,them_m,them_h,thematic1[i])

		rule1 = max(them_in['them_high'],num_in['num_high'],len_in['len_high'],titl_in['titl_high'])
		rule2 = max(them_in['them_high'],num_in['num_high'],len_in['len_high'],titl_in['titl_med'])
		rule3 = max(them_in['them_high'],num_in['num_high'],len_in['len_high'],titl_in['titl_low'])

		rule4 = max(them_in['them_high'],num_in['num_high'],len_in['len_med'],titl_in['titl_high'])
		rule5 = max(them_in['them_high'],num_in['num_high'],len_in['len_med'],titl_in['titl_med'])
		rule6 = max(them_in['them_high'],num_in['num_high'],len_in['len_med'],titl_in['titl_low'])	

		rule7 = max(them_in['them_high'],num_in['num_high'],len_in['len_low'],titl_in['titl_high'])
		rule8 = max(them_in['them_high'],num_in['num_high'],len_in['len_low'],titl_in['titl_med'])
		rule9 = max(them_in['them_high'],num_in['num_high'],len_in['len_low'],titl_in['titl_low'])

		rule10 = max(them_in['them_high'],num_in['num_med'],len_in['len_high'],titl_in['titl_high'])
		rule11 = max(them_in['them_high'],num_in['num_med'],len_in['len_high'],titl_in['titl_med'])
		rule12 = max(them_in['them_high'],num_in['num_med'],len_in['len_high'],titl_in['titl_low'])

		rule13 = max(them_in['them_high'],num_in['num_med'],len_in['len_med'],titl_in['titl_high'])
		rule14 = max(them_in['them_high'],num_in['num_med'],len_in['len_med'],titl_in['titl_med'])
		rule15 = max(them_in['them_high'],num_in['num_med'],len_in['len_med'],titl_in['titl_low'])	

		rule16 = max(them_in['them_high'],num_in['num_med'],len_in['len_low'],titl_in['titl_high'])
		rule17 = max(them_in['them_high'],num_in['num_med'],len_in['len_low'],titl_in['titl_med'])
		rule18 = max(them_in['them_high'],num_in['num_med'],len_in['len_low'],titl_in['titl_low'])
						
		rule19 = max(them_in['them_high'],num_in['num_low'],len_in['len_high'],titl_in['titl_high'])
		rule20 = max(them_in['them_high'],num_in['num_low'],len_in['len_high'],titl_in['titl_med'])
		rule21 = max(them_in['them_high'],num_in['num_low'],len_in['len_high'],titl_in['titl_low'])			
		
		rule22 = max(them_in['them_high'],num_in['num_low'],len_in['len_med'],titl_in['titl_high'])
		rule23 = max(them_in['them_high'],num_in['num_low'],len_in['len_med'],titl_in['titl_med'])
		rule24 = max(them_in['them_high'],num_in['num_low'],len_in['len_med'],titl_in['titl_low'])	
		
		rule25 = max(them_in['them_high'],num_in['num_low'],len_in['len_low'],titl_in['titl_high'])
		rule26 = max(them_in['them_high'],num_in['num_low'],len_in['len_low'],titl_in['titl_med'])
		rule27 = max(them_in['them_high'],num_in['num_low'],len_in['len_low'],titl_in['titl_low'])

############################28-54################################################3

		rule28 = max(them_in['them_med'],num_in['num_high'],len_in['len_high'],titl_in['titl_high'])
		rule29 = max(them_in['them_med'],num_in['num_high'],len_in['len_high'],titl_in['titl_med'])
		rule30 = max(them_in['them_med'],num_in['num_high'],len_in['len_high'],titl_in['titl_low'])

		rule31 = max(them_in['them_med'],num_in['num_high'],len_in['len_med'],titl_in['titl_high'])
		rule32 = max(them_in['them_med'],num_in['num_high'],len_in['len_med'],titl_in['titl_med'])
		rule33 = max(them_in['them_med'],num_in['num_high'],len_in['len_med'],titl_in['titl_low'])	

		rule34 = max(them_in['them_med'],num_in['num_high'],len_in['len_low'],titl_in['titl_high'])
		rule35 = max(them_in['them_med'],num_in['num_high'],len_in['len_low'],titl_in['titl_med'])
		rule36 = max(them_in['them_med'],num_in['num_high'],len_in['len_low'],titl_in['titl_low'])

		rule37 = max(them_in['them_med'],num_in['num_med'],len_in['len_high'],titl_in['titl_high'])
		rule38 = max(them_in['them_med'],num_in['num_med'],len_in['len_high'],titl_in['titl_med'])
		rule39 = max(them_in['them_med'],num_in['num_med'],len_in['len_high'],titl_in['titl_low'])

		rule40 = max(them_in['them_med'],num_in['num_med'],len_in['len_med'],titl_in['titl_high'])
		rule41 = max(them_in['them_med'],num_in['num_med'],len_in['len_med'],titl_in['titl_med'])
		rule42 = max(them_in['them_med'],num_in['num_med'],len_in['len_med'],titl_in['titl_low'])	

		rule43 = max(them_in['them_med'],num_in['num_med'],len_in['len_low'],titl_in['titl_high'])
		rule44 = max(them_in['them_med'],num_in['num_med'],len_in['len_low'],titl_in['titl_med'])
		rule45 = max(them_in['them_med'],num_in['num_med'],len_in['len_low'],titl_in['titl_low'])
						
		rule46 = max(them_in['them_med'],num_in['num_low'],len_in['len_high'],titl_in['titl_high'])
		rule47 = max(them_in['them_med'],num_in['num_low'],len_in['len_high'],titl_in['titl_med'])
		rule48 = max(them_in['them_med'],num_in['num_low'],len_in['len_high'],titl_in['titl_low'])			
		
		rule49 = max(them_in['them_med'],num_in['num_low'],len_in['len_med'],titl_in['titl_high'])
		rule50 = max(them_in['them_med'],num_in['num_low'],len_in['len_med'],titl_in['titl_med'])
		rule51 = max(them_in['them_med'],num_in['num_low'],len_in['len_med'],titl_in['titl_low'])	
		
		rule52 = max(them_in['them_med'],num_in['num_low'],len_in['len_low'],titl_in['titl_high'])
		rule53 = max(them_in['them_med'],num_in['num_low'],len_in['len_low'],titl_in['titl_med'])
		rule54 = max(them_in['them_med'],num_in['num_low'],len_in['len_low'],titl_in['titl_low'])



		###########################55-81#################################

		rule55 = max(them_in['them_low'],num_in['num_high'],len_in['len_high'],titl_in['titl_high'])
		rule56 = max(them_in['them_low'],num_in['num_high'],len_in['len_high'],titl_in['titl_med'])
		rule57 = max(them_in['them_low'],num_in['num_high'],len_in['len_high'],titl_in['titl_low'])

		rule58 = max(them_in['them_low'],num_in['num_high'],len_in['len_med'],titl_in['titl_high'])
		rule59 = max(them_in['them_low'],num_in['num_high'],len_in['len_med'],titl_in['titl_med'])
		rule60 = max(them_in['them_low'],num_in['num_high'],len_in['len_med'],titl_in['titl_low'])	

		rule61 = max(them_in['them_low'],num_in['num_high'],len_in['len_low'],titl_in['titl_high'])
		rule62 = max(them_in['them_low'],num_in['num_high'],len_in['len_low'],titl_in['titl_med'])
		rule63 = max(them_in['them_low'],num_in['num_high'],len_in['len_low'],titl_in['titl_low'])

		rule64 = max(them_in['them_low'],num_in['num_med'],len_in['len_high'],titl_in['titl_high'])
		rule65 = max(them_in['them_low'],num_in['num_med'],len_in['len_high'],titl_in['titl_med'])
		rule66 = max(them_in['them_low'],num_in['num_med'],len_in['len_high'],titl_in['titl_low'])

		rule67 = max(them_in['them_low'],num_in['num_med'],len_in['len_med'],titl_in['titl_high'])
		rule68 = max(them_in['them_low'],num_in['num_med'],len_in['len_med'],titl_in['titl_med'])
		rule69 = max(them_in['them_low'],num_in['num_med'],len_in['len_med'],titl_in['titl_low'])	

		rule70 = max(them_in['them_low'],num_in['num_med'],len_in['len_low'],titl_in['titl_high'])
		rule71 = max(them_in['them_low'],num_in['num_med'],len_in['len_low'],titl_in['titl_med'])
		rule72 = max(them_in['them_low'],num_in['num_med'],len_in['len_low'],titl_in['titl_low'])
						
		rule73 = max(them_in['them_low'],num_in['num_low'],len_in['len_high'],titl_in['titl_high'])
		rule74 = max(them_in['them_low'],num_in['num_low'],len_in['len_high'],titl_in['titl_med'])
		rule75 = max(them_in['them_low'],num_in['num_low'],len_in['len_high'],titl_in['titl_low'])			
		
		rule76 = max(them_in['them_low'],num_in['num_low'],len_in['len_med'],titl_in['titl_high'])
		rule77 = max(them_in['them_low'],num_in['num_low'],len_in['len_med'],titl_in['titl_med'])
		rule78 = max(them_in['them_low'],num_in['num_low'],len_in['len_med'],titl_in['titl_low'])	
		
		rule79 = max(them_in['them_low'],num_in['num_low'],len_in['len_low'],titl_in['titl_high'])
		rule80 = max(them_in['them_low'],num_in['num_low'],len_in['len_low'],titl_in['titl_med'])
		rule81 = max(them_in['them_low'],num_in['num_low'],len_in['len_low'],titl_in['titl_low'])


		imp1 = np.fmin(rule1,sen_imp)
		imp2 = np.fmin(rule2,sen_unimp)
		imp3 = np.fmin(rule3,sen_unimp)
		
		imp4 = np.fmin(rule4,sen_imp)
		imp5 = np.fmin(rule5,sen_ave)
		imp6 = np.fmin(rule6,sen_ave)
		
		imp7 = np.fmin(rule7,sen_imp)
		imp8 = np.fmin(rule8,sen_imp)		
		imp9 = np.fmin(rule9,sen_ave)
		
		imp10 = np.fmin(rule10,sen_ave)
		imp11 = np.fmin(rule11,sen_unimp)
		imp12 = np.fmin(rule12,sen_unimp)
		
		imp13 = np.fmin(rule13,sen_ave)
		imp14 = np.fmin(rule14,sen_ave)
		imp15 = np.fmin(rule15,sen_unimp)
		
		imp16 = np.fmin(rule16,sen_imp)
		imp17 = np.fmin(rule17,sen_ave)
		imp18 = np.fmin(rule18,sen_unimp)
		
		imp19 = np.fmin(rule19,sen_ave)
		imp20 = np.fmin(rule20,sen_unimp)
		imp21 = np.fmin(rule21,sen_unimp)
		
		imp22 = np.fmin(rule22,sen_ave)
		imp23 = np.fmin(rule23,sen_ave)
		imp24 = np.fmin(rule24,sen_unimp)
		
		imp25 = np.fmin(rule25,sen_imp)
		imp26 = np.fmin(rule26,sen_ave)
		imp27 = np.fmin(rule27,sen_unimp)
		
		#######################28-54###################

		imp28 = np.fmin(rule28,sen_imp)
		imp29 = np.fmin(rule29,sen_unimp)
		imp30 = np.fmin(rule30,sen_unimp)
		
		imp31 = np.fmin(rule31,sen_imp)
		imp32 = np.fmin(rule32,sen_ave)
		imp33 = np.fmin(rule33,sen_unimp)
		
		imp34 = np.fmin(rule34,sen_imp)
		imp35 = np.fmin(rule35,sen_ave)		
		imp36 = np.fmin(rule36,sen_unimp)
		
		imp37= np.fmin(rule37,sen_ave)
		imp38 = np.fmin(rule38,sen_ave)
		imp39 = np.fmin(rule39,sen_unimp)
		
		imp40 = np.fmin(rule40,sen_imp)
		imp41 = np.fmin(rule41,sen_ave)
		imp42 = np.fmin(rule42,sen_ave)
		
		imp43 = np.fmin(rule43,sen_imp)
		imp44 = np.fmin(rule44,sen_ave)
		imp45 = np.fmin(rule45,sen_imp)
		
		imp46 = np.fmin(rule46,sen_ave)
		imp47 = np.fmin(rule47,sen_unimp)
		imp48 = np.fmin(rule48,sen_unimp)
		
		imp49 = np.fmin(rule49,sen_ave)
		imp50 = np.fmin(rule50,sen_ave)
		imp51 = np.fmin(rule51,sen_unimp)
		
		imp52 = np.fmin(rule52,sen_imp)
		imp53 = np.fmin(rule53,sen_ave)
		imp54 = np.fmin(rule54,sen_unimp)

		#########################55-81###################
		
		imp55 = np.fmin(rule55,sen_ave)
		imp56 = np.fmin(rule56,sen_ave)
		imp57 = np.fmin(rule57,sen_unimp)
		
		imp58 = np.fmin(rule58,sen_ave)
		imp59 = np.fmin(rule59,sen_ave)
		imp60 = np.fmin(rule60,sen_unimp)
		
		imp61 = np.fmin(rule61,sen_imp)
		imp62 = np.fmin(rule62,sen_ave)		
		imp63 = np.fmin(rule63,sen_unimp)
		
		imp64 = np.fmin(rule64,sen_ave)
		imp65 = np.fmin(rule65,sen_unimp)
		imp66 = np.fmin(rule66,sen_unimp)
		
		imp67 = np.fmin(rule67,sen_ave)
		imp68 = np.fmin(rule68,sen_unimp)
		imp69 = np.fmin(rule69,sen_unimp)
		
		imp70 = np.fmin(rule70,sen_ave)
		imp71 = np.fmin(rule71,sen_unimp)
		imp72 = np.fmin(rule72,sen_unimp)
		
		imp73 = np.fmin(rule73,sen_unimp)
		imp74 = np.fmin(rule74,sen_unimp)
		imp75 = np.fmin(rule75,sen_unimp)
		
		imp76 = np.fmin(rule76,sen_ave)
		imp77 = np.fmin(rule77,sen_unimp)
		imp78 = np.fmin(rule78,sen_unimp)
		
		imp79 = np.fmin(rule79,sen_ave)
		imp80 = np.fmin(rule80,sen_ave)
		imp81 = np.fmin(rule81,sen_unimp)

		d = imp1 + imp2 + imp3+ imp4+ imp5+ imp6+ imp7+ imp8+ imp9+ imp10+ imp11+ imp12+ imp13+ imp14+ imp15+ imp16+ imp17+ imp18+ imp19+ imp20+ imp21+ imp22+ imp23+ imp24+ imp25+ imp26 + imp27
		e = imp28 + imp29 + imp30+ imp31+ imp32+ imp33+ imp34+ imp35+ imp36+ imp37+ imp38+ imp39+ imp40+ imp41+ imp42+ imp43+ imp44+ imp45+ imp46+ imp47+ imp48+ imp49+ imp50+ imp51+ imp52+ imp53 + imp54
		f = imp55 + imp56+ imp57+ imp58+ imp59+ imp60+ imp61+ imp62+ imp63+ imp64+ imp65+ imp66+ imp67+ imp68+ imp69+ imp70+ imp71+ imp72+ imp73+ imp74+ imp75+ imp76+ imp77+ imp78+ imp79 + imp80+imp81

		aggregate_membership =  d+ e + f
		k=fuzz.defuzz(sen, aggregate_membership , 'centroid')
		result.append(k)
		#print(len(result))
	return result









