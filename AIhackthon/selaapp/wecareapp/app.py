from flask import Flask, render_template, request, redirect, jsonify, \
    url_for, flash, session, send_file # المكتبات اللي نحتاجها 

from flask_sqlalchemy import SQLAlchemy #مكتبة  مسؤولة عن الداتا بيس 
from forms import AddComplaint, AddQuery, AddSuggestion, RegisterForm, LoginForm #نسوي فيها الفورمز 
from flask_bcrypt import Bcrypt #نسوي تشفير للباسوورد 
from flask_login import LoginManager, UserMixin, login_user #مسؤولة عن الدخول و الخروج و ما الى ذلك
import os
from werkzeug.utils import secure_filename #نربط فيها الملفات 


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__) # هنا الconnect with DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' # من خلال كتابة الباث تبع الداتابيس
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d' # أي رقم عشوائي فقط عشان نسوي السيكيور للداتابيس


db = SQLAlchemy(app) # مكتبة تعرف الداتابيس
bcrypt = Bcrypt(app)  #للتشفير
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin): #  عشان نصنّف اعمدة الداتابيس من خلال الاسم و النوع و عدد الخانات اللي حندخلها
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30) ,unique=True, nullable=False)
    email_address = db.Column(db.String(length=50),unique=True ,
                              nullable=False)
    password_hash = db.Column(db.String(length=60), nullable=False)
    department = db.Column(db.String(length=100), nullable=False)
    isapproved = db.Column(db.Integer(), nullable=False, default=1)
    phone = db.Column(db.String(length=100), nullable=False)


class Complaint(db.Model, UserMixin): # جدول الشكاوى 
    id = db.Column(db.Integer(), primary_key=True) 
    username = db.Column(db.String(length=30), nullable=False)
    description = db.Column(db.String(length=200),
                            nullable=False)
    phone = db.Column(db.String(length=100), nullable=False)


class Query(db.Model, UserMixin): #جدول الاستفسارات 
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False)
    description = db.Column(db.String(length=200),
                            nullable=False)
    phone = db.Column(db.String(length=100), nullable=False)


class Suggestion(db.Model, UserMixin): #جدول الاقتراحات 
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False)
    description = db.Column(db.String(length=200),
                            nullable=False)
    phone = db.Column(db.String(length=100), nullable=False)


# Display all things
# with app.app_context():
#     db.create_all(); # ننفذه مره وحدة فقط و بعدها حيكون اوريدي موجود بس يتعدل حسب ما ابغى سواء حذف او اضافة 


    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(
            plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


@app.route('/')
def showMain(): # ندخل على الصفحة الرئيسية 

    return render_template('main.html') # نستدعي التيمبليت تبعها من فولدر التيمبليت 


@app.route('/register', methods=['GET', 'POST']) # نظهر الفورم تبع الريجستر 
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password_hash=form.password.data,
                              department=form.department.data,
                              isapproved="1",
                              phone=form.phone.data
                              )
        db.session.add(user_to_create) # عشان يتم اضافة اليوزر اللي سواء تسجيل للداتا بيس
        db.session.commit()
        return redirect(url_for('userdashboard_page')) # بعد ما يصير يوزر مسجل يدخل على الداشبورد عشان يختار الخدمة اللي يبغاها 

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST']) # برضو نستدعي الفورم تبع اليوزر عشان يدخل 
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(
            email_address=form.email_address.data).first()
        print(attempted_user)
        if (attempted_user and attempted_user.password_hash == form.password.data
            ):
            login_user(attempted_user)

            return redirect(url_for('userdashboard_page')) # لو كان مسجل خلاص يدخل على الداشبورد

    return render_template('login.html', form=form) # لو مو مسجل يجلس في صفحة الدخول 


