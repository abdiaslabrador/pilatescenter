Instrucciones de instalación:
	1- Hacer clone, si no sabes tienes que hacer lo siguiente: vas a alguna carpeta donde quieres que esté el proyecto y escribes desde  tu terminal “git clone https://github.com/abdiaslabrador/pilatescenter.git” eso te descargará el proyecto en una carpeta.

	2- Tienes que tener la versión de python3.8

	3- Crear un entorno virtual con python escribiendo:
              - linux: python3 -m venv virtual
	    - windows: python -m venv virtual
	 y activarlo para instalar los paquetes necesarios. Si no sabes como activarlo puedes buscar por internet "como instalar o activar un entorno virtual".

	4- Instalar lo paquetes del requirement.txt yendo donde está la carpeta descargada desde la terminal ( cd "<nombre del carpeta descargada del git>/pilatescenter/"), luego escribes "pip install -r requirements.txt". Esto instalará todos lo paquetes necesarios para correr el proyecto.

	5- tienes que tener postgresql instalado. Creas una base de datos con el nombre pilatescenter y en el archivo settings que se 	encuentra en "<nombre del carpeta descargada del git>/pilatescenter/pilatescenter/settings.py", en la línea 113 modificas la contraseña y colocas la contraseña que tiene le has colocado a tu postgresql, guardas los cambios.

	6- Una vez hecho esto te posicionas desde la terminal en la dirección "<nombre del carpeta descargada del git>/pilatescenter" y escribes "python manage.py makemigrations", y luego "python manage.py makemigrations". Esto pasará todas las tablas necesarias a la base de datos.

	7- Luego es necesario crear un superusuario, para hacer esto tienes que ir a la carpeta "<nombre del carpeta descargada del git>/pilatescenter/pilatescenter" y escribes "python manage.py createsuperuser". A continuación al escribir esto te pedirá unos datos los cuales tienes que llenar. Estos datos son: username, nombre, apellido, cédula y clave.

	8- Después de hacer esto, escribes "python manage.py runserver", lo cual activará el servidor.

	9- Abrir el navegador y escribir en la barra de tu url "http://127.0.0.1:8000/admin_login/login_admin" o cualquier url que está en settings. Esto de dirigirá el "login" de la página administrador, te logueas escribes el username y el password y entraras al sistema.

Los links de la página los se pueden ver en el archivo urls.py que está en la carpeta "<nombre del carpeta descargada del git>/pilatescenter/pilatescenter/settings.py"


Links del administrador
http://127.0.0.1:8000/admin_login/ login_admin
…/plan/...
…/exercise/...
…/users/...
…/lesson/...
…/history/...

links del lado del usuario
…/user_site/login/...
…/user_site/home/...
…/user_site/lessons/...
…/user_site/profile/...
