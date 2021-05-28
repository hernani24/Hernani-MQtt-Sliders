from adafruit_clue import clue  #importing clue from the adafruit_clue library
import paho.mqtt.client as mqtt #importing the pqho mqtt client as mqtt


# this will display text on the different sensors
def display_text(clueValue):
    clue_data[0].text = "Accel: {} {} {} m/s^2".format(*(clueValue["clueSlider/accelXRange"], clueValue["clueSlider/accelYRange"], clueValue["clueSlider/accelZRange"]))    #display in the clue_data index zero the acceleration  value of x, y & z
    clue_data[1].text = "Gyro: {} {} {} dps".format(*(clueValue["clueSlider/gyroXRange"], clueValue["clueSlider/gyroYRange"], clueValue["clueSlider/gyroZRange"]))          #display in the clue_data index one the gyro value of x, y & z
    clue_data[2].text = "Magnetic: {} {} {} uTesla".format(*(clueValue["clueSlider/magneticXRange"], clueValue["clueSlider/magneticYRange"], clueValue["clueSlider/magneticZRange"]))   #display in the clue_data index two the magnetic range value of x, y & z
    clue_data[3].text = "Pressure: {} hPa".format(clueValue["clueSlider/pressureRange"])    #display in the clue_data index three the pressure range value 
    clue_data[4].text = "Temperature: {} C".format(clueValue["clueSlider/tempRange"])       #display in the clue_data index four the temperature range value 
    clue_data[5].text = "Humidity: {} %".format(clueValue["clueSlider/humidityRange"])      #display in the clue_data index five the humidity range value 
    clue_data[6].text = "Proximity: {}".format(clueValue["clueSlider/proximityRange"])      #display in the clue_data index six the proximity range value 
    clue_data[7].text = "Color: {}, {}, {}".format(*(clueValue["clueSlider/colorRRange"], clueValue["clueSlider/colorGRange"], clueValue["clueSlider/colorBRange"], clueValue["clueSlider/colorCRange"]))    #display in the clue_data index seven the rgb color range value
    clue_data[8].text = "Light: {}".format(clueValue["clueSlider/colorCRange"])  #display in the clue_data index eight the light sensor value
    clue_data.show()
    
#initializing the clueData variable with the value of the topics
clueData = {
    "clueSlider/accelXRange" : 0,  #set the clue acceleration X value to zero, this will reflect in the clue accel x index
    "clueSlider/accelYRange" : 0,   #set the clue acceleration  Y value to zero, this will reflect in the clue accel y index
    "clueSlider/accelZRange" : 0,   #set the clue acceleration Z value to zero, this will reflect in the clue accel z index
    "clueSlider/gyroXRange" : 0,    #set the clue gyro X value to zero, this will reflect in the clue gyro x index
    "clueSlider/gyroYRange" : 0,    #set the clue gyro y value to zero, this will reflect in the clue  gyro y index
    "clueSlider/gyroZRange" : 0,    #set the clue gyro z value to zero, this will reflect in the clue  gyro z index
    "clueSlider/magneticXRange" : 0,    #set the clue magnetic x value to zero, this will reflect in the clue magnetic x index
    "clueSlider/magneticYRange" : 0,    #set the clue magnetic y value to zero, this will reflect in the clue magnetic y index
    "clueSlider/magneticZRange" : 0,    #set the clue magnetic z value to zero, this will reflect in the clue magnetic z index
    "clueSlider/pressureRange" : 800,   #set the clue pressure value to 800, this will reflect in the clue pressure index
    "clueSlider/tempRange" : clue.temperature,  #set the clue temperature value  to clue.temperature, this will reflect in the clue temp index
    "clueSlider/humidityRange" : clue.humidity, #set the clue humidity value to clue.humidity, this will reflect in the clue humidity index
    "clueSlider/proximityRange" : clue.proximity,   #set the clue proximity value to clue.proximity, this will reflect in the clue proximity index
    "clueSlider/colorRRange" : 0,   #set the clue color red value to zero, this will reflect in the clue red index
    "clueSlider/colorGRange" : 0,   #set the clue color green value to zero, this will reflect in the clue green index
    "clueSlider/colorBRange" : 0,   #set the clue color blue value to zero, this will reflect in the clue blue index
    "clueSlider/colorCRange" : 0   #set the clue light sensor value to zero, this will reflect in the clue light sensor index
}

#define the on_connect function with 4 parameters
def on_connect(client, userdata, flags, rc):
    if rc == 0:                             #if result code is zero
        client.subscribe("clueSlider/#")    #it will subscribe to  a certain topic
        display_text(clueData)              #then it will call up the display_text function that accepts the clueData

#define an on_message function that will ask 3 parameters
def on_message(client, userdata, msg):
    print(msg.topic)                        #prints out the topic
    print(msg.payload.decode())             #prints out the decoded payload/value
    clueData[msg.topic]= msg.payload.decode() #this will identify the msg topic then will decode the payload
    display_text(clueData)                   #this will display_text with the value of the clueData

clue_data = clue.simple_text_display(text_scale=2) #set the scale of the text to #2

client = mqtt.Client()          #initializing the variable client to the mqqt Client() built in function
client.on_connect = on_connect  #initializing the client.on_connect to the value of the on_connect function
client.on_message = on_message  # initializing the client-on_message to  the  value of on-message function
client.connect("mqtt.eclipseprojects.io", 1883, 60) #client connect to the broker eclipse

client.loop_forever() #infinite loop unless stop by the user