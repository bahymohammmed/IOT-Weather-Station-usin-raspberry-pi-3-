import sys
import urllib
import urllib2
from time import sleep
import Adafruit_DHT as dht
import Adafruit_BMP.BMP085 as BMP085 # Imports the BMP library


# My ThingSpeak API key ( you need to replace it with your key )
myAPI = 'WIF55E621FNCEH7L'
# My Thingtweet API key ( you need to replace it with your key )
tweetAPI = 'UL5RJC37HA2N67LU'

# URL where we will send the data
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI 
# URL where we will send the data
tweetURL = 'https://api.thingspeak.com/apps/thingtweet/1/statuses/update/'   
tweetForm = "The Weather Status : Temprature = %s , Humidity = %s , Pressure = %s , SeaLevel Pressure = %s and The Altitude = %s "

# Reading from BMP sensor 
sensor = BMP085.BMP085()
def BMP180_data():
    pres = float(format(sensor.read_pressure()))  # The local pressure
    slpres = float(format(sensor.read_sealevel_pressure())) # The sea-level pressure
    alt = float(format(sensor.read_altitude())) # The current altitude
  
    return pres,slpres,alt

# Reading from DHT sensor 
def DHT22_data():
    # Reading from DHT22 and storing the temperature and humidity
    humi, temp = dht.read_retry(dht.DHT22, 23) 
    return humi, temp
# Reading the values, Upload and Tweet it 
while True:
    try:
        humi, temp = DHT22_data()
        pres, slpres, alt = BMP180_data()
        # If Reading is valid
        if isinstance(humi, float) and isinstance(temp, float):
            # Formatting to two decimal places
            humi = '%.2f' % humi                       
            temp = '%.2f' % temp
            pres = '%.2f' % pres
            slpres = '%.2f' % slpres
            alt = '%.2f' % alt
            # Sending the data to thingspeak
            conn = urllib2.urlopen(baseURL + '&field1=%s&field2=%s&field3=%s&field4=%s&field5=%s' % (temp, humi, pres, slpres, alt))            
            print (conn.read())
            # Closing the connection
            conn.close()
            
            # Sending the data to Twitter
            tweet = tweetForm % (temp, humi, pres, slpres, alt)
            data = urllib.urlencode({'api_key' : tweetAPI, 'status': tweet})
            response = urllib2.urlopen(url=tweetURL, data=data)
            print(response.read())
            print ("Tweet Succeeded")
            

        else:
            print ('Error')

 # sleeping time in seconds between the results ( you can change it as you want )        
        sleep(10)

    except:
        break
    
