Use the app here [TODO List](https://todo-list-zameel.herokuapp.com).

![This is the logo](/static/icon.ico)

# TODO List:
#### Video Demo:  https://youtu.be/N7bTTossE7E
#### Description:
This is the final project of CS50.
It's a simple TODO List maker that sorts the tasks, shows the history of tasks, shows the due date and more over it simplifies our daily task scheduling.
TODO list is something that every student wants.
As a grad student, I cannot live a day without using the TODO list.
So I thought of making a TODO list I along with anyone in the world can use for their daily task listing.
The web app is entirely made using python, JS, HTML, css and Flask. It was such a great experience making this all by myself!
The web app has a register section where you can register yourself for an account and a login page to log in to your account.
You can add your tasks in the Add task section. The task can be viewed in the main page which can be seen in 3 colours.
Red: High priority, Orange: Medium priority, Green: Least priority. A done button can be seen in the task cards which by pressing sets the task as done.
All the tasks and its details can be viewed in the history section of the page. All possible errors are handled after user testing.

There are 7 page templates inside the templates folder excluding the layout file. 'add.html' is the page that makes the add task option work. 'apology.html' handles the errors in the page.
'histoy.html' is for the history section that shows all the tasks that had been done and currently doing.
'index.html' is the welcoming page and 'login.html' and 'register.html' helps in making and accessing the accounts. 'main.html' is the page that can be seen as soon as you log in to the app.
It shows the task cards in it.

In the static folder, it has the basic css styles file. There is no much styles given as it is mostly derived from the bootstrap styles. An icon is also put inside the static folder that represents the todo icon.

Apart from these, application.py is where the magic takes place. It contains all the python and flask codes. Separate def for each of the routes are inside it.
Some routes are required with login so that foreigners don't access the files inside. The login check, error handling and some other functions are inside the helpers.py file.
The requirements.txt file has names of the libraries that are to be imported so that the application works.

todolist.db is the database that has all the data's inside this app. It handles the user details and the tasks that each user has.

This web app is entirely made using
- Python
- Flask
- HTML, CSS
- JS

> If any errors or problems seen in the app, kindly ping me at [Linkedin](https://www.linkedin.com/in/zameelhassan/).

*I'm so proud I made this all alone!*
***Made with 🖤 by Zameel Hassan***
