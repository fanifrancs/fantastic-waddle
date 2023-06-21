import pymongo, bcrypt, datetime

logged_in = False
current_user = None
# A variable always holding all user data : ) awkward, I know
users = None

def invalid_username(username):
  username = username.replace(' ', '')
  if len(username) == 0:
    return True

def sanitize_username(username):
    return username.lower().replace(' ', '')

def collect_command():
    command = input('Enter a new command: ')
    execute_command(command)

def login():
    global logged_in, current_user

    if current_user or logged_in:
        print('You are logged in as', current_user)
        collect_command()

    username = str(input('Enter username: '))

    user = users.find_one({'username': username})
    if user is None:
        print('User does not exist in database.')
        login()

    password = str(input('Enter password: '))
    password = password.encode('utf-8')

    user = users.find_one({'username': username})

    if not bcrypt.checkpw(password, user['password']):
        print('Invalid username or password')
        login()

    logged_in = True
    current_user = user['username']
    print('You are logged in as ' , current_user)
    collect_command()

def register():
    if current_user or logged_in:
        print('Please logout first.')
        collect_command()

    username = str(input('Enter username: '))

    if invalid_username(username):
        print('Username is not valid')
        register()

    username = sanitize_username(username)
    print('Your username is ' + username)

    password = str(input('Enter password: '))

    if len(password) < 6:
        print('Password must be at least 6 characters long.')
        password = str(input('Enter password: '))

    password2 = str(input('Confirm password: '))

    if password != password2:
        print('Passwords do not match.')
        register()

    password = password.encode('utf-8')

    if users.find_one({'username': username}) is not None:
        print('A user with the given username is already registered.')
        register()

    # else register user
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password, salt)
    user = {
        'username': username,
        'password': hash,
        'salt': salt,
        'messages': []
    }
    users.insert_one(user)
    print('Successfully registered. You can now login.')
    collect_command()

def message():
    username = str(input('Enter username: '))

    user = users.find_one({'username': username})
    if user is None:
        print('User does not exist in database.')
        collect_command()
        
    text = str(input('Enter message: '))
    message = {
        'date': datetime.datetime.now(),
        'message': text
    }

    user['messages'].append(message)

    users.update_one({'_id': user['_id']}, {'$set': user})
    print('Message sent!')
    collect_command()

def messages():
    if not (current_user or logged_in):
        print('Please login first')
        collect_command()
    user = users.find_one({'username': current_user})

    for message in user['messages']:
        print(f"{message['date']}: {message['message']}")
    
    collect_command()

def contact():
    print('Send an email to fanikufran6@gmail.com')  

def logout():
    global current_user, logged_in
    if current_user or logged_in:
        current_user = None
        logged_in = None
        print('You are logged out')
    else:
        print('You are not logged in')
    collect_command()

def execute_command(command):
    command = command.lower()
    if command == 'login':
        login()
    elif command == 'register':
        register()
    elif command == 'message':
        message()
    elif command == 'messages':
        messages()
    elif command == 'contact':
        contact()
    elif command == 'logout':
        logout()
    else:
        print('Invalid command')
        collect_command()

def connect_db():
    try:
        global users
        client = pymongo.MongoClient('mongodb://localhost:27017')
        db = client['py_anonimaze']
        users = db['users']
    except Exception as e:
        print(e)

connect_db()
collect_command()
