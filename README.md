# WearAQ
Files and code for WearAQ experiment - specifically centered around data fetching from external sources and the different models employed

## Files
### WearAQ_data_assets
To get an idea of the environment, we're pulling data from open source sensors and platforms. These platforms are:
- Organicity
- Thingful
- London Air Quality Network
This file holds the endpoints and parses through the response to pull necessary datapoints

### WearAQ_LAQN_data
Since there isn't the largest spread of AQ data in the region, we need to look at other sources such as traffic and weather. This file holds a model used to predict AQ from these external factors

### WearAQ_kriging
To recommend locations for the participants to take measurements at, we're using a method called kriging. This method is used for interpolation in spatial statistics. Basically, given a set of known points, it returns a cloud estimation of all points along with the error as well as total model error. Using these measures we can recommend locations to collect data based on highest error, and highest likelihood to decrease total error of the model.
Found a few sources explaining this in a little more detail here:
- One of the libraries im using: http://pykriging.com/
- The wiki: https://en.wikipedia.org/wiki/Kriging
- A better explanation: http://gisgeography.com/kriging-interpolation-prediction/

### WearAQ_model
For the recommendation model that we want on the server, this file contains just the relevant code needed.

## Folders
### Sandbox
Just somewhere I play around with the data, with some incomplete ideas that I don't wanna throw away just yet

### Data
Data from the LAQN - houses 7 datasets in and around tower hamlets
Data from the workshops

### Images
Images and maps generated from code in exp
