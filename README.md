# Sigma Technology RC-car

![Front Image](images/front_image.jpg)
An ongoing project in creating an autonomous RC-car that can follow lanes.

## Background
###### Password for the Jetson Nano at the office is ```sigma```
This project contains two different software running on two different units connected via Ethernet.
##### 1. Nvidia Jetson Nano - Running Python code with lane detection
##### 2. Arduino MEGA 2560 - Running C code to control motor and servo

These units communicate over Ethernet to get the RC-car moving within the lanes.

## Installation

#### Jetson Nano
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required packages.
Required packages are currently:
```
cv2
numpy
tplotlib.pyplot
```
These should be preinstalled if using the same Jetson Nano that was previously used. 
Python 3.6+ is also required but is also preinstalled. 
Then just download this GitHub repo.

#### Arduino

From the downloaded GitHub repo open the ```rc_control.cpp``` in Platform.io in Visual Studio Code. [Install Guide for VSC.](https://docs.platformio.org/en/latest/ide/vscode.html)


You will need to install the following libaries though Platform.io:
```
Ethernet
Servo
ArduinoJson
nlohmann-json
```
Flash the Arduino with the software provided.

In the software the pins for the servo and motor are defined as following:

```c
#define steeringControl 5
#define motorPin 4
```

## Usage
#### 1. Arduino
Boot up the Arduino with the server and motor connected to the corresponding pins.
#### 2. Jetson Nano
Open a terminal in the downloaded directory. 
Then run:
```bash
python ./start.py
```
The Jetson and Arudino should now have communication through the Ethernet cable and start working on controlling the car. If you have the Jetson Nano connect to an HDMI you can enable the output from the camera. To do that open the ```start.py``` file and look for 
```python
#Enable line below to show the final output on the screen
#cv2.imshow("result", combo_image)    
```
or 
```python
#Enable line below to show the black/white contrast output
#cv2.imshow("cropped", cropped_image)
```
Enable one or both options. First one will show you a result as the 1 output picture below and the second one will give you an output like picture 3 and 4.


## Output Images

- ![#f03c15](https://placehold.it/15/f03c15/000000?text=+) `Detected lane(s)`
- ![#c5f015](https://placehold.it/15/c5f015/000000?text=+) `Boundry for lane detection`
- ![#1589F0](https://placehold.it/15/1589F0/000000?text=+) `Path RC-Car will follow`

Car Going Straight Final Ouput 
![Straight Color](images/output_data/straight_color.png)
Car Turning Final Ouput 
![Turn Color](images/output_data/turn_color.png)

Car Going Straight Contrast(black/white) Ouput 
![Straight No Color](images/output_data/straight_no_color.png)
Car Turning Contrast(black/white) Ouput 
![Turn No Color](images/output_data/turn_no_color.png)


## Contributers
[Martin Myhrman](https://skies.sigmatechnology.se/main.asp?rID=1&alt=2&username=miy)

[Simon Malmberg](https://skies.sigmatechnology.se/main.asp?rID=1&alt=2&username=smg)

[Rakshith M Rao](https://skies.sigmatechnology.se/main.asp?rID=1&alt=2&username=rmo)

[Oskar Hellqvist](https://skies.sigmatechnology.se/main.asp?rID=1&alt=2&username=oht)
