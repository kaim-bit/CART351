#import the lib
import requests

#city arg
city = "Montreal" 

#my api key -> you should add yours
api_key = "0853ab2aadbc94b89b83b05f7d664c79" 

#url to get results with the city added
url_with_city ="http://api.openweathermap.org/data/2.5/weather?q=" +city 

#url with the api key appeneded
url_to_send = url_with_city + "&APPID=" + api_key 

#make the request
response = requests.get(url_to_send) 

#get the response as json
data = response.json() 

#print
print(data)