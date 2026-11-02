from flask import Flask
app = Flask(__name__)


@app.route("/")
def index():
    return ' hello CART '


@app.route("/about")
def about():
    return '<h1 style = "color:purple"> About cart 351!</h1>'

@app.route("user/<name>")
def user_profile(name):
    # we will use templates sooN!
    return f"<h2> This is <span style = 'color:orange'>{name}'s</span> profile page" 


@app.route("catGen/<cat_name>")
def cat_generator(cat_name):
    if(cat_name[-1].lower() != "y"):
        return f"{cat_name}y"
    return f"{cat_name}iful"

app.run()