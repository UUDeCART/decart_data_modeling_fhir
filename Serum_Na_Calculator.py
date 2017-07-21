
# coding: utf-8

# Install fhirclient via 'pip install'

# In[1]:

get_ipython().system('pip install fhirclient')


# Import the packages that will be needed to find the relevant information 

# In[6]:

from fhirclient import client
import fhirclient.models.patient as p
import fhirclient.models.observation as obs
import fhirclient.models.condition as cond
import datetime
from datetime import timedelta
from datetime import date
from dateutil.relativedelta import relativedelta


# Below sets up a 'client' so that we can access the HAPI server. The variable 'smart'

# In[4]:

settings = {
    'app_id': 'my_web_app',
    'api_base': 'https://fhirtest.uhn.ca/baseDstu3'
}
smart = client.FHIRClient(settings=settings)


# Here's the documentation on with examples on the python code:
# https://github.com/smart-on-fhir/client-py

# In[17]:

# Perform a GET on patient with id of 'cf-1500583253346'
import fhirclient.models.patient as p
patient = p.Patient.read('cf-1500583253346', smart.server)

# Print the first (i.e. [0] element in the patient.name
print ('Patient\'s Name = ',patient.name[0].given[0],patient.name[0].family)

# Define variable DOB as the patient's date of birth in a string format
DOB = patient.birthDate.isostring

# Print patient's gender
gender = patient.gender
print ('Gender = ',gender)
if gender == "female":
    sex=0.5
elif gender == "male":
    sex=0.6
print("sex", sex)  
# Print the patient's date of birth
print ('DOB = ', DOB)

# Define and print today variable
now = datetime.datetime.today()

print ('Today\'s Date = ', now)

#Define DOB2 date object
DOB2 = datetime.datetime.strptime(DOB, '%Y-%m-%d')

# Calcuate patient's age using rdelta method of the dateutil module
rdelta = relativedelta(now, DOB2)
age = rdelta.years
# print the years from the rdelta object
print ('Patient\'s age = ',age)


# In[18]:

#Weight
import fhirclient.models.observation as obs
search = obs.Observation.where(struct={'patient':"Patient/cf-1500583253346",'code':"29463-7"})
WT = search.perform_resources(smart.server)
if WT:
    WT_val = WT[0].valueQuantity.value
    #print(type(WT_val))
    print(str(WT_val) + " " + WT[0].valueQuantity.unit)


# In[19]:

#Serum Na
import fhirclient.models.observation as obs
search = obs.Observation.where(struct={'patient':"Patient/cf-1500583253346",'code':"2951-2"})
SR = search.perform_resources(smart.server)
if SR:
    SR_val = SR[0].valueQuantity.value
    #print(type(SR_val))
    print(str(SR_val) + " " + SR[0].valueQuantity.unit)


# In[20]:

#NaDeficit = Sex * NormalWgt * (DesiredNa - SerumNa)
DesiredNa= 140
NormalWgt = WT_val
SerumNa = SR_val
NaDeficit = sex * NormalWgt * (DesiredNa - SerumNa)
print (NaDeficit)

