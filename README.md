# MKR

MKR is the testing server powering Niche, an iot service for tracking your inventories.
It is built in Flask in TDD fashion, following the MVC architecture pattern.

### Installation

MKR requires python 3.6 to run.

After cloning this repository, install the dependencies and start the server.

```sh
$ cd MKR
$ virtualenv env --python=python3.6
$ source env/bin/activate
$ pip install -r requirements.txt
$ python app.py
```


### Development

Want to contribute? Great! 

MKR uses nose2 for testing. Before you start, try running nose2 to confirm all tests pass.

#### Setup
Here are the commands for the initial setup.
```sh
$ cd MKR
$ source env/bin/activate
$ nose2
```

#### Getting Started

There's documentation in the `views` and `models` folders which will be helpful. If you don't know what views, controllers, or models are, it is strongly suggested that you learn about MVC patterns prior to contribution. Here's an article to get you started.


https://developer.chrome.com/apps/app_frameworks


Try starting by grabbing issues with `easy` tags. If you are stuck, feel free to contact one of the contributors for help.


### Contributor

***Mark Jung*** 
email: gujung2022@u.northwestern.edu
github: https://github.com/Mark-Jung

License
----

MIT


****

