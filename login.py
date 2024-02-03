from flask import request, jsonify

def login():
    user_name = request.form.get("user_name", "")
    password = request.form.get("password", "")
    if user_name == "" :
        return jsonify({
            "message": "User Name cannot be empty",
            "success": False
        })
    elif password == "":
        return jsonify({
            "message": "Password cannot be empty",
            "success": False
        })
    elif len(user_name) <= 5:
        return jsonify({
            "message": "Length of User Name is not less than 4 characters",
            "success": False
        })
    elif len(password) <= 9:
        return jsonify({ 
            "message": "Length of password cannot be less than 8 characters",
            "success": False
        })
    return jsonify({
        "message": "Login successfully",
        "success": True 
    })