from flask import Flask, request, jsonify
from database import User, db

# create the extension

# create the app
app = Flask(__name__)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"

# initialize the app with the extension
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/user/login", methods=["GET", "POST"])
def login():
    user_name = request.form.get("user_name", "")
    password = request.form.get("password", "")
    data = login_validation(user_name, password)
    
    return data.data.decode()
    
@app.route("/user/register", methods=["GET", "POST"])
def register():

    # Get form data values
    user_name = request.form.get("user_name", "")
    password = request.form.get("password", "")
    first_name=request.form.get("first_name", "")
    last_name=request.form.get("last_name", "")
    age=request.form.get("age", 0)
    address=request.form.get("address", "")
    phone_number=request.form.get("phone_number", "")
    
    data = resgister_validation(user_name, password, first_name, last_name)

    # Write data into database
    if request.method == "POST":
        user = User(
            user_name=user_name,
            password=password,
            first_name=first_name,
            last_name=last_name,
            age=age,
            address=address,
            phone_number=phone_number
        )
        db.session.add(user)
        db.session.commit()
    
    return data.data.decode()

def resgister_validation(user_name, password, first_name, last_name):
    # User validation
    if  db.session.query(db.exists().where(User.user_name == user_name)).scalar():
        return jsonify({
            "message": "This user name is existed",
            "success": False
        })
    if user_name == "":
        return jsonify({
            "message": "User Name cannot be empty",
            "success": False
        })
    if password == "":
        return jsonify({
            "message": "Password cannot be empty",
            "success": False
        })
    
    if first_name == "":
        return jsonify({
            "message": "First Name cannot be empty",
            "success": False
        })

    if last_name == "":
        return jsonify({
            "message": "Last Name cannot be empty",
            "success": False
        })
      
    if len(user_name) <= 5:
        return jsonify({
            "message": "Length of User Name is not less than 4 characters",
            "success": False
        })
    if len(password) <= 9:
        return jsonify({ 
            "message": "Length of password cannot be less than 8 characters",
            "success": False
        })
    
    return jsonify({
        "message": "Register Successfully",
        "success": True
    })

def login_validation(user_name, password):

    if not db.session.query(db.exists().where(User.user_name == user_name)).scalar():
        return jsonify({
            "message": "User name does not exist. Please check again.",
            "success": False
        })
    
    if db.session.query(db.exists().where(User.user_name == user_name)).scalar() and not db.session.query(db.exists().where(User.password == password)).scalar():
        return jsonify({
            "message": "Your password is wrong. Please check again.",
            "success": False
        })

    if user_name == "":
        return jsonify({
            "message": "User Name cannot be empty. Please check again.",
            "success": False
        })
    if password == "":
        return jsonify({
            "message": "Password cannot be empty. Please check again.",
            "success": False
        })

    if len(user_name) <= 5:
        return jsonify({
            "message": "Length of User Name is not less than 4 characters. Please check again.",
            "success": False
        })
    if len(password) <= 9:
        return jsonify({ 
            "message": "Length of password cannot be less than 8 characters. Please check again.",
            "success": False
        })
    
    return jsonify({
        "message": "Login successfully",
        "success": True
    })

if __name__ == '__main__':
    app.run(debug=True)