Galaxy OJ
=========

Galaxy OJ is an online judge system ready to be deployed on Linux systems.

Requirements
-------
* python3
* postgresql
* redis

Deployment
-------
install `python3` `postgresql` `redis` first
install python modules: command `pip install -r requirements.txt

run server: command `python manager.py runserver --threaded`
launch redis server: command `redis-server`
run judge module: command `python -m judge`


License
-------
Dual license:

* For non-commercial use, the software is licensed under **GPLv3.0**.
* For commercial use, please contact the authors for licensing.

