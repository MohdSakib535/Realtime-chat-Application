# Real-Time Chat Application

A real-time chat application built with Django and Django Channels. This application includes public chat rooms for group chats and private one-to-one chats between friends. The application is powered by WebSockets with Redis for the channel layer, allowing seamless real-time communication.

## Features

- **Public Chat Rooms**: 
  - Authenticated users can choose a room to chat in.
  - Real-time messaging between multiple users in a public room.

- **Private One-to-One Chat**:
  - Search for friends by their user IDs.
  - Start a private chat if both users are friends.
  - Real-time messaging between two users in a personal room.

- **Friendship Management**:
  - Users can search for each other by their unique IDs and initiate private chats if they are friends.

- **Redis for Channels Layer**:
  - Redis is used as the backend for Django Channels, enabling real-time WebSocket communication.

## Prerequisites

Make sure you have the following installed:
- Python 3.10+
- Redis server (for the Django Channels layer)
- PostgreSQL or SQLite (or another compatible database)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/chat-application.git
   cd chat-application
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the dependencies:**
   Install the required Python packages using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your database:**
   - If you're using PostgreSQL, configure your database settings in `settings.py`. For example:
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.postgresql',
             'NAME': 'your-db-name',
             'USER': 'your-db-user',
             'PASSWORD': 'your-db-password',
             'HOST': 'localhost',
             'PORT': '5432',
         }
     }
     ```

   - If you're using SQLite (the default), no changes are needed.

5. **Set up the database:**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (admin):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Redis server:**
   Make sure Redis is installed and running on your system. You can start Redis using the following command (depending on your system):
   ```bash
   redis-server
   ```

8. **Run the Django development server:**
   ```bash
   python manage.py runserver
   ```

9. **Run Daphne (ASGI server for Django Channels):**
   In a separate terminal window, run:
   ```bash
   daphne -b 0.0.0.0 -p 8001 ChatApplication.asgi:application
   ```

10. **Access the application:**
    - Open a browser and navigate to: `http://localhost:8000`

## Usage

### Public Chat Rooms
1. Register or log in as an authenticated user.
2. Navigate to the public chat rooms page.
3. Choose a room from the available list or create a new one.
4. Start chatting in real-time with other users.

### Private One-to-One Chat
1. Use the search feature to find friends by their user IDs.
2. If the user is a friend, you can initiate a private chat.
3. Exchange messages in real-time with your friend.

## Project Structure

```
├── ChatApplication/              # Main Django project directory
│   ├── asgi.py                   # ASGI configuration for Django Channels
│   ├── settings.py               # Django settings
│   ├── urls.py                   # URL routing
│   ├── wsgi.py                   # WSGI configuration
├── chatenv/                      # Virtual environment directory
├── globalchat/                   # Chat application for public chat rooms
│   ├── apps.py                   # App configuration
│   ├── consumers.py              # WebSocket consumers for real-time messages
│   ├── models.py                 # Models for PublicChatRoom and chat messages
│   ├── routing.py                # WebSocket routing
│   ├── views.py                  # Views for public chat handling
│   ├── templates/                # HTML templates for chat UI
│       ├── public_chat.html      # Public chat room template
│       ├── private_chats.html    # Private one-to-one chat template
│       ├── home.html             # Homepage template
│       ├── userProfile.html      # User profile template
│       ├── requested_list.html   # Friends list and friend requests
├── useraccount/                  # User authentication and friend management
│   └── models.py                 # CustomUser and friend relationships
├── static/                       # Static files (CSS, JS, images)
│   └── (static files, if any)
├── media/                        # Media files (profile images, etc.)
│   ├── profile_images/           # Profile image uploads
├── db.sqlite3                    # SQLite database (or you can use PostgreSQL)
├── manage.py                     # Django management script
├── requirements.txt              # Python dependencies
```

## WebSocket Setup

The application uses **Django Channels** with **Redis** as the channel layer backend. WebSocket connections are managed in real-time, and messages are broadcasted instantly to connected users.

### Channels and Redis Configuration:

Make sure your `settings.py` includes the following configuration for Django Channels and Redis:

```python
# Channels setup
ASGI_APPLICATION = 'ChatApplication.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
```

## Technologies Used

- **Django**: For the backend and user authentication.
- **Django Channels**: For handling WebSocket connections.
- **Redis**: As the channel layer for real-time communication.
- **PostgreSQL/SQLite**: As the database for storing users, messages, and rooms.

## Dependencies

Below are the dependencies listed in `requirements.txt`:

```
asgiref==3.8.1
attrs==24.2.0
autobahn==24.4.2
Automat==24.8.1
cffi==1.17.1
channels==4.1.0
channels-redis==4.2.0
constantly==23.10.4
cryptography==43.0.1
daphne==4.1.2
Django==5.1.1
hyperlink==21.0.0
idna==3.10
incremental==24.7.2
msgpack==1.1.0
pillow==11.0.0
pyasn1==0.6.1
pyasn1_modules==0.4.1
pycparser==2.22
pyOpenSSL==24.2.1
redis==5.1.0
service-identity==24.1.0
setuptools==75.1.0
sqlparse==0.5.1
Twisted==24.7.0
txaio==23.1.1
typing_extensions==4.12.2
tzdata==2024.2
zope.interface==7.0.3
```

## Download

You can download the project [here](https://github.com/your-username/chat-application/archive/refs/heads/main.zip).

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
