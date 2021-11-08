from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app.models import recipe


EMAIL_REGEX= re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class User:
    def __init__(self,user_data):
        self.id= user_data["id"]
        self.first_name=user_data["first_name"]
        self.last_name=user_data["last_name"]
        self.email=user_data["email"]
        self.password=user_data["password"]
        self.created_at=user_data["created_at"]
        self.updated_at=user_data["updated_at"]
        self.recipes=[]
    @classmethod
    def save(cls,data):
        query="INSERT INTO users(first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s, %(password)s);"
        return connectToMySQL("recipe_schema").query_db(query,data)
    @classmethod
    def check_email(cls, data):
        query="SELECT * FROM users WHERE email=%(email)s;"
        result=connectToMySQL("recipe_schema").query_db(query,data)
        if len(result)<1:
            return False
        return cls(result[0])
    @classmethod
    def get_one(cls,data):
        query="SELECT * FROM users WHERE id=%(id)s;"
        result=connectToMySQL("recipe_schema").query_db(query,data)
        return cls(result[0])
    @classmethod
    def get_one_with_recipe(cls,data):
        query="SELECT * FROM users LEFT JOIN recipes ON users.id=recipes.user_id WHERE users.id=%(id)s order by recipes.created_at desc;"
        result=connectToMySQL("recipe_schema").query_db(query,data)
        user=cls(result[0])
        for r in result:
            recipe_data={
                "id": r["recipes.id"],
                "name":r["name"],
                "description":r["description"],
                "instructions": r["instructions"],
                "date_made": r["date_made"],
                "under_30_mins": r["under_30_mins"],
                "created_at":r["created_at"],
                "updated_at":r["updated_at"],
                "user_id":r["user_id"]
                }
            user.recipes.append(recipe.Recipe(recipe_data))
        return user
            
        
    @staticmethod
    def validate(user):
        is_valid=True
        query="SELECT* FROM users WHERE email=%(email)s;"
        results=connectToMySQL("recipe_schema").query_db(query,user)
        if not EMAIL_REGEX.match(user["email"]):
            flash("Invalid email")
            is_valid=False
        if len(user["first_name"])<2:
            flash("First name must have atleast 2 characters")
            is_valid=False
        if len(user["last_name"])<2:
            flash("Last name must have atleast 2 characters")
            is_valid=False
        if len(results)>=1:
            flash("email already taken")
            is_valid=False
        if user["password"] != user["confirm"]:
            flash("Passwords don't match")
            is_valid=False
        if not (bool(re.search(r'\d',user["password"]))) or not(re.match(r'\w*[A-Z]\w*',user["password"])):
            flash("password must contain atleast 1 number and 1 uppercase letter")
            is_valid=False

        return is_valid
