from flask import request
from flask_restx import Resource, fields
from server.instance import server
from models.book import BookModel
from schema.book import BookSchema

book_schema = BookSchema()
book_list_schema = BookSchema(many=True)

book_ns = server.book_ns

ITEM_NOT_FOUND = "Item not found"

item = book_ns.model(
    "Book",
    {
        "title": fields.String("Book Title"),
        "pages": fields.Integer(default=0),
    },
)


@book_ns.route("/books/<int:id>")
class Book(Resource):
    def get(self, id):
        book_data = BookModel.find_by_id(id=id)
        if book_data:
            return book_schema.dump(book_data), 200
        return {"message": ITEM_NOT_FOUND}, 404

    @book_ns.expect(item)
    def put(self, id):
        book_json = request.get_json()
        book_data = BookModel.find_by_id(id=id)
        if book_data:
            book_data.title = book_json["title"]
            book_data.pages = book_json["pages"]

            book_data.save_to_db()

            return book_schema.dump(book_data), 200
        return {"message": ITEM_NOT_FOUND}, 404

    @book_ns.expect(item)
    def delete(self, id):
        book_data = BookModel.find_by_id(id=id)
        if book_data:
            book_data.delete_from_db()
            return book_schema.dump(book_data), 200

        return {"message": ITEM_NOT_FOUND}, 404


@book_ns.route("/books")
class BookList(Resource):
    def get(self):
        book_data = BookModel.find_all()
        if book_data:
            return book_list_schema.dump(book_data), 200
        return {"message": ITEM_NOT_FOUND}, 404

    @book_ns.expect(item)
    @book_ns.doc("Creat an item")
    def post(self):
        book_json = request.get_json()
        book_data = book_schema.load(book_json)
        try:
            book_data.save_to_db()
            return book_schema.dump(book_data), 201
        except:
            return {"message": "Item dont create"}, 500
