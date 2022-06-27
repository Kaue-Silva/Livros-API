from unittest import TestCase, mock
from app import app


class TestBook(TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_get_all_books_return_200(self):
        response = self.client.get("/api/books")
        self.assertEqual(200, response.status_code)

    def test_get_all_books_return_json(self):
        response = self.client.get("/api/books")
        self.assertEqual("application/json", response.content_type)

    @mock.patch("controllers.book.BookModel.save_to_db")
    def test_create_new_book_return_201(self, mock_db):
        book = {"title": "Percy Jackson", "pages": 300}
        response = self.client.post("api/books", json=book)

        self.assertEqual(201, response.status_code)

    @mock.patch("controllers.book.BookModel.save_to_db")
    def test_create_new_book_return_json(self, mock_db):
        book = {"title": "Percy Jackson", "pages": 300}
        response = self.client.post("api/books", json=book)

        self.assertEqual("application/json", response.content_type)

    @mock.patch("controllers.book.BookModel.save_to_db")
    def test_altered_book_return_200(self, mock_db):
        book = {"title": "Percy Jackson", "pages": 300}
        response = self.client.put("api/books/1", json=book)

        self.assertEqual(200, response.status_code)

    @mock.patch("controllers.book.BookModel.save_to_db")
    def test_altered_book_return_json(self, mock_db):
        book = {"title": "HarryPotter", "pages": 200}
        response = self.client.put("api/books/1", json=book)

        self.assertEqual("application/json", response.content_type)

    @mock.patch("controllers.book.BookModel.delete_from_db")
    def test_delete_book_return_200(self, mock_db):
        response = self.client.delete("api/books/1")

        self.assertEqual(200, response.status_code)

    @mock.patch("controllers.book.BookModel.delete_from_db")
    def test_delete_book_return_json(self, mock_db):
        response = self.client.delete("api/books/1")

        self.assertEqual("application/json", response.content_type)

    @mock.patch("controllers.book.BookModel.save_to_db")
    def test_altered_partial_return_200(self, mock_db):
        book = {"title": "Percy Jackson"}
        response = self.client.patch("api/books/1", json=book)

        self.assertEqual(200, response.status_code)

    @mock.patch("controllers.book.BookModel.save_to_db")
    def test_altered_partial_return_json(self, mock_db):
        book = {"pages": 200}
        response = self.client.patch("api/books/1", json=book)

        self.assertEqual("application/json", response.content_type)
