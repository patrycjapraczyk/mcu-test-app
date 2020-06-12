# Testing of Data Acquisition Board with Python

  

The project contains an application that analyses, logs and visualises data frames coming from the hardware.

For more information about functional requirements and project design, please consult **Preparations for the first radiation test campaign of Data Acquisition Board (DAQ)** section of the **internal note of Patrycja Praczyk**.

The project also provides a GUI for interacting with the board.

GUI was developed via **Flask** framework.

It is intended to be used during the radiation test of the DAQ board.

  

Project Python dependencies/packages, must be installed before running the project:

* Flask 1.1.1
* Flask-JSGlue 0.3.1
* Jinja2 2.11.1
* MarkupSafe 1.1.1
* Werkzeug 1.0.0
* click 7.1.1 
* itsdangerous 1.1.0
* pip 19.0.3
* pyserial 3.4
* setuptools 40.8.0

  
  

## Repository structure and file overview

* controller/ - controllers, contain functions for model and view interaction
	* StartController.py - controller functions for the start page
	* MainController.py - controller functions for the main page
* model/
	* Communication/ - all communication related classes
	* ComInterfaceFactory.py - creates and gets a communication interface of the type given
	* CommunicationManager.py - controls communication with the client, holds queues for data to be sent and received, contains heartbeat loop and sends commands to the client
	* ETHSocketManager.py - manages Ethernet communication - based on socket API
	* SerialManager.py - manages serial communication
* Data/ - representation of data frames of different types and their storage
	* ComError.py
	* ComErrorStorage.py
	* Data.py
	* DataStorage.py
	* MemErrorData.py
	* MemErrorStorage.py
	* ResetData.py
	* ResetStorage.py
* Interfaces/ - abstract classes
	* ComInterface.py
	* FileManager.py

* Logging/ - all logging related classes,
When logging to files with a more specific message format, create a new class with Logger composition
	* ComErrorLogger.py
	* JSONEncoder.py
	* Logger.py - basic Logger class, holds file manager interface (for example TextFileManager)
	* MemErrorLogger.py
	* ResetLogger.py
	* TextFileManager.py - text file IO
* Observer/ - Observer pattern related abstract classes
* StaticClasses/ - classes containing static helper functions for various purposes
	* Calculator.py
	* Checksum.py
	* DataPacketFactory.py - creates and returns a bytearray of a packet with a specific format related to MSG_CODE
	* DataStructFunctions.py
	* GlobalConstants.py - global constants for all files across the project
	* StrManipulator.py
	* Time.py

* DataProcessingThread.py - inherits from Thread, performs correctness analysis of data packets (according to the frame format)

* static/
	* assets/ - all GUI assets, such as images
	* css/ - css files for GUI styling
		* common.css - common styles
		* start.css - start page styles
		* styles.css - main page styles
	* js/ - JavaScript files, written in jQuery style
		* drop-down - drop down menu js
		* index.js - js for main page, contains AJAX requests for getting info from the model
	* lib/ - imported libraries for the view- jquery and fontawesome (for icons)
* templates/ - Jinja templates (a templating library that ships with Flask, similar to HTML)
	* base.html - structure common for all pages
	* index.html - main page blocks
	* start.html - start page blocks
* test/ - a folder with unit tests and hardware simulator
	* TestSerialCom.py - hardware simulator
* app.py - contains main function and routes/REST API functions

## Instructions for running the app:

* to run the GUI execute app.py
  GUI is a web-app running locally. 
  For viewing it, open the browser with your localhost address printed in the console, for example http://127.0.0.1:5000/
  It is recommended that Google Chrome browser is used.
* for testing purposes, run hardware simulator - TestSerialCom.py, while running the Flask app at the same time,
* for creating virtual ports (useful for testing) on Windows, use the following program: 
https://freevirtualserialports.com

## Future development:
Detailed description and instructions of the future tasks is found under **Gitlab issues**