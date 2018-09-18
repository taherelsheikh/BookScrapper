# BookScrapper 

An application and database solution that scrapes book data from ten websites. The app’s output is a final merged dataset from all the ten sources that is then pushed to a MySQL database.

### Getting started

* Download and install Python 2.7. Required packages will be installed from the **requirements.txt** file - ensure pip is installed as well
* Using Homebrew download **Chromedriver**
* Make sure you have **Google Chrome** downloaded
* Create a MySQL database with a default collation of **utf8mb4_unicode_ci**
* Create a table in the new MySQL database using the code in the **create_sql_table.txt** file (run in database from MySQL workbench or similar program)


### Installing packages

* After downloading Python go to the project’s directory from the terminal (eg. $ ~/bookscrapper)
* Run the following code in the terminal:

```
$ pip install -r requirements.txt
```

### Downloading ChromeDriver
* Make sure to download and install Homebrew first (https://brew.sh/)
* Run the following code in the terminal

```
$ brew install chromedriver
```

### Bookbrowse credentials
* Put your bookbrowse credentials in the **bookbrowse_credentials.json** file


### Connecting the Database

* Put your MySQL database credential/connection info in the **sql_credentials.json** file
 * Host ex *localhost:3036*
 * User ex *root*
 * Password ex *SQLpassword*
 * Database ex *Books*


### Running the App

* From the terminal go to **spiders** directory found inside the app

```
$ cd spiders/
```

* Run the following code in the terminal

```
$ python MAIN.py
```

* Code will run to completion at which point MySQL database Books table populated with scraped data
