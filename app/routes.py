from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app.models import Admin, Book, BorrowRecord
from app.forms import LoginForm, AddBookForm, EditBookForm, BorrowBookForm, SearchForm
from werkzeug.utils import secure_filename
import os
import requests
import json

bp = Blueprint('routes', __name__)

@bp.route('/')
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('routes.search_results', query=form.search.data))
    books = Book.query.all()
    return render_template('book_list.html', title='Home', books=books, form=form)

@bp.route('/search_results/<query>')
@login_required
def search_results(query):
    form = SearchForm()
    books = Book.query.filter(
        Book.title.ilike(f'%{query}%') |
        Book.author.ilike(f'%{query}%') |
        Book.isbn.ilike(f'%{query}%')
    ).all()
    return render_template('search_results.html', title='Search Results', books=books, query=query, form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Admin.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('routes.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('routes.index'))
    return render_template('login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('routes.login'))

@bp.route('/edit_book/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_book(id):
    book = Book.query.get_or_404(id)
    form = EditBookForm(obj=book)
    if form.validate_on_submit():
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            book.image = filename
        book.title = form.title.data
        book.author = form.author.data
        book.publisher = form.publisher.data
        book.publication_date = form.publication_date.data
        book.isbn = form.isbn.data
        book.category = form.category.data
        book.stock_quantity = form.stock_quantity.data
        db.session.commit()
        flash('Book updated successfully!')
        return redirect(url_for('routes.index'))
    return render_template('edit_book.html', title='Edit Book', form=form, book=book)

@bp.route('/delete_book/<int:id>', methods=['POST'])
@login_required
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully!')
    return redirect(url_for('routes.index'))

@bp.route('/borrow_book/<int:id>', methods=['GET', 'POST'])
@login_required
def borrow_book(id):
    book = Book.query.get_or_404(id)
    form = BorrowBookForm()
    if form.validate_on_submit():
        if book.stock_quantity > 0:
            book.stock_quantity -= 1
            borrow_record = BorrowRecord(user_id=current_user.id, book_id=book.id, borrower_name=form.borrower_name.data)
            db.session.add(borrow_record)
            db.session.commit()
            flash('Book borrowed successfully!')
        else:
            flash('Book out of stock!')
        return redirect(url_for('routes.index'))
    return render_template('borrow_book.html', title='Borrow Book', form=form, book=book)

@bp.route('/return_book/<int:id>', methods=['POST'])
@login_required
def return_book(id):
    borrow_record = BorrowRecord.query.filter_by(book_id=id, user_id=current_user.id, return_date=None).first_or_404()
    borrow_record.return_date = db.func.current_timestamp()
    book = Book.query.get(borrow_record.book_id)
    book.stock_quantity += 1
    db.session.commit()
    flash('Book returned successfully!')
    return redirect(url_for('routes.index'))

@bp.route('/borrow_records')
@login_required
def borrow_records():
    records = BorrowRecord.query.filter_by(user_id=current_user.id).all()
    return render_template('borrow_records.html', title='Borrow Records', records=records)

def upload_image_to_smms(image_path, api_token):
    url = "https://sm.ms/api/v2/upload"
    headers = {
        "Authorization": api_token
    }
    files = {
        "smfile": open(image_path, "rb")
    }
    response = requests.post(url, headers=headers, files=files)
    response_data = response.json()
    print(f"SM.MS Response: {response_data}")  # 打印SM.MS API的响应
    if response_data["success"]:
        return response_data["data"]["url"]
    else:
        return None

def get_book_info_from_image(image_url):
    api_url = "https://api.pumpkinaigc.online/v1/chat/completions" # 替换为你的 OpenAI API url
    headers = {
        "Authorization": "Bearer XXXXXXXXXX",  # 替换为你的 OpenAI API Key
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "根据这张图书封面，以json的格式，查询后告诉我这本书的title,author,publisher,publication_date,isbn,category.可进行推测，确保每个字段有实际的数据相对应，日期要以年月日的格式，不能是不详。无需返回其他描述。"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        }
                    }
                ]
            }
        ]
    }

    response = requests.post(api_url, headers=headers, data=json.dumps(data))
    response_text = response.text
    print(f"OpenAI Response: {response_text}")  # 打印OpenAI API的响应内容
    try:
        response_json = response.json()
        content = response_json['choices'][0]['message']['content']
        # 去掉前后的 ```json 标记
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        book_info = json.loads(content)
        return {
            'title': book_info.get('title', '1'),
            'author': book_info.get('author', '1'),
            'publisher': book_info.get('publisher', '1'),
            'publication_date': book_info.get('publication_date', '2008-8-8'),
            'isbn': book_info.get('isbn', '1'),
            'category': book_info.get('category', '1'),
            'stock_quantity': 1  # 默认填充1
        }
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        raise

@bp.route('/auto_acquire_info', methods=['POST'])
@login_required
def auto_acquire_info():
    if 'image' not in request.files:
        print("No image uploaded")  # 打印日志
        return jsonify({'error': 'No image uploaded'}), 400

    image = request.files['image']
    filename = secure_filename(image.filename)
    image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    print(f"Saving image to: {image_path}")  # 打印保存的路径
    image.save(image_path)

    image_url = upload_image_to_smms(image_path, "XXXXXXXXXXXXXXX")  # 替换为你的 SM.MS API Token
    if not image_url:
        print("Failed to upload image to SM.MS")  # 打印日志
        return jsonify({'error': 'Failed to upload image to SM.MS'}), 500

    try:
        book_info = get_book_info_from_image(image_url)
        print(f"Book info: {book_info}")  # 打印获取的书籍信息
        return jsonify(book_info)
    except Exception as e:
        print(f"Error getting book info: {e}")  # 打印错误信息
        return jsonify({'error': 'Failed to get book info from image'}), 500

@bp.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    form = AddBookForm()
    if form.validate_on_submit():
        filename = None
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        book = Book(
            title=form.title.data,
            author=form.author.data,
            publisher=form.publisher.data,
            publication_date=form.publication_date.data,
            isbn=form.isbn.data,
            category=form.category.data,
            stock_quantity=1,  # 填充为1
            image=filename
        )
        db.session.add(book)
        db.session.commit()
        flash('Book added successfully!')
        return redirect(url_for('routes.index'))
    return render_template('add_book.html', title='Add Book', form=form)
