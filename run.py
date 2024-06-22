from app import create_app, db
from app.models import Admin, Book, BorrowRecord

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Admin': Admin, 'Book': Book, 'BorrowRecord': BorrowRecord}

if __name__ == "__main__":
    app.run(debug=True)
