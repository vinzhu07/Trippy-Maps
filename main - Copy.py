import random
import time
import requests
from datetime import datetime

starttime=0
###Insert you own key! Keys are free from Google Dev Console and you have free monthly credit,
###But to avoid being botted, I have removed my own AUTH_Key. Thanks!
AUTH_KEY = ""
output = ""
masterdistance = []
masterduration = []
masteraddress= []
#startlocation=
####################################################################
trippy={'LexisNexis Risk Solutions':['ChIJ3eW3tG2e9YgR07e4SypatfU','1000 Alderman Dr, Alpharetta, GA 30005']}
planner = {}
def GoogPlac(loc):
  info = []
  #making the url
  locations=loc.split()
  LOCATION = ""
  for x in locations:
    LOCATION = ""+LOCATION+x+"+"
  MyUrl = ('https://maps.googleapis.com/maps/api/place/findplacefromtext/json?key=%s&input=%s&fields=name,place_id&inputtype=textquery&locationbias=ipbias') % (AUTH_KEY, LOCATION)
  place = requests.get(MyUrl)
  response_data = place.json()
  if response_data.get("status")=="OK":
    candidates = [response_data["candidates"]]
    location = candidates[0]
    stuff = location[0]
    name = stuff.get("name")
    placeid = stuff.get("place_id")
    info.append(placeid)
    output = "We found a match nearby!"
    print("We found a match nearby!")
    output=name
    print(name)
    time.sleep(1)
  else:
    return(False)

  MyUrl = ('https://maps.googleapis.com/maps/api/place/details/json?placeid=%s&fields=formatted_address,type&key=%s') % (placeid, AUTH_KEY)
  place = requests.get(MyUrl)
  response_data = place.json()
  if response_data.get("status")=="OK":
    stuff = response_data.get("result")
    address = stuff.get("formatted_address")
    thing = stuff.get("types")[0]
    info.append(address)
    masteraddress.append(address)

    
    
  else:
    output = "Error"
    print("Error")  
    return(False)
  trippy[name]=info
  return True

def DistTime():
  if len(Itinerary)>=2:
    
    for i in range(len(Itinerary)-1):
      #making the url
      start= trippy.get(Itinerary[i])
      startid = start[0]
      end = trippy.get(Itinerary[i+1])
      endid = end[0]
      MyUrl = ('https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=place_id:%s&destinations=place_id:%s&key=%s') % (startid, endid,AUTH_KEY)
      place = requests.get(MyUrl)
      response_data = place.json()
      if response_data.get("status")=="OK":
        rows = [response_data["rows"]]
        element=rows[0]
        elements = element[0]
        miles = elements.get("elements")
        time = miles[0].get("duration")
########Itinerary[i] to Itinerary[i+1]
        duration = time.get("text")
        masterduration.append(duration)
        mile = miles[0].get("distance")
        distance = mile.get("text")
        masterdistance.append(distance)

        #planner[x]=answers
        #output=planner
        #print(planner)
      else:
        return("No road path or internal error.")
  start= trippy.get(Itinerary[len(Itinerary)-1])
  startid = start[0]
  end = trippy.get(Itinerary[0])
  endid = end[0]
  MyUrl = ('https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=place_id:%s&destinations=place_id:%s&key=%s') % (startid, endid,AUTH_KEY)
  place = requests.get(MyUrl)
  response_data = place.json()
  if response_data.get("status")=="OK":
    rows = [response_data["rows"]]
    element=rows[0]
    elements = element[0]
    miles = elements.get("elements")
    time = miles[0].get("duration")
########Itinerary[i] to Itinerary[i+1]
    duration = time.get("text")
    masterduration.append(duration)
    mile = miles[0].get("distance")
    distance = mile.get("text")
    masterdistance.append(distance)      
  
  
      
    
################################################################
Itinerary=[]
Chinese=["chinese","dumplings", "fried rice","almond milk","asian pear","baby bok choy","baijiu","beef brisket","beggar's chicken","bitter melon","bubble tea","duck","chinese sausage","dragonfruit","green beans","egg drop soup","egg rolls","fortune cookie","fried milk","fried rice","noodles", "tea","hot and sour soup"]
Mexican=["mexican","taco", "burrito","enchilida", "gordita", "chalupa", "chimichanga", "guac","tortilla","frijole","quesadilla","salsa", "tamales","Quesarito"]
American=["american","burger","sausage","hot dog","steak","wing","nugget","fries", "potato", "shake", "sandwich", "slider","fried chicken", "bacon","beef","rib","chicken"]
Italian=["italian",'pasta','pizza','stromboli', "lasagna","risotto","truffles","gelato","tiramisu"]
Indian=["indian","curry", 'paneer', "tandoori","tikka masala","naan","dosa","biryani","rice","gulab" ]
Food=[Chinese,Mexican,American,Italian,Indian]
common=["panda","taco bell", "starbucks", "gym","mall", "subway", "marta", "airport", "bus","park","beach","pool"]
Places=[common]
staytime=[]
starttime=0

def intro():
  a=random.randint(0,3)
  if a==0:
    processinput(input("Hey, where would you like to go today? "))
  elif a==1:
    processinput(input("Hi, what place is on your mind? "))
  elif a==2:
    processinput(input("Hello. Where do you want to go? "))
  else:  
    processinput(input("Hey, what are you thinking about doing first? "))

def Continue():
  Yes=['ye','ok',"yes"]
  output=("Got it!")
  print("Got it!")
  x=input("Would you like to continue? ")
  x = x.lower()
  if any(x == y for y in Yes)==True:
    processinput(input("Where do you want to go next? "))
  else:
    finish()

def Time():
  x=input("How many minutes would you like to stay there? ")
  if (x.isdigit()==True and int(x)>4 and int(x)<360):
      staytime.append(int(x))
      Continue()     
  else:
    time.sleep(0.5)
    output="Sorry but your time was not valid. Please try again"
    print("Sorry but your time was not valid. Please try again")
    Time()

def commonresponses(answer):
  for x in common:
    if x==answer:
      return
      #Itinerary.append(x)
      #boolean check goog
  
def processinput(answer):
  answer=answer.lower()
  commonresponses(answer)
  if GoogPlac(""+answer.capitalize())==True:
      Time()
  elif any(z in answer for sublist in Food for z in sublist )==True: 
    for sublist in Food:
      for z in sublist:
        if z in answer:
          GoogPlac(""+sublist[0].capitalize()+" food")
          #Itinerary = trippy.keys()
          Time()
  elif any(z in answer for sublist in Places for z in sublist )==True:
    for sublist in Places:
      for z in sublist:
        if z in answer:
          GoogPlac(z)
          Time()
  elif greetings(answer)==True and len(answer)<12:
    main()
  else:
    unknown()

def unknown():
  output="I am sorry but I do not know how to help you."
  print("I am sorry but I do not know how to help you.")
  time.sleep(0.5)
  main()

def greetings(answer):
  List=["hi", "hey", "hello", "sup", "yo"]
  if any(x in answer for x in List):
    return True
  else:
    return False

def finish():
  stayminutes=["0"]
  print("Compiling itinerary...")
  time.sleep(1.5)
  print("OK. Here is what I compiled:")   
  for i in trippy:
    Itinerary.append(i)
  stayhours=["0"]
  for x in staytime:
    stayhours.append(x//60)
  for x in staytime:
    stayminutes.append(x%60)   
  DistTime()
  print("Itinerary")
  print("Your trip starts at " + str(starttime)+":00")
  print("Starting location: " + Itinerary[0])
  for x in range(len(Itinerary)):
    if x==0:
      continue
    print("Travel time: "+masterduration[x-1])
    print("Travel distance: "+masterdistance[x-1])
    print(str(x)+".",Itinerary[x]+":")
    print("\t Address:"+masteraddress[x-1])
    print("\t Time to Spend:",stayhours[x],"hours",stayminutes[x],"minutes")
  print("Travel time: ",masterduration[len(Itinerary)-1])
  print("Travel distance: ",masterdistance[len(Itinerary)-1])
  
    #travel time to, address, stay time
    #output=str(x)+".",Itinerary[x]+":",stayhours[x],"hours",stayminutes[x],"minutes"
  #trippy["starttime"]=starttime
  #print(trippy)
  #print(Itinerary)
  #print(masteraddress)
  #print(masterdistance)
  #print(masterduration)

def Begin():
  a=0
  b=0
  x= input("What time would you like to start your trip? Specify AM/PM ")
  global starttime
  if " " in x:
    y = x.split()
    if y[1].lower()=="pm":
      z = int(y[0])
      starttime=z+12
    else:
      starttime=y[0]
  else:
    if "pm" in x.lower():
      z=int(x[:-2])
      starttime= z+12
    else:
      starttime = x[:-2]    
    
def main():
  intro()
  start()

def start():
  while True:
    response = input()
    response=response.lower()
    processinput(response)

if __name__ == "__main__":
  Begin()
  main()
