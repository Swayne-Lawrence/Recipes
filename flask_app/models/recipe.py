from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    def __init__(self,recipe_data):
        self.id=recipe_data["id"]
        self.name=recipe_data["name"]
        self.description=recipe_data["description"]
        self.instructions=recipe_data["instructions"]
        self.date_made=recipe_data["date_made"]
        self.under_30_mins=recipe_data["under_30_mins"]
        self.created_at=recipe_data["created_at"]
        self.updated_at=recipe_data["updated_at"]
        self.user_id=recipe_data["user_id"]
    @classmethod
    def save(cls,data):
        query="INSERT INTO recipes(name,description,instructions,date_made,under_30_mins,user_id)VALUES(%(name)s,%(description)s,%(instructions)s,%(date_made)s,%(under_30_mins)s,%(user_id)s);"
        return connectToMySQL("recipe_schema").query_db(query,data)
    @classmethod
    def get_one(cls,data):
        query="SELECT * FROM recipes WHERE id=%(id)s;"
        result=connectToMySQL("recipe_schema").query_db(query,data)
        return  cls(result[0])
    @classmethod
    def get_all(cls):
        query="SELECT * FROM recipes;"
        results=connectToMySQL("recipe_schema").query_db(query)
        recipes=[]
        for r in results:
            recipes.append(cls(r))
        return recipes
    @classmethod
    def delete(cls,data):
        query="DELETE FROM recipes WHERE id=%(id)s;"
        return connectToMySQL("recipe_schema").query_db(query,data)
    @classmethod
    def edit(cls,data):
        query="UPDATE recipes SET name=%(name)s, description=%(description)s,instructions=%(instructions)s,date_made=%(date_made)s,under_30_mins=%(under_30_mins)s WHERE id=%(id)s"
        return connectToMySQL("recipe_schema").query_db(query,data)
    @staticmethod
    def validate(recipe):
        is_valid=True
        if len(recipe["name"])<3:
            flash("Name too short")
            is_valid=False
        if len(recipe["description"])<3:
            flash("Enter a description")
            is_valid=False
        if len(recipe["instructions"])<3:
            flash("Instructions must be more the 3 charaters")
            is_valid=False
        if len(recipe["date_made"])<3:
            flash("Enter a Date")
            is_valid=False
        if len(recipe["under_30_mins"])<1:
            flash("Select Yes/No")
            is_valid=False
        
        return is_valid