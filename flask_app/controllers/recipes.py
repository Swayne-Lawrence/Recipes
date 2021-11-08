from flask_app import app
from flask import render_template, redirect,flash,session,request
from flask_app.models.recipe import Recipe
from flask_app.models.user import User

@app.route('/create_recipe')
def create_recipe():
    if not 'user_id' in session:
        return redirect('/')
    return render_template('create_recipe.html')
@app.route('/recipe_form', methods=["POST"])
def recipe_form():
    if not Recipe.validate(request.form):
        return redirect('/create_recipe')
    id=Recipe.save(request.form)
    print(session)
    return redirect(f"/show_recipe/{id}")
@app.route('/show_recipe/<int:id>')
def show_recipe(id):
    if not 'user_id' in session:
        return redirect('/')
    data={
        "id":id
    }
    data_u={
        "id":session['user_id']
    }
    recipe_data=Recipe.get_one(data)
    user_data= User.get_one(data_u)
    return render_template("show_recipe.html", data=recipe_data, user=user_data)
@app.route('/edit_recipe/<int:id>')
def edit_recipe(id):
    if not 'user_id' in session:
        return redirect('/')
    data={"id":id}
    recipe_db=Recipe.get_one(data)
    return render_template("edit_recipe.html",data=recipe_db)
@app.route('/update', methods=['POST'])
def update():
    if not Recipe.validate(request.form):
        return redirect(f'/edit_recipe/{request.form["id"]}')
    Recipe.edit(request.form)
    return redirect(f'/show_recipe/{request.form["id"]}')
@app.route('/delete/<int:id>')
def delete(id):
    data={"id":id}
    Recipe.delete(data)
    return redirect('/user_page')
