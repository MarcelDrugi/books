# Books-API
##### Live: [http://piotrmazurbooks.pythonanywhere.com/](http://piotrmazurbooks.pythonanywhere.com/)
##
# Running the application 
#### To start the app, follow the steps below.
###### 1. Clone repo:
    https://github.com/MarcelDrugi/books
###### 2. Go to project main directory:
    cd books
###### 3. Create virtual environment:
    virtualenv venv 
###### 4. Activate venv:
    source venv/bin/activate
###### 5. Install requirements:
    pip install -r  requirements.txt
###### 6. Create database for the project. <br>You can use any SQL management system, but you need to install it into venv.<br> From requirements.txt you have already installed mySQL. If you want to use it go: 
    mysql -u [your_username] -p
###### 7a. Create  <span style="color:black">.env</span> file in <span style="color:black">/rate/backend/rate/rate</span> (the directory that contains <span style="color:black">settings.py</span> file).<br>
###### 7b. To the <span style="color:black">.env</span>  file enter settings of the database you created and some secret key. <br> For mySQL the file should looks like:
    SECRET_KEY=your_secret_key
    DATABASE_NAME=name_of_created_databas
    DATABASE_USER=username
    DATABASE_PASSWORD=password
###### 8. Go to the project main directory(<span style="color:black">/rate/backend/rate</span>) and make the migration
    python3 managey migrate
###### 9. Create superuser
    python3 manage.py createsuperuser
###### 10. Run the server:
    python3 manage.py runserver
##### The app should be launched at:
    http://127.0.0.1:8000
##### You can also use the live version with a set of users.
    http://piotrmazurbooks.pythonanywhere.com/

## 

