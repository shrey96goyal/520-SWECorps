## Team - SDECorps
## 520 Course Project - ELeNa
The project is about implementing a navigation system that considers the elevation gain. A typical system like Apple or Google Maps just takes the start and end points from the user and presents the shortest distance between them using standard algorithms such as Dijkstra’s or A*.  The goal of this project is to develop a software system that determines a route to minimize/maximize the elevation gain depending on the start and end locations of the user. The elevation gain increment/decrement can change the distance to up to x% of the original shortest route. 

For the purposes of this project, we have used 'drive' as the mode of transport to load the graph using OSMnx.
<br />

### 1. Install requirements for running the application
##### `pip install -r requirements.txt`

### 2. Start the backend server
#### Navigate to backend/controller and run the following command
##### `python server.py`

### 3. In order to perform integration testing of backend and unit testing of backend
#### Navigate to backend/tests, run following command
##### `pytest`

### 5. To use the application, navigate to frontend/view/
##### Open the front_end_body.html in browser
##### Start using the application!

<br />
<br />

### The user can interact with the application in the following way
<br />

#### 1. The start screen of the application looks as follows
#### ![plot](./output/1.png)
<br />

#### 2. Using the top magnifying glass, the user can enter the source location
#### ![plot](./output/2.png)
<br />

#### 3. After typing the source location, they hit enter and the location will be visible in the text box on the right side
#### ![plot](./output/3.png)
<br />

#### 4. Similarly, using the bottom magnifying glass, the user can enter the target location. Suggestions for the location will be visible, out of which user can select one
#### ![plot](./output/5.png)
<br />

#### 5.By default, the option for shortest path is selected
#### ![plot](./output/6.png)
<br />

#### 6. User can select appropriate option for elevation
#### ![plot](./output/7.png)
<br />

#### 7. User can enter the desired distance percentage. Default value is 0.
#### ![plot](./output/8.png)
<br />

#### 8. Upon clicking the 'Get Path' button, a message is displayed indicating that response is yet to be recieved
#### ![plot](./output/10.png)
<br />

#### 9. Upon receiving the response, path is displayed on the map and total distance and elevation is displayed along the path
#### ![plot](./output/9.png)
<br />

#### 10. A different source/target location can be selected and using the appropriate options, the path for the same will be retrieved
#### ![plot](./output/11.png)
<br />

#### 11. If the user enters source/target locations from different cities, the corresponding error message will be displayed
#### ![plot](./output/12.png)
<br />