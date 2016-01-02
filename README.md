Galaxy OJ
=========

Galaxy OJ is an online judge system ready to be deployed on Linux systems.

Requirements
-------
* python3
* postgresql
* redis


Deployment
----------
First install python dependencies (using a `virtualenv` is recommended):

### Python Dependencies

```
pip install -r requirements.txt
```

### Config the Web Server
Then, you probably should set the following environment variables
for your web server or change the values in `server/config.py`:

```
# the configuration set you want to use. Always use 'PRODUCTION' in production environment
CONFIG_NAME
# database uri for sqlalchemy (The app is only tested with PostgreSQL).
DATABASE_URI
# secret key for the app. You probably want a random one (maybe using 'openssl rand').
SECRET_KEY
# path to the data folder used by the server.
DATA_FOLDER
```


### Create the Directories
Replace `$DATA_FOLDER` to the path you specified in your configuration:

```bash
$ mkdir -p $DATA_FOLDER/{submissions, testcases, uploaded_images}
```


### Create the Database
After these, you should create the database:

```bash
# here take postgresql as an example. Note that the database name should be the
#   same as specified in DATABASE_URI
$ createdb galaxyoj
```

And then create the tables:

```bash
# use migration scripts
$ python manager.py db upgrade
# or import server.db and call 'db.create_all()'
```

### Create a Root User
Currently the OJ has three types of users: *normal*, *admin*, *root*.
You will need a root user to manage user privileges.

Launch a python shell in app context:

```bash
$ python manager.py shell
```

Run the following in that shell:

```python
u = User()
u.login_name = 'root'
u.password = 'whatever'
u.email = 'whatever@example.com'
u.privilege_level = 10
db.session.add(u)
db.session.commit()
```

### Run Server For Development
For a development environment, you will want to just run a `redis` server,
a `judge` worker, and the web server, all on your local machine.

#### Redis Server
Example (assuming default connection):

```bash
$ redis-server
```

#### Judge Worker

```bash
$ python -m judge
```

#### Web Server

```bash
$ python manager.py runserver --threaded
```


### Run Server For Production
The procedures for running a server for production use is similar to
that for development use, except that you should not use the web server
of `flask`, but make use of real web servers such as `uwsgi`.

Since the environments are different and we won't and can't cover all cases,
this section is deliberately left blank.

In the future, we may employ `docker` to provide easy production set up.


License
-------
Dual license:

* For non-commercial use, the software is licensed under **GPLv3.0**.
* For commercial use, please contact the authors for licensing.

