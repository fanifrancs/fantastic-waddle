# fantastic-waddle
Basically a Python script that implements an anonymous messaging app. The program interacts with a MongoDB database to store user data and messages. Authentication is handled using bcrypt, a secure password hashing function.

## Setup
You need to have installed
- Python
- MongoDB

[Click here](https://www.mongodb.com/try/download/community) to download and install MongoDB locally if you intend to use it as part of your development environment, or [click here](https://www.mongodb.com/) to setup a cloud database. Setting up the database won't be a problem if you already know what you are doing. Clone this repo onto your machine using
```
git clone https://github.com/fanifrancs/fantastic-waddle.git
```
Navigate to repo directory, open up the terminal and run
```
pip install -r requirements.txt
```
to install dependencies. Make sure MongoDB is running and ready to accept connections. Then run `app.py` to start app and hopefully, everything should work fine.