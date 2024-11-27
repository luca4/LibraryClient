source code: https://github.com/luca4/LibraryClient/tree/master

# Library Client

developed using Python 3.12.6 on Windows 10

## Setup Instructions
1. Configure mock server:<br>
   Download Mockoon, click on File-> Open Local Environment, use the file library.json (found in repository), start server

2. Clone the repository:<br>
   git clone -b master https://github.com/luca4/LibraryClient.git

3. Set Mockoon's ip and port
   Edit config.py and set base url that will be used to call mock server. Default is: "http://127.0.0.1:3001"
   
4. Navigate to project directory:<br>
   cd LibraryClient
   
5. Create and activate a virtual environment:<br>
   python -m venv venv<br>
   venv\Scripts\activate

6. Install dependencies:<br>
   pip install -r requirements.txt
   
7. Run the program:<br>
   python main.py


If you want to run API interaction tests:<br>
pytest tests\test_library_client.py


## Documentation
1. New endpoints for Admin:
   - **/books** <br>
   HTTP method: POST<br>
   let's you create a new book once you pass the following json structure: <br>
   {"title": "", "author": "", "is_borrowed": true/false}<br>
     Assumption: the id will be generated from the server and will be returned in the body request
  
   - **/books/:id**<br>
    HTTP method: DELETE<br>
    Deletes the book with the specified ID and returns a 204. If the book is not found, returns a 404
   
   - **/books/:id**<br>
    HTTP method: PUT<br>
    Updates the data of the book with the specified ID and returns a 204. If the book is not found, returns a 404

2. New test user:<br>
   A new user has been created in order to test admin and non-admin scenarios.<br>
   Available users:
   - **admin** username:mario, password:rossi
   - **non-admin** username:carlo, password:bianchi

4. New field for token returned on login:<br>
   I added a field (is_admin) in token returned to client that indicate if logged user is admin or not


     
