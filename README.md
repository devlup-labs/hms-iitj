# IIT Jodhpur Hospital Management System

<a href="https://devlup-labs.github.io"><img src="https://img.shields.io/badge/Maintained%20under-Winter%20of%20Code%2C%20DevlUp%20Labs-brightgreen"/></a>

# HMS


## Setting up the repository-

### Step 1-
 First clone the repository using :
 ```
 git clone https://github.com/devlup-labs/hms-iitj.git 
 ```

### Step 2-
 Then we need all the tools and software mentioned in the requirments.txt , so install all that required using the following command-
```
 pip install -r requirements.txt
```    

### Step 3-
When we were trying to migrate the files we were facing errors , due to relational files in hc and accounts app, which have been resolved by following steps-

* Clear the database and delete the earlier migrations(if any)

* Then in the models.py of the hc app , comment out the lines which have relation with the accounts.py i.e-
```
 line-21-   doctor = models.ForeignKey(to='accounts.Doctor', on_delete=models.CASCADE, null=True)  
```
  (Line no. may change if so, please update in the readme file)
and also in-
```
   line -51 (doctor = models.ForeignKey(to="accounts.Doctor", on_delete=models.CASCADE,
                               related_name="app_doctor", blank=True, null=True))
```
* Then makemigrations for the hc app, then migrate it too, using-

```
  python manage.py makemigrations hc
  python manage.py migrate hc
```

* Then go to the accounts app and without any change just makemigrations in it then simply migrate.
  ```
  python manage.py makemigrations accounts
  python manage.py migrate accounts
  ```
* Then come back to the hc file and uncomment the commented lines (i.e. 21 and 51) and then again makemigrations 
  
* Now makemigrations for the main app, using-
```
  python manage.py makemigrations main
  python manage.py migrate main
```
* Now migrate the whole file using-
```
 python manage.py migrate
```
### Step 4-
 That's it, our error is resolved , then we can run it locally to verify it using-
```
 python manage.py runserver
```

