# Library Management System

## Description

The Library Management System is a backend API developed using FastAPI and MongoDB. It provides functionality for managing books, creating borrowings, returning books, and retrieving borrowings.

## Tech Stack

- **Language:** Python
- **Framework:** FastAPI
- **Database:** MongoDB (MongoDB Atlas M0 Free Cluster)

## Requirements

- Python 3.x
- FastAPI
- PyMongo
- MongoDB Atlas M0 Free Cluster

## Installation

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd library-management-system
   ```

Sure, here is the content formatted as requested:

markdown
Copy code

# Library Management System

## Description

The Library Management System is a backend API developed using FastAPI and MongoDB. It provides functionality for managing books, creating borrowings, returning books, and retrieving borrowings.

## Tech Stack

- **Language:** Python
- **Framework:** FastAPI
- **Database:** MongoDB (MongoDB Atlas M0 Free Cluster)

## Requirements

- Python 3.x
- FastAPI
- PyMongo
- MongoDB Atlas M0 Free Cluster

## Installation

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd library-management-system
   ```

2. Install dependencies:

   pip install -r requirements.txt

3. Set up MongoDB Atlas and obtain the connection URI.

4. Replace the MongoDB connection URI in the main.py file.

5. Run the application:

   uvicorn main:app --reload

## API Endpoints

GET /books: Retrieve all books.
POST /borrowings: Create a borrowing.
GET /borrowings: Retrieve all borrowings.
GET /borrowings/{borrowing_id}: Retrieve a borrowing by ID.
PUT /borrowings/{borrowing_id}/return: Return a book.
