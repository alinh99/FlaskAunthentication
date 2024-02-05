from flask import Flask, request, jsonify
from database import User, db, ForgotPassword
from validation import resgister_validation, login_validation, forgot_password_validation
from otp_sending import generate_otp, expire_time

# create the app
app = Flask(__name__)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"

# initialize the app with the extension
db.init_app(app)

with app.app_context():
    db.create_all()


print()
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

        # Write data into database
        if request.method == "POST":
            user = User(
                user_name=user_name,
                password=password,
                first_name=first_name,
                last_name=last_name,
                age=age,
                address=address,
                phone_number=phone_number,
                email=email,
            )
            db.session.add(user)
            db.session.commit()
        data = resgister_validation(user_name, password, first_name, last_name, email)
        return data.json
    except Exception as e:
        return str(e)

@app.route("/user/forgot-password", methods=["GET", "POST"])
def forgot_password():
    email = request.form.get("email", "")
    user_id = db.session.query(User).filter_by(email=email).first()
    if not hasattr(user_id, "id"):
        return jsonify({
            "message": "Email does not exist in our database. Please register your email.",
            "success": False
        })
    user_id = user_id.id
    otp = generate_otp()
    is_confirmed_otp = False
    expired_in = expire_time()

    user_forgot = ForgotPassword(
        user_id=user_id,
        otp=otp,
        is_confirmed_otp=is_confirmed_otp,
        expired_in=expired_in
    )
    db.session.add(user_forgot)
    db.session.commit()
    
    data = forgot_password_validation(email, user_id)
    
    return data.json

if __name__ == '__main__':
    app.run(debug=True)