from database import db
from flask import jsonify
from database import User
from otp_sending import send_email, otp

def resgister_validation(user_name, password, first_name, last_name, email):
    # User validation
    if db.session.query(db.exists().where(User.user_name == user_name)).scalar():
        return jsonify({
            "message": "This User Name is existed",
            "success": False
        })

    if db.session.query(db.exists().where(User.email == email)).scalar():
        return jsonify({
            "message": "This Email is existed",
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
    
    if email == "":
        return jsonify({
            "message": "Email cannot be empty",
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
    
    if len(password) < 8:
        return jsonify({ 
            "message": "Length of password cannot be less than 8 characters",
            "success": False
        })
    
    return jsonify({
        "message": "Register Successfully",
        "success": True
    })

def login_validation(user_name, password, email):
    # User validation
    if not db.session.query(db.exists().where(User.user_name == user_name)).scalar():
        return jsonify({
            "message": "User name does not exist. Please check again.",
            "success": False
        })

    if not db.session.query(db.exists().where(User.email == email)).scalar():
        return jsonify({
            "message": "Email does not exist. Please check again.",
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

def forgot_password_validation(email, user_id):
    if not user_id:
        return jsonify({
            "message": "Email does not exist. Please check again.",
            "success": False
        })
    if not db.session.query(db.exists().where(User.id == user_id)).scalar():
        return jsonify({
            "message": "Email does not exist. Please check again.",
            "success": False
        })
    if not db.session.query(db.exists().where(User.email == email)).scalar():
        return jsonify({
            "message": "Email does not exist. Please check again.",
            "success": False
        })
    if not email:
        return jsonify({
            "message": "Email cannot be empty. Please check again",
            "success": False
        })
    send_email()
    return jsonify({
        "message": "The OTP is sent successfully to your email. Please check it.",
        "success": True,
    })