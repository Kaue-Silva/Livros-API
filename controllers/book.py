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
        "title": fields.String(
            description="Book Title", required=True, min_lenght=1, max_length=80
        ),
        "pages": fields.Integer(
            default=0, required=True, description="Amount pages the book"
        ),
    },
)


@book_ns.route("/books/<int:id>")
@book_ns.doc(responses={200: "Success", 404: "Not Found"}, model=item)
class Book(Resource):
    @book_ns.doc(
        "Get item by Id",
    )
    def get(self, id):
        book_data = BookModel.find_by_id(id=id)
        if book_data:
            return book_schema.dump(book_data), 200
        return {"message": ITEM_NOT_FOUND}, 404

    @book_ns.doc(
        "Change item by Id",
        body=item,
    )
    def put(self, id):
        book_json = request.get_json()
        book_data = BookModel.find_by_id(id=id)
        if book_data:
            book_data.title = book_json["title"]
            book_data.pages = book_json["pages"]

            book_data.save_to_db()

            return book_schema.dump(book_data), 200
        return {"message": ITEM_NOT_FOUND}, 404

    @book_ns.doc(
        "Change partial item by Id",
        body=item,
    )
    def patch(self, id):
        book_json = request.get_json()
        book_data = BookModel.find_by_id(id=id)
        if book_data:
            if "title" in book_json:
                book_data.title = book_json["title"]
            if "pages" in book_json:
                book_data.pages = book_json["pages"]
            book_data.save_to_db()
            return book_schema.dump(book_data), 200
        return {"message": ITEM_NOT_FOUND}, 404

    @book_ns.doc(
        "Delete item by Id",
    )
    def delete(self, id):
        book_data = BookModel.find_by_id(id=id)
        if book_data:
            book_data.delete_from_db()
            return book_schema.dump(book_data), 200

        return {"message": ITEM_NOT_FOUND}, 404


@book_ns.route("/books")
@book_ns.doc(responses={200: "Success", 404: "Not Found"}, model=item)
class BookList(Resource):
    @book_ns.marshal_with(item, as_list=True)
    @book_ns.doc(
        "Get all items",
    )
    def get(self):
        book_data = BookModel.find_all()
        if book_data:
            return book_list_schema.dump(book_data), 200
        return {"message": ITEM_NOT_FOUND}, 404

    @book_ns.doc(
        "Creat an item",
        body=item,
    )
    def post(self):
        book_json = request.get_json()
        book_data = book_schema.load(book_json)
        try:
            book_data.save_to_db()
            return book_schema.dump(book_data), 201
        except:
            return {"message": "Item dont create"}, 500