@app.route('/loginadmin', methods=['GET', 'POST'])
def loginadmin_page(): # صفحة الدخول بس للآدمن 
    form = LoginForm()
    if form.validate_on_submit():
        # attempted_user = User.query.filter_by(
        #     email_address=form.email_address.data).first()
        email_address = form.email_address.data
        password = form.password.data
        if (email_address == "admin@gmail.com" and password == "123456789"): # لو دخل بهذا الايميل والباس اوكي يسمح له بالدخول 

            # flash(
            #     f'Success! You are logged in as: {attempted_user.email_address}', category='success')
            return render_template("home/index.html") # هنا حيدخل الادمن 
        # else:
        #     flash('Username and password are not match! Please try again',
        #           category='danger')

    return render_template('loginadmin.html', form=form)


@app.route('/admin') # عشان يتم عرض بيانات اليوزر للادمن لانو هوا مسؤول عنهم 
def admin_page():

    # users = User.query.all()
    print(User.query.all())

    return render_template('home/tables.html', users=User.query.all())


@app.route('/adminsuggestions') #هنا تظهر الاقتراحات للادمن 
def adminsuggestions_page():

    # users = User.query.all()
    print(Suggestion.query.all())

    return render_template('home/tables-sugs.html', suggestions=Suggestion.query.all())


@app.route('/admincomplaints') #هنا تظهر الشكاوى للادمن 
def admincomplaints_page():

    # users = User.query.all()
    print(Complaint.query.all())

    return render_template('home/tables-comps.html', complaints=Complaint.query.all())


@app.route('/adminqueries') #هنا تظهر الاستفسارات للادمن 
def adminqueries_page():

    # users = User.query.all()
    # print(User.query.all())

    return render_template('home/tables-queries.html', queries=Query.query.all())


# @app.route('/dashboard', methods=['GET', 'POST'])
# def dashboard_page():

#     return render_template('dashboard.html')


@app.route('/admindashboard', methods=['GET', 'POST'])
def admindashboard_page():

    return render_template('home/index.html')


@app.route('/userdashboard', methods=['GET', 'POST'])
def userdashboard_page():

    return render_template('home/profile.html')


@app.route('/addcomplaint', methods=['GET', 'POST']) # اضافة الشكاوى 
def addcomplaint_page():
    form = AddComplaint()
    if form.validate_on_submit():
        complaint_to_create = Complaint(username=form.username.data,#اضافة الاسم 
                                        description=form.description.data,#اضافة وصف الشكوى 
                                        phone=form.phone.data #اضافة رقم الجوال 
                                        )
        db.session.add(complaint_to_create)
        db.session.commit()
        return redirect(url_for('addcomplaint_page'))

    return render_template('home/add-complaint.html', form=form)


@app.route('/addquery', methods=['GET', 'POST']) #اضافة الاستفسارات 
def addquery_page():
    form = AddQuery()
    if form.validate_on_submit():
        query_to_create = Query(username=form.username.data, #اضافة الاسم 
                                description=form.description.data, #وصف الاستفسار
                                phone=form.phone.data #رقم الجوال 
                                )
        db.session.add(query_to_create)
        db.session.commit() #هنا يتم التنفيذ 
        return redirect(url_for('addquery_page'))

    return render_template('home/add-query.html', form=form)


@app.route('/addsuggestion', methods=['GET', 'POST']) #اضافة الاقتراحات 
def addsuggestion_page():
    form = AddSuggestion()

    if form.validate_on_submit():
        suggestion_to_create = Suggestion(username=form.username.data, #الاسم 
                                          description=form.description.data,#وصف الاقتراح 
                                          phone=form.phone.data #رقم الجوال 
                                          )
        db.session.add(suggestion_to_create)
        db.session.commit()
        return redirect(url_for('addsuggestion_page'))

    return render_template('home/add-suggestion.html', form=form)


@app.route('/users/<int:id>/delete', methods=['GET', 'POST']) # عشان نحذف اليوزر 
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin_page'))

# @app.route('/download/<filename>')
# def download(filename):
#     print(filename)
#     return send_file(filename, as_attachment=True)




















if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
