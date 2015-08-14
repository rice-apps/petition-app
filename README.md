# Rice Petitions
An open source online platform that allows:
* Organizations to create elections with a time-frame and positions
* Rice Students to create petitions to be on the ballot for those elections
* Other Rice Students to sign those petitions
* Email notification to the petitioner and the organization administrators when the required number of signatures have been met

### Requirements
You must have Rice credentials to login to the application

### Running the application
* Install Python Version 2.7 or higher (https://www.python.org/downloads/)
* Install Google App Engine for Python (https://cloud.google.com/appengine/downloads)
    + Make sure you add product path to your PATH
    + In Windows, there is a checkbox in the installer
    + In Linux/Mac, it should be the following command with the path being the path to the google_appengine folder created: `PATH=$PATH:/home/computer_name/Desktop/google_appengine/`
* Clone the repository
    + This will create a petition-app folder
* Run the App Engine in Windows
    + Double-click the application. Go to `File`, `Add Existing Application`
    + Navigate to the petition-app folder for the Application Path
    + The admin port will be 8000
    + The port will be 8080
    + The name should say 'valued-mission-851'
    + Click the Run button in the top-left corner. Wait until the browse button is activated, and then click it
    + The project should open in your browser at http://localhost:8080
    + To stop running the application, just press the Stop button
* Run the App Engine in Mac/Linux
    + In the command line, navigate to the directory just above petition-app
    + Type the following command: `dev_appserver.py petition-app`
    + The project will be running at http://localhost:8080
    + To stop running the application, just enter `[Ctrl] + c`

### Server Logs and Database
* To view the server logs
    + In Windows, just click the Logs button in Google App Engine
    + In Mac/Linux, the logs will just appear in the command prompt window
* To view the local database, navigate to http://localhost:8000/datastore in the browser

### Configuration
* To run as an administrator, just change the `ADMIN_ID` to your net-id in the config.py file
* To change debugging options, change the `DEBUG` variable to either `True` or `False`

### Questions? Suggestions?
* Just email rsk8@rice.edu



