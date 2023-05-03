from flask import Flask
from random import randint

app = Flask(__name__)

constant = [1, 2, 3]


@app.route("/")
def show_items():
    '''Shows items of the `constant` list.'''
    
    return f"<h3>Our Items are: {constant}!!!</h3>"


@app.route("/delete_item", methods=["GET", "DELETE"])
def delete_item():
    '''Deletes last item from the `constant` list.'''

    global constant

    try:
        deleted_element = constant.pop()
        return f"<h3>Item {deleted_element} was deleted!\n Now, the list looks like this: {constant}.</h3>"
    except IndexError:
        return "<h3>Sorry, but there are no Items left in the list!</h3>"


@app.route("/add_item", methods=["GET", "POST"])
def add_item():
    '''Adds an item to the `constant` list.'''

    global constant

    new_element = randint(0, 100)
    constant.append(new_element)
    return f"<h3>New Item {new_element} was added!\nNow, the list looks like this: {constant}.<h3\>"



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
