# YouFace README

YouFace is a mock social media platform. Originally designed as an assignment
for CS 1410, it has been simplified and modernized for CS 2450. This repository
houses a rough implementation of the completed version of the original
assignment, yet still provides only minimal functionality. Your group will take
this social media baseline and make it your own. Consider yourselves a small
startup with a new and unique take on the social media market.

This README is far from comprehensive. The entire project will provide you an
opportunity to have the experience of jumping into an existing code base, having
to learn about it as you go (lack of documentation and disorganized layouts are
commonplace in the industry). With that in mind, I still want to help as much as
I can. As you go about working on the project, please let me know of any
specific areas where I could improve the documentation.

## Getting Started

### Installing Dependencies

The required dependencies are listed in `requirements.txt`. With `pip`, they can be
easily installed in one command:

`pip3 install -r requirements.txt`

### Running the Server

The server main is found in `youface.py`. It requires Python 3 and can be run
with the following command:

`python3 youface.py`

By default, the server can be accessed at `http://127.0.0.1:5005`

Press `CTRL+C` to stop the server

## Development

### File Tree

```
.
├── db
│   ├── posts.py
│   └── users.py
├── db.json
├── handlers
│   ├── copy.py
│   ├── friends.py
│   ├── login.py
│   ├── posts.py
├── README.md
├── requirements.txt
├── static
│   ├── bootstrap.min.css
│   └── youface.css
├── templates
│   ├── base.html
│   ├── feed.html
│   ├── friend.html
│   ├── login.html
│   └── nav.html
├── tests
│   └── test_login.py
└── youface.py
```

### External Libraries

The following external libraries were used to help make this project. Please
refer to their documentation frequently. It will be more useful to you to check
with the documentation before you search Google/StackOverflow. In fact, the more
you practice referencing official documentation, the quicker you'll get at it.
You might eventually find yourself not relying on StackOverflow near as much as
before. I'll include some links with helpful tutorials as well.

- [Flask](https://palletsprojects.com/p/flask/)
    - https://pythonhow.com/flask-navigation-menu/
    - https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
    - https://blog.pythonanywhere.com/121/
- [jinja](https://jinja.palletsprojects.com/en/2.11.x/)
    - https://jinja.palletsprojects.com/en/2.11.x/tricks/
    - https://realpython.com/primer-on-jinja-templating/
- [TinyDB](https://pypi.org/project/tinydb/)
    - https://tinydb.readthedocs.io/en/latest/
    - See examples in dbhelpers.py
- [timeago](https://pypi.org/project/timeago/)

### Database Documents (Objects)

Users

| Key | Type | Description |
| --- | ------ | --- |
| id | int | The user's unique identifier. |
| username | str | The user's unique username. |
| password | str | The user's password. |
| friends | []int | A list of user ids for this user's friends. |

Posts

| Key | Type | Description |
| --- | ------ | --- |
| nsfw | bool | Is the post NSFW? |
| id | int | The post's unique identifier. |
| user | str | The username of the post creator. |
| text | str | The text of the post. |
| time | float | The timestamp for when the post was created. |

### Running the Tests

Run all the tests in the `tests` directory:

```
python3 -m unittest discover -vs tests
```

Run a specific test file (e.g., `tests/test_login.py`:

```
python3 -m unittest tests.test_login
```
