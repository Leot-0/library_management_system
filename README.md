
# Library Management System

This is a simple library management system built with Flask and MySQL. It allows administrators to manage books, borrow records, and users. The system also supports auto-acquisition of book information based on uploaded cover images using the SM.MS and OpenAI APIs.

## Features

- Add, edit, and delete books.
- Borrow and return books.
- View borrow records.
- Auto-acquisition of book information based on uploaded cover images.
- Search for books by title, author, or ISBN.

## Prerequisites

- Python 3.x
- MySQL

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/your-username/library_management_system.git
    cd library_management_system
    ```

2. Create and activate a virtual environment:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Set up the MySQL database:

    ```sh
    mysql -u root -p
    CREATE DATABASE library_db;
    ```

5. Configure the application:

    - Create a `.env` file in the root directory and add the following:

    ```sh
    FLASK_APP=app
    FLASK_ENV=development
    DATABASE_URL=mysql+pymysql://root:123456@localhost/library_db
    SECRET_KEY=your_secret_key
    ```

6. Initialize the database:

    ```sh
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```

## Running the Application

1. Start the Flask development server:

    ```sh
    flask run
    ```

2. Open your web browser and go to `http://127.0.0.1:5000`.

## Usage

### Adding a Book

1. Go to the "Add Book" page.
2. Fill out the form with the book details. If you enable the "Auto Acquisition" option, the form will auto-fill the details based on the uploaded cover image.
3. Click the "Add Book" button.

### Editing a Book

1. Go to the "Home" page.
2. Click on the "Edit" button next to the book you want to edit.
3. Update the book details and click the "Save" button.

### Deleting a Book

1. Go to the "Home" page.
2. Click on the "Delete" button next to the book you want to delete.

### Borrowing a Book

1. Go to the "Home" page.
2. Click on the "Borrow" button next to the book you want to borrow.
3. Fill out the borrower's name and click the "Borrow" button.

### Returning a Book

1. Go to the "Borrow Records" page.
2. Click on the "Return" button next to the book you want to return.

## Configuration

### SM.MS API

To use the auto-acquisition feature, you need an SM.MS API token. Add the token to the `.env` file:

```sh
SMMS_API_TOKEN=your_smms_api_token
```

### OpenAI API

To use the OpenAI API for book information extraction, add your OpenAI API key to the `.env` file:

```sh
OPENAI_API_KEY=your_openai_api_key
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
