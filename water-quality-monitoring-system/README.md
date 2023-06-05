Water Monitoring System

This is a project for monitoring water quality in water management systems. The system consists of water monitoring devices deployed at different locations, which collect readings such as pH, temperature, and dissolved oxygen. The collected data is then sent to a database for storage and analysis.

Features

Real-time monitoring of water quality
Easy deployment and management of water monitoring devices
Analysis of collected data to aid in water management
Notification system for users to receive alerts based on predefined thresholds
Technologies Used

Raspberry Pi for collecting data from sensors
Python for programming the Raspberry Pi
SQLite for database management
Flask for web development
Getting Started

To get started with the project, you will need the following:

Raspberry Pi with connected sensors
Python installed on the Raspberry Pi
SQLite installed on the Raspberry Pi
Flask installed on the Raspberry Pi
Once you have all the necessary components, you can clone the repository and start the application by running python app.py in your terminal.

Usage
The water monitoring system is designed to be easy to use and manage. You can access the web interface by visiting http://localhost:5000 in your web browser. From there, you can view the collected data, manage devices, and set up notifications.

Graphical User Interface 
Our GUI will provide a user-friendly interface for users to monitor and control their home's environmental factors. The interface will have a login screen where users can enter their username and password. Once logged in, the interface will display real-time updates for temperature, water level, and pH level. Users will be able to control the settings of the smart home automation system, such as adjusting the temperature or turning on/off the water pump, through the GUI. The system will also record and log the sensor readings in a SQLite database and a text file for future reference. The GUI will be developed using the Kivy framework and Python programming language.

Database
In addition to displaying the sensor data, the system will also log the data to a SQLite database for later analysis. The database will store the timestamp, temperature, water level, and pH level for each reading, and will allow the user to query the data and generate graphs and other visualizations.
Contributors

Codye Singh (codyesingh@yahaoo.com)
Michael Arciniega (primistandem9@gmail.com)
License
WQMS

This project is licensed under the MIT License - see the LICENSE file for details.
