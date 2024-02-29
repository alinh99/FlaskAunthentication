from database import db
from flask import jsonify
from database import User, ForgotPassword
from otp_sending import send_email
from datetime import datetime

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
      
    if len(user_name) < 5:
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
    user = User.query.filter_by(
            user_name=user_name).first()
    if user_name != "" and not db.session.query(db.exists().where(User.user_name == user_name)).scalar():
        return jsonify({
            "message": "User name does not exist. Please check again.",
            "success": False
        })

    if email != "" and not db.session.query(db.exists().where(User.email == email)).scalar():
        return jsonify({
            "message": "Email does not exist. Please check again.",
            "success": False
        })
    
    if user.password != password:
        return jsonify({
            "message": "Your password is wrong. Please check again.",
            "success": False
        })

    if user_name == "" and email == "":
        return jsonify({
            "message": "User Name/Email cannot be empty. Please check again.",
            "success": False
        })
    
    if password == "":
        return jsonify({
            "message": "Password cannot be empty. Please check again.",
            "success": False
        })

    if len(user_name) < 5:
        return jsonify({
            "message": "Length of User Name is not less than 4 characters. Please check again.",
            "success": False
        })
    if len(password) < 8:
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
    
    if not email:
        return jsonify({
            "message": "Email cannot be empty. Please check again",
            "success": False
        })
    
    send_email(email)
    
    return jsonify({
        "message": "The OTP is sent successfully to your email. Please check it.",
        "success": True,
    })

def forgot_password_verification_validation(otp, new_password):
    if otp == "":
        return jsonify({
            "message": "Password cannot be empty. Please check again.",
            "success": False
        })
    
    if new_password == "":
        return jsonify({
            "message": "Password cannot be empty. Please check again.",
            "success": False
        })
    
    if len(new_password) < 8:
        return jsonify({ 
            "message": "Length of password cannot be less than 8 characters. Please check again.",
            "success": False
        })
    
    if not db.session.query(db.exists().where(ForgotPassword.otp == otp)).scalar():
        return jsonify({
            "message": "The OTP is expired or invalid. Please check again.",
            "success": False
        })
    current_time = datetime.now()
    if not db.session.query(db.exists().where(ForgotPassword.expired_in >= current_time)).scalar():
        return jsonify({
            "message": "The OTP is expired or invalid. Please check again.",
            "success": False
        })
    return jsonify({
        "message": "Your password is reset successfully.",
        "success": True
    })