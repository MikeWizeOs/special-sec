from flask import Flask, request, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import pyotp
from flask_jwt_extended import JWTManager, create_access_token, decode_token
import datetime
# from flask_mail import Mail, Message  # Комментарий для отправки по почте

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "jwt_secret_key"

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Настройки для отправки почты (закомментировано)
# app.config["MAIL_SERVER"] = "smtp.yourmailserver.com"  # ваш SMTP сервер
# app.config["MAIL_PORT"] = 587
# app.config["MAIL_USE_TLS"] = True
# app.config["MAIL_USERNAME"] = "your_email@example.com"
# app.config["MAIL_PASSWORD"] = "your_password"
# mail = Mail(app)

# Модель пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    totp_secret = db.Column(db.String(32), nullable=False)

# Создание базы данных
with app.app_context():
    db.create_all()

# Главная страница
@app.route("/")
def index():
    return render_template("index.html")

# Страница регистрации
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Проверяем, существует ли пользователь
        if User.query.filter_by(username=username).first():
            return "Пользователь уже существует!"

        # Генерация секретного ключа для 2FA
        totp_secret = pyotp.random_base32()

        # Сохранение пользователя в базе данных
        new_user = User(username=username, password=password, totp_secret=totp_secret)
        db.session.add(new_user)
        db.session.commit()

        return f"Регистрация успешна! Ваш секретный ключ для 2FA: {totp_secret}"

    return render_template("register.html")

# Страница входа
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Проверяем логин и пароль
        user = User.query.filter_by(username=username, password=password).first()
        if not user:
            return "Неверное имя пользователя или пароль!"

        # Сохраняем пользователя в сессии для дальнейшего использования
        session["username"] = username

        # Генерация JWT токена, который действителен 60 секунд
        access_token = create_access_token(identity=username, expires_delta=datetime.timedelta(seconds=60))
        session["token"] = access_token

        # Закомментированный код для отправки токена по почте
        # msg = Message("Ваш токен авторизации", sender="your_email@example.com", recipients=[user.email])
        # msg.body = f"Ваш токен: {access_token}"
        # mail.send(msg)

        # Открываем новую вкладку для токена и перенаправляем основное окно на ввод токена
        return redirect(url_for("token_input"))

    return render_template("login.html")

# Страница для ввода токена (основное окно)
@app.route("/token_input", methods=["GET", "POST"])
def token_input():
    if request.method == "POST":
        token = request.form["token"]

        # Проверка токена
        try:
            decode_token(token)
            return "Токен действителен!"
        except:
            return "Токен недействителен или истек!"

    return render_template("token_input.html")

# Страница с токеном (новая вкладка)
@app.route("/token", methods=["GET"])
def token():
    if "token" not in session:
        return redirect(url_for("login"))

    token = session["token"]

    # Проверка, истёк ли токен
    try:
        decode_token(token)
    except:
        return "Токен истёк! Пожалуйста, войдите снова."

    return render_template("token.html", token=token)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)