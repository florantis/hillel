from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from random import randint
from .models import WeekDay, Note
# Since I still don't know how to operate with DBs properly, I use this class as a temporal solution
class Student():
    def __init__(self, name = None, language = None):
        self.name = name
        self.language = language
        self.course = ""
        self.grade = None

    def set_course(self, course):
        self.course = course 

    def get_grade(self, grade):
        self.grade = grade
user = Student()


# Create your views here.
def index(request):
    if not user.name:   # if the user's name is None (the user hasn't logged in)
        return HttpResponse(f"""
            <div class="header">    
                <h1>Bibell School</h1>
                <p><a href="/">Home page</a>- - - -<a href="/my_week/">Diary</a>
            <hr>
            </div>

            <h3>{"Please, log in!"} </h3>
            <form action="login/" method="POST">
            <div>
                <label for="un">Please, enter your name:</label>
                <input name="username" id="un" value="" />
                <label for="ln">Enter the language you are studying:</label>
                <input name="language" id="lg" value="" />
            </div>
                <button>Log in!</button>
            </form>""")
    if not user.course:    # if the user hasn't chosen the course
        return HttpResponse(f"""<h3>The current user is {user.name}, 
            the language you are going to learn is {user.language}
            <form action="choose_course/" method="POST"> <button>Choose course!</button> </form>""")
    if not user.grade:    # if the user hasn't got a grade
        return HttpResponse(f"""<h3>The current user is {user.name}, 
            the course you are taking is {user.language} {user.course}.</h3>
            <form action="grade/" method="POST"> <button>Let's discover your grade!</button> </form>""")
    # else this:
    return HttpResponse(f"""<h3>The current user is {user.name}, 
        the course you are taking is {user.language} {user.course} and your grade is {user.grade}.</h3>""")


def login(request):
    from string import ascii_letters

    if not request.POST:
        return render(request, 'reg_log/please_login.html')
    
    username = request.POST.get('username').title() # Make it so the names users enter are CAPSed right 
    language = request.POST.get('language')
    
    # Validating username
    if username == "":
        return HttpResponse("""<h3>Sorry, but the name you entered is invalid!</h3> 
             <a href="/">\nReturn to the HOME page</a>""")
    for char in username:
        if char not in ascii_letters and char != " ":
            return HttpResponse("""<h3>Sorry, but the name you entered is invalid!</h3> 
             <a href="/">\nReturn to the HOME page</a>""")
    # Validating language
    if not language.isascii() or language == "":
        return HttpResponse("""<h3>Sorry, but the language you entered is invalid!</h3>  
          <a href="/">\nReturn to the HOME page</a>""")
        
    user.name = username
    user.language = language

    return HttpResponse(f"""
        <h3>Now you are logged in as {user.name}!</h3>
        </br>
        <h4>Now, you can choose the course you are taking</h4>
    
        <form action="/choose_course/" method="POST"> <button>Choose course!</button> </form>
        </br>
        or
        <a href="/">Return to the HOME page</a>
    """)


def choose_course(request):
    if not user.name:   # if the user's name is None (the user hasn't logged in)
        return HttpResponse("""<h3>Please, login from the HOME page!</h3>  
            <a href="/">\nReturn to the HOME page</a>""")
    
    return HttpResponse(f"""
    <h3>Choose the course for {user.language}!</h3>
    <form action="done/" method="POST">
        <input type="radio" id="basic" name="course" value="Basic">
        <label for="basic">Basic</label><br>
        <input type="radio" id="pro" name="course" value="Pro">
        <label for="pro">Pro</label><br>
        <button>Choose!</button>
    </form>
    """)


# I need this view to assign the grade and redirect the user to the main page
def course_ok(request):
    if not user.name:   # if the user's name is None (the user hasn't logged in)
        return render(request, 'reg_log/please_login.html')
    
    user.set_course(request.POST.get('course')) 
    return HttpResponse(f"""
    <h3>Course is chosen successfully!</h3>
    <a href="/">Return to the HOME page</a>
    """)


def grade(request):
    if not user.name:   # if the user's name is None (the user hasn't logged in)
        return render(request, 'reg_log/please_login.html')

    user.get_grade(randint(1, 100))
    return HttpResponse(f"""
    <h3>Your teacher decided that your grade should be {user.grade}!</h3>
    {"Congratulations!" if user.grade >= 60 else "You could do better."}
    <a href="/">Return to the HOME page</a>
    """)
  

def show_week(request):
    """Shows every WeekDay object in a HTML list."""
    return render(request, 'diary/week.html', {"week": WeekDay.objects.all()})

def show_day(request, day):
    """Shows every Note for the day `day` if it exists."""
    try:
        day = WeekDay.objects.get(pk=day)
    except ObjectDoesNotExist:
        raise Http404  # I wanted to raise 404 error not through a shortcut to get better understanding how it works
    return render(request, 'diary/day.html', {'day': day})

def show_note(request, day, note_id):
    """Shows specific note that with ID `note_id`."""
    note = get_object_or_404(Note, pk=note_id) # But here I use a shortcut
    return render(request, 'diary/note.html', {'note': note})
