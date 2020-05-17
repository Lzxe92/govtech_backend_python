# Household APP App

a [flask](https://flask.palletsprojects.com/) application

  
## Database Setup Guide
* Create a database, named govtech_household_dev for this project
* Create a database, named govtech_household_preprod for testing 
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
* Unit & Integration test are located at /test.
1. Setup Testing database at TestingConfig [/app/main/config.py](app/main/config.py)
2. Run the code below to run the unit test on the controllers
    ```
    manage.py test
    ```
3. Not 100% was done but just a POC at the moment

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
2.  Add a family member to household
    
    It's actually described above under 1.b)
    
3.  List households
    ```       
    curl --location --request GET 'http://127.0.0.1:5000/household'
    ```   
4.  Show household

    Below is an example of showing household under the household_id 1
    ```   
    curl --location --request GET 'http://127.0.0.1:5000/household/1' 
    ```      
5.  Search for households and recipients of grant disbursement endpoint

    This API allows the use of search parameters with values to filter out 
    household that are eligible for grant disbursement. They work as an AND operation,
    search will be filtered based on the parameters provided and the values.
    The values will consist of operator followed by operand. 
    
    EG. search?age=lt16
    ```         
    household with someone age less than 16
    ```         
    
    EG. search?age=lt16&total_income=lt150000
    ```   
     (Household with someone age less than 16) AND (Household with total income less than $150,000)
    ```       
    The following are the search parameters allowed and the defination
    
    1. age
    2. total_income
    3. marital_status
    4. household_type
    
    The following are the operator parameters allowed, followed by the defination
    
    1. lt   (Less than)
    2. gt   (Greater than)
    3. le   (Less than and equal to)
    4. eq   (Equal to)
    5. ne   (Not equal)
    6. ge   (greater than and equal to)
    
    The following below are the endpoints to filter out household eligibility for bonus
    
    1. List households and qualifying family members for <b>Student Encouragement Bonus</b>
        1. Households with children of less than 16 years old
        2. Household income of less than $150,000.

        ```   
        curl --location --request GET 'http://127.0.0.1:5000/household/search?age=lt16&total_income=lt150000'
        ```          
    
    2. List households and qualifying family members for <b>Family Togetherness Scheme</b>
        1. Households with husband & wife
        2. Has child(ren) younger than 18 years old.

        ```   
        curl --location --request GET 'http://127.0.0.1:5000/household/search?age=lt18&marital_status=eq1'
        ```                   
       
    3. List households and qualifying family members for <b>Elder Bonus</b>
        1. HDB household with family members above the age of 50

        ```   
        curl --location --request GET 'http://127.0.0.1:5000/household/search?age=gt50&household_type=eq1'
        ```           
                  
    4. List households and qualifying family members for <b>Baby Sunshine Grant</b>
        1. Household with young children younger than 5.

        ```   
       curl --location --request GET 'http://127.0.0.1:5000/household/search?age=lt50'
        ```
       
    5. List households that qualify for the <b>YOLO GST Grant</b>
        1. HDB households with annual income of less than $100,000.

        ```   
       curl --location --request GET 'http://127.0.0.1:5000/household/search?age=lt5'
        ```                 
6.  Show Member

    Below is an example of showing household under the member_id 1
    ```   
    curl --location --request GET 'http://127.0.0.1:5000/member/1' 
    ```       
### Links

+ [Flask documentations](https://flask.palletsprojects.com/en/1.1.x/)
+ [Sqlalchemy documentation (Database layer)](https://www.sqlalchemy.org/)

### Coding guideline

* Use orm query
* split common used codes into services (Services in MVCS)
* thin controller, fat model (services and models are models)




