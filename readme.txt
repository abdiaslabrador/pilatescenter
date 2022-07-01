Installation instructions:
	1- Clone the project

	2- You have to have the version of python3.8

	3- Create a virtual environment and activate it
        - linux: python3 -m venv virtual
	    - windows: python -m venv virtual	 

	4- Install the packages requirement.txt "pip install -r requirements.txt"

	5- You have to have postgresql installed. Create a database with the name pilates center, in the settings file found in "<nombre del carpeta descargada del git>/pilatescenter/pilatescenter/settings.py", in line 113 modify the password and put the password you have put in your postgresql, save the changes.

	6- Once this is done you position yourself from the terminal in the address "<nombre del carpeta descargada del git>/pilatescenter" and write "python manage.py makemigrations", and then "python manage.py migrate"

	7- The is necesary to create a superuser, to do this go to the direction folder "<nombre del carpeta descargada del git>/pilatescenter/pilatescenter" and write "python manage.py createsuperuser". Next, when writing this, it will ask you for some data which you have to fill in. These data are: username, name, surname, ID and password.

	8- After doing this, you write "python manage.py runserver"

	9- Go to "http://127.0.0.1:8000/admin_login/login_admin" or whatever url is in settings. This will direct you to the "login" admin page, you log in, type in your username and password, and enter the system.
