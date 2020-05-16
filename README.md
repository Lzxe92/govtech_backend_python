# Household APP App

a [flask](https://flask.palletsprojects.com/) application

  
## Database Setup Guide
* Create a database, named govtech_household_dev for this project
* Database User and Password for development can be set at [/app/main/config.py](app/main/config.py)

## Data Dictionary
* [Database Data Dictionary](database/data_dictionary.docx)
* Read it for the schema details of the database.


### Startup guide
* Python 3.7 is required
* python library are specified under [requirements.txt](requirements.txt).
1. Run the code below to install python required libraries and flask
    ```
    pip install -r requirements.txt
    ```
2. Run the code below to populate the database. Setup the database first by following "Database Setup Guide" at the top.
    ```
    manage.py db upgrade
    manage.py seed
    ```   
2. Run the code below to Start the App at Development Mode
    ```
    manage.py run
    ```
3. Default endpoint is running at http://localhost:5000 

### Test Guide
* Unit test are located at /test.
1. Run the code below to run the unit test on the controllers
    ```
    manage.py test
    ```

### Endpoints for assignment 
* API documentation http://localhost:5000/docs/
1. Create Household

    As this app is designed with relationship database in mind. Members and household are on a different table, they are linked up through an association table.
    There is actually two way to create household with members. 
    
    a. In one api call, a household with members inside
    ```
    curl --location --request POST 'http://127.0.0.1:5000/household/' \
    --header 'accept: application/json' \
    --header 'Content-Type: application/json' \
    --header 'Content-Type: text/plain' \
    --data-raw '{
      "type": 1,
      "members": [
        {
          "nric": "S9992098C",
          "name": "Eric Lee",
          "gender": 1,
          "dob": "1992-05-15",
          "annual_income": 123987,
          "occupation_type": 1,
          "marital_status": 1,
          "spouse_nric": "S9489098C"
        },
         {
          "nric": "S9489098C",
          "name": "Yan Ni",
          "gender": 2,
          "dob": "1994-05-15",
          "annual_income": 123987,
          "occupation_type": 1,
          "marital_status": 1,
          "spouse_nric": "S9992098C"
        }
      ]
    }'
    ```
    b. In three api call 
    
    Firstly create the household
    ```
    curl --location --request POST 'http://127.0.0.1:5000/household/' \
    --header 'Content-Type: application/json' \
    --data-raw '{
      "type": 1
    }'
    ```    
   
    Then create the member
    ```
    curl --location --request POST 'http://127.0.0.1:5000/member/' \
    --header 'Content-Type: application/json' \
    --data-raw '{
          "nric": "S9992098C",
          "name": "Eric Lee",
          "gender": 1,
          "dob": "1992-05-15",
          "annual_income": 123987,
          "occupation_type": 1,
          "marital_status": 1,
          "spouse_nric": "S9489098C"
    }'
    ```    
   
     Then add member into household (assuming both of their primary id is 1)
    ```   
    curl --location --request POST 'http://127.0.0.1:5000/household/1/member/1' \
    --header 'accept: application/json' \
    --header 'Content-Type: application/json'
    ```   
2.

 

### Links

+ [Flask documentations](https://flask.palletsprojects.com/en/1.1.x/)

### Coding guideline

* Use strictly waterline query
* split common used codes into services (Services in MVCS)
* thin controller, fat model (services and models are models)




