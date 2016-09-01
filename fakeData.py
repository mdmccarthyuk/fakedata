#!/usr/bin/python

from faker import Faker,Factory
import random
import hashlib

countryCodes = ['en_GB/United Kingdom','fr_FR/France','pl_PL/Poland','it_IT/Italy','en_US/United States','es_ES/Spain','nl_NL/Netherlands','el_GR/Greece','de_DE/Germany']
personalTaxonomyCodes = ["02001", "02002", "02003", "02004", "03001", "03002", "03003", "10001", "10002", "10003"]
householdTaxonomyCodes = ["01000", "01001", "01002"]

fake = Factory.create('en_GB')
randomFactory = random

def makeHousehold():
	family=[]
	adultAge=randomFactory.randint(18,60)
	maxChildAge=int(adultAge*0.25)
	if randomFactory.random() > 0.5:
		# MARRIED
		familySize=2
		lastName=fake.last_name()
		# KIDS?
		if(randomFactory.random() > 0.5):
			familySize=2+randomFactory.randint(1,4)
		for x in range(0,familySize):
			if x<2:
				age=adultAge+randomFactory.randint(0,5)
			else:
				age=randomFactory.randint(1,maxChildAge)
			if x==0:
				firstName=fake.first_name_male()
				prefix=fake.prefix_male()
			if x==1:
				firstName=fake.first_name_female()
				prefix=fake.prefix_female()
			if x>1:
				if randomFactory.random() > 0.5:
					firstName=fake.first_name_male()
					prefix=fake.prefix_male()
				else:
					firstName=fake.first_name_female()
					prefix=fake.prefix_female()

			family.append(firstName+","+lastName+","+str(age))
	else:
		parentName = fake.last_name()
		# UNMARRIED
		familySize=1
		if(randomFactory.random() > 0.5):
			# COUPLE
			familySize=2
			# KIDS?
			if(randomFactory.random() > 0.2):
				familySize=2+randomFactory.randint(1,4)
		for x in range(0,familySize):
			if x==1:
				lastName=fake.last_name()
			else:
				lastName=parentName
			if x<2:
				age=adultAge+randomFactory.randint(0,5)
			else:
				age=randomFactory.randint(1,maxChildAge)
			family.append(fake.first_name()+","+lastName+","+str(age))

	return family

def main():
	#GENERATE COUNTRIES
	with open('output.csv','w') as outputFile:
		for locale in countryCodes:
			localeSplit = locale.split('/')
			fake = Factory.create(localeSplit[0])
			country = localeSplit[1]
			#City
			for y in range(0,80+randomFactory.randint(10,50)):
				city = fake.city()
				for z in range(0,1000+randomFactory.randint(25,1500)):
					address = fake.building_number()+","+fake.street_name()+","+city+","+fake.postcode()
 					houseTax = ""
 					for code in householdTaxonomyCodes:
 						if (randomFactory.random() > 0.5):
							houseTax = houseTax + code + "|"
					for person in makeHousehold():
						try:
 							personTax = ""
 							for code in personalTaxonomyCodes:
 								personTax = personTax + code + "|"
							hashedID=hashlib.md5((person+","+address+","+country).encode('utf-8')).hexdigest()
							outputFile.write((hashedID+","+person+","+address+","+country+","+houseTax+personTax+"\n").encode('utf-8'))
						except Exception, e:
							##print "BAD RECORD: "+hashedID+","+person+","+address+","+country+" - "+e
							print e

if __name__ == '__main__':
    main()

