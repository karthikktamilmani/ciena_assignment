# OSA

Deployed Application: You can find the application up and running on https://ciena-osa.herokuapp.com/.

API end point:

```
https://ciena-osa.herokuapp.com/api/
```

## Getting Started

Refer the following sections on how to install, run, and deploy the Moviesight application.


### Prerequisites

To have a local copy up and running on your machine, you will first need to install python3 in your machine.

### Installing

Follow the steps listed below to setup the app, and run it on your local machine / computer.

#### Step 1: Clone Repository

Run the following command from the terminal on your machine, to clone the repository:

```
git clone https://github.com/karthikktamilmani/ciena_assignment.git
```

#### Step 2: Install Dependencies

Navigate into the `ciena_assignment` folder and run the following command to install the required dependencies:

```
pip3 install -r requirements.txt
```

#### Step 3: Start The Dev Server

To start the app, without any complicated build steps, simply start the development sever through the following command:

```
python3 app.py
```

#### Step 4: The Application

In the last step, open your web browser, and navigate to `localhost:5000` to view a running instance of the application. If everything went fine, you should see the following page:

![Image of App Running](/deployed_app.png)

### Running via Docker

This app can also be served via Docker. Make sure docker is installed in the local machine. Follow the below steps to run via docker:

#### Step 1: Clone Repository

Run the following command from the terminal on your machine, to clone the repository:

```
git clone https://github.com/karthikktamilmani/ciena_assignment.git
```

#### Step 2: Build docker image

Navigate to `ciena_assignment` folder and run the below command to build a docker image:

```
docker build -t ciena-osa .
```

#### Step 3: Run docker image

After building the docker image, run the image using:

```
docker run -p5000:5000 ciena-osa
```

#### Step 4: The Application

In the last step, open your web browser, and navigate to `localhost:5000` to view a running instance of the application. If everything went fine, you should see the following page:

![Image of App Running](/deployed_app.png)

## Sample Screenshot

The below image shows a sample screenshot of the graph and fields to query the commands:

![Image of Sample App](/sample_graph.png)

## Features available

* Options to zoom, pan, download, scale the graphs
* Overlay of graphs upto 3 values
* Input field to enter the commands and a response box
* Logs tab -> shows the time of the request and the subsequent response data and time
* For API endpoints, Timeout or random data are handled and 503 Service Unavailable error is thrown instead of a 200 status code.

## Assumptions

* Clicking on Start button invokes the START command and only when Stop button is clicked, STOP command is sent and TRACE is plotted.
* Clicking Single button invokes SINGLE command, waits for 1 second and initiates a TRACE command to plot the graph.
