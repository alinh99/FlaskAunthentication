from flask import Flask, request, jsonify
from database import User, db, ForgotPassword
from validation import resgister_validation, login_validation, forgot_password_validation, forgot_password_verification_validation
from otp_sending import otp, expired_in
import hashlib

# create the app
app = Flask(__name__)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

# initialize the app with the extension
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/user/login", methods=["GET", "POST"])
def login():
    try:
        user_name = request.form.get("user_name", "")
        password = request.form.get("password", "")
        email = request.form.get("email", "")

        data = login_validation(user_name, password, email)
        
        return data.json
    except Exception as e:
        return str(e)
    
@app.route("/user/register", methods=["GET", "POST"])
def register():
    try:
        # Get form data values
        user_name = request.form.get("user_name", "")
        password = request.form.get("password", "")
        first_name=request.form.get("first_name", "")
        last_name=request.form.get("last_name", "")
        age=request.form.get("age", 0)
        address=request.form.get("address", "")
        phone_number=request.form.get("phone_number", "")
        email = request.form.get("email", "")

        data = resgister_validation(user_name, password, first_name, last_name, email, phone_number, address, age)
        
        # Write data into database
        if request.method == "POST":
            user = User(
                user_name=user_name,
                password=hashlib.sha256(password.encode('utf-8')).hexdigest(),
                first_name=first_name,
                last_name=last_name,
                age=age,
                address=address,
                phone_number=phone_number,
                email=email,
            )

            if data.json["success"] != False:
                db.session.add(user)
                db.session.commit()
                
        return data.json
    except Exception as e:
        return str(e)

@app.route("/user/forgot-password", methods=["GET", "POST"])
def forgot_password():
    try:
        email = request.form.get("email", "")
        user = db.session.query(User).filter_by(email=email).first()
        
        if user is None:
            return jsonify({
                "message": "Email does not exist in our database. Please register your email.",
                "success": False
            })

        user_id = user.id
        is_confirmed_otp = False
        user_forgot = db.session.query(ForgotPassword).filter_by(user_id=user_id).first()
        data = forgot_password_validation(email, user_id)

        if user_forgot:
            user_forgot.otp = otp
            user_forgot.expired_in = expired_in
        else:
            user_forgot = ForgotPassword(
                user_id=user_id,
                otp=otp,
                is_confirmed_otp=is_confirmed_otp,
                expired_in=expired_in
            )
            if data.json["success"] != False:
                db.session.add(user_forgot)
        
        db.session.commit()
        
        return data.json
    except Exception as e:
        return str(e)

@app.route("/user/reset-password", methods=["GET", "POST"])
def reset_password():
    try:
        otp = int(request.form.get("otp", ""))
        new_password = request.form.get("password", "")
        
        user_forgot = db.session.query(ForgotPassword).filter_by(otp=otp).first()
        
        data = forgot_password_verification_validation(otp, new_password)
        
        if user_forgot is None:
            return jsonify({
                "message": "The OTP is expired or invalid. Please check again.",
                "success": False
            })
        
        if data.json["success"] != False:
            user_forgot.user.password = hashlib.sha256(new_password.encode("utf-8")).hexdigest()
            user_forgot.is_confirmed_otp = True
            
        db.session.delete(user_forgot)
        db.session.commit()
        
        return data.json

    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)