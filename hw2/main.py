from flask import Flask, request
from string import ascii_letters
from random import randint


app = Flask(__name__)

class User():

    def __init__(self, name = None, language = None):
        self.name = name
        self.language = language
        self.course = ""
        self.grade = None

    def choose_course(self, course):
        self.course = course 

    def get_grade(self, grade):
        self.grade = grade

user = User()


@app.route("/")
def show_info():
    if not user.name:   # if the user's name is None (the user hasn't logged in)
        return f"""
            <h3>{"Please, log in!"} </h3>
            <form action="/login" method="POST">
            <div>
                <label for="un">Please, enter your name:</label>
                <input name="username" id="un" value="" />
                <label for="ln">Enter the language you are studying:</label>
                <input name="language" id="lg" value="" />
            </div>
                <button>Log in!</button>
            </form>    
    """
    if not user.course:    # if the user hasn't chosen the course
        return f"""<h3>The current user is {user.name}, 
        the language you are going to learn is {user.language}
        <form action="/choose_course" method="POST"> <button>Choose course!</button> </form>"""
    
    if not user.grade:    # if the user hasn't got a grade
        return f"""<h3>The current user is {user.name}, 
            the course you are taking is {user.language} {user.course}.</h3>
            <form action="/grade" method="POST"> <button>Let's discover your grade!</button> </form>"""
    
    # else this:
    return f"""<h3>The current user is {user.name}, 
        the course you are taking is {user.language} {user.course} and your grade is {user.grade}.</h3>"""
    
    


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get('username')
    language = request.form.get('language')
    for char in username:
        if char not in ascii_letters and char != " ":
            return """<h3>Sorry, but the name you entered is invalid!</h3> 
            <a href="/">\nReturn to the HOME page</a>"""
        
    user.name = username
    user.language = language

    return f"""
        <h3>Now you are logged in as {user.name}!</h3>
        </br>
        <h4>Now, you can choose the course you are taking</h4>
    
        <form action="/choose_course" method="POST"> <button>Choose course!</button> </form>
        </br>
        or
        <a href="/">Return to the HOME page</a>
    """


@app.route("/choose_course", methods=["POST"])
def choose_course():
    return f"""
    <h3>Choose the course for {user.language}!</h3>
    <form action="/course_choosed" method="POST">
        <input type="radio" id="basic" name="course" value="Basic">
        <label for="basic">Basic</label><br>
        <input type="radio" id="pro" name="course" value="Pro">
        <label for="pro">Pro</label><br>

        <button>Choose!</button>
    </form>
    """

@app.route("/course_choosed", methods=["POST"]) # I need this page to assign the grade and redirect the user to the main page
def course_ok():
    user.choose_course(request.form.get('course')) 
    return f"""
    <h3>Course is chosen successfully!</h3>
    <a href="/">Return to the HOME page</a>
    """

@app.route("/grade", methods=["POST"])
def grade():
    user.get_grade(randint(1, 100))
    return f"""
    <h3>Your teacher decided that your grade should be {user.grade}!</h3>
    {"Congratulations!" if user.grade >= 60 else "You could do better."}
    <a href="/">Return to the HOME page</a>
    """


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
