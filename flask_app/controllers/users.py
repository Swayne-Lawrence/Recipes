from flask_app import app
from flask import render_template, request, session,flash, redirect
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
from flask_app.models.recipe import Recipe
bcrypt= Bcrypt(app)

@app.route('/')
def register():
    if 'user_id' in session:
        return redirect('/user_page')
    return render_template("register.html")
@app.route('/reg_form', methods=["POST"])
def reg_form():
    if not User.validate(request.form):
        return redirect('/')
    pw_hash=bcrypt.generate_password_hash(request.form["password"])
    data={
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password":pw_hash

    }
    session["user_id"]=User.save(data)
    return redirect('/user_page')
@app.route('/login_form',methods=["POST"])
def login_form():
    user_db=User.check_email(request.form)
    if (not user_db) or (not bcrypt.check_password_hash(user_db.password,request.form["password"])):
        flash("Invalid email/password")
        return redirect('/')
    session["user_id"]=user_db.id
    return redirect('/user_page')
@app.route('/user_page')
def user_page():
    if not 'user_id' in session:
        return redirect('/')
    data={
        "id":session['user_id']
    }
    user_db=User.get_one_with_recipe(data)
    recipe_db= Recipe.get_all()
    return render_template("user_page.html",user=user_db, recipes=recipe_db)
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')