from os import name
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from werkzeug import datastructures
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt

#Kullanıcı Kayıt FOrmu
class RegisterForm(Form):
    name = StringField("İsim Soyisim:", validators = [validators.Length(min = 4, max = 25)])#Maksimum ve Minimum alanı belirlememiz için length kullandık#
    username = StringField("Kullanıcı Adı:", validators = [validators.Length(min = 5, max = 25)])
    email = StringField("Email Adresi:", validators = [validators.Length(min = 15, max = 65), validators.Email(message="Lütfen geçerli bir mail adresi giriniz")])#Email adresinin gerçek olup lmadığını sorgulayacak
    password = PasswordField("Parola:", validators = [validators.DataRequired(message = "Lütfen bir parola belirleyin"), #PasswordFİeld fonksiyonu sayesinde text olarak değil şifre olarak görünecek
    validators.EqualTo(fieldname = "confirm", message = "Parolanız Uyuşmuyor")]) #confirm ile passwordu kıyaslayı eğer uyuşmuyorsa hata mesajı verecek

    confirm = PasswordField("Parola Doğrula")

app = Flask(__name__)

app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "andmeuser"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app) #Dahil ettiğimiz sınıftan nesne oluşturuyoruz#
@app.route("/")
def index():
    return "AndME'ye hoşgeldiniz"

#kAYIT oL
@app.route("/form", methods = ["GET", "POST"])
def register():
    form = RegisterForm(request.form)

    if request.method == "POST" and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data)
        
        cursor = mysql.connection.cursor()

        sorgu = "Insert into users(name, email, username, password) VALUES(%s,%s,%s,%s)"

        cursor.execute(sorgu,(name,email,username,password))
        mysql.connection.commit()

        cursor.close()

        return redirect(url_for("index"))
    else:
        return render_template("form.html", form = form)


if __name__ ==  "__main__":
    app.run(debug=True)