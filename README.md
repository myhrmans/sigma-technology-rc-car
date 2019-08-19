# Sigma Technology RC-car

An ongoing project in creating an autonomous RC-car that can follow lanes.

## Background
This project contains two different software running on two different units connected via Ethernet.
##### 1. Nvidia Jetson Nano - Running Python code with lane detection
##### 2. Arduino MEGA 2560 - Running C code to control motor and servo

These units communicate over Ethernet to get the RC-car moving within the lanes.

### Theory



## Installation

#### Jetson TX2
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

From the downloaded GitHub repo open the 

## Usage
Open a terminal in the downloaded directory. 
Then run:
```bash
python ./start.py
```
This is going to start up the 
```python
import foobar

foobar.pluralize('word') # returns 'words'
foobar.pluralize('goose') # returns 'geese'
foobar.singularize('phenomena') # returns 'phenomenon'
```
## Result Images
- ![#f03c15](https://placehold.it/15/f03c15/000000?text=+) `Detected lane(s)`
- ![#c5f015](https://placehold.it/15/c5f015/000000?text=+) `Boundry for lane detection`
- ![#1589F0](https://placehold.it/15/1589F0/000000?text=+) `Path RC-Car will follow`
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
