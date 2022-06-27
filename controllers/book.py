from flask_restx import Resource
from server.instance import server
from models.book import BookModel
from schema.book import BookSchema

book_ns = server.book_ns

ITEM_NOT_FOUND = "Item not found"


@book_ns.route("/books/<int:id>")
class Book(Resource):
    def get(self, id):
        book_data = BookModel.find_by_id(id=id)
        if book_data:
            return BookSchema.dump(book_data), 200
        return {"message": ITEM_NOT_FOUND}, 404


@book_ns.route("/books")
class BookList(Resource):
    def get(self):
        book_data = BookModel.find_all()
        if book_data:
            return BookSchema.dump(book_data), 200
        return {"message": ITEM_NOT_FOUND}, 404
