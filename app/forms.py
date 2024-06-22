from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, IntegerField, FileField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from flask_wtf.file import FileAllowed, FileRequired
from app.models import Admin

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class AddBookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    publisher = StringField('Publisher', validators=[DataRequired()])
    publication_date = StringField('Publication Date', validators=[DataRequired()])
    isbn = StringField('ISBN', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    stock_quantity = IntegerField('Stock Quantity', default=1)
    image = FileField('Book Image')
    auto_acquisition = BooleanField('Auto acquisition')
    submit = SubmitField('Add Book')

class EditBookForm(AddBookForm):
    submit = SubmitField('Update Book')

class BorrowBookForm(FlaskForm):
    borrower_name = StringField('Borrower Name', validators=[DataRequired()])
    submit = SubmitField('Borrow Book')

class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')
