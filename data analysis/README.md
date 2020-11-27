# Data analysis

## Step 1 : Requests to get data

### The basics of sending a GET request to a server

`basic_request.py` : Sends a request to the Binance servers and prints the server time in datetime format

### Sending a GET request and write the JSON data into a .csv file

`get_data.py` : Sends a request to the Binance servers and stores the requested json data in a csv file

## Step 2 : Load and visualize data

### load a .csv file, prepare the data and visualize it

`load_prep_visualize.py` : This program loads a .csv file, prepares the data and plots it for visualization

## Step 3 : Explore the data and get insights

### Find relationships among variables

`linear_regression.py` : Use Scikit-Learn package to perform an univariate linear regression 

Find relationships between Price, Volume and Number of trades