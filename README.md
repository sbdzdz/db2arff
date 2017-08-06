# AWARE to Weka
This is a part of the [ContextViewer](https://link.springer.com/chapter/10.1007/978-3-319-25591-0_6) project. It generates an [ARFF](http://www.cs.waikato.ac.nz/ml/weka/arff.html) file from data collected using the [AWARE](http://www.awareframework.com) framework.
 
### Configuring the database connection
First, you need to create a config file with connection details. It has to include the host, user, password, and name of your MySQL database. See the `establishConnection()` function in `jsonClasses.py`. By default, this file should be called `connection.conf`.
 
### Labelling
The converter takes care of the labelling, but you have to manually define classes in `config.json`. Several types of contextual data are supported, see `jsonClasses.py` for details.
 
For example, if you want geolocation data to be labeled, you must define at least one area polygon in `config.json`. Every location within that polygon will get an appropriate label and every area outside of it will be labeled as "Other" (see the `Area` class in `jsonClasses.py`).
 
### Convertion
Set the `start` and `end` timestamps and provide a `deviceID` in `main.py`, then run it. This should create an ARFF file called `out.arff`.


