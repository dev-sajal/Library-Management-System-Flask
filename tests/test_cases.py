import os
import pytest
from api import app, db


class TestAPI:
    client = app.test_client()
    server_url = "http://localhost:5000/"
    headers = {'Content-Type': "application/json", 'cache-control': "no-cache"}

    @pytest.fixture(autouse=True, scope='session')
    def set_up(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testing.db'
        db.create_all()
        yield db
        os.remove('testing.db')

    ####################################################################################################################
    def test_create_user_with_valid_details(self):
        url = f"{self.server_url}users/"
        payload = '{"user_id": 1 , "user_name": "username1"}'
        response = self.client.post(url, data=payload, headers=self.headers)
        assert response.status_code == 201
        assert response.json['Message'].strip() == 'User registered successfully'

        payload = '{"user_id": 2 , "user_name": "username2"}'
        response = self.client.post(url, data=payload, headers=self.headers)
        assert response.status_code == 201
        assert response.json['Message'].strip() == 'User registered successfully'

    def test_create_user_with_invalid_details(self):
        url = f"{self.server_url}users/"
        payload = '{"user_id": 1 , "user_name": "username1"}'
        response = self.client.post(url, data=payload, headers=self.headers)
        assert response.status_code == 400
        assert response.json['Error'].strip() == 'User with same id already exists'

        url = f"{self.server_url}users/"
        payload = '{"user_id": 21 , "user_name": ""}'
        response = self.client.post(url, data=payload, headers=self.headers)
        assert response.status_code == 400
        assert response.json['Error'].strip() == 'User name cannot be empty'

    def test_get_list_of_all_user(self):
        url = f"{self.server_url}users/"
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.json == [{"user_id": 1, "user_name": "username1"}, {"user_id": 2, "user_name": "username2"}]

    def test_get_particular_user(self):
        url = f"{self.server_url}users/1"
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.json == {'user_name': 'username1', 'user_id': 1}

    def test_get_particular_user_with_invalid_id(self):
        url = f"{self.server_url}users/15"
        response = self.client.get(url)
        assert response.status_code == 400
        assert response.json['Message'].strip() == 'No user with that ID'

    def test_delete_particular_user(self):
        url = f"{self.server_url}users/2"
        response = self.client.delete(url)
        assert response.status_code == 204

    ########################################################################################################

    def test_create_book_with_valid_details(self):
        url = f"{self.server_url}books/"
        payload = '{"book_id": 1 , "book_name": "test_book", "book_author":"test_author"}'
        response = self.client.post(url, data=payload, headers=self.headers)
        assert response.status_code == 201
        assert response.json['Message'].strip() == 'Book added successfully'

        payload = '{"book_id": 2 , "book_name": "test_book", "book_author":"test_author2"}'
        response = self.client.post(url, data=payload, headers=self.headers)
        assert response.status_code == 201
        assert response.json['Message'].strip() == 'Book added successfully'

    def test_create_book_with_invalid_details(self):
        url = "http://localhost:5000/books/"
        payload = '{"book_id": 1 , "book_name": "test_book", "book_author":"test_author"}'
        response = self.client.post(url, data=payload, headers=self.headers)
        assert response.status_code == 400
        assert response.json['Error'].strip() == 'Book with same id already exists'

        payload = '{"book_id": 21 , "book_name": "", "book_author":"test_author"}'
        response = self.client.post(url, data=payload, headers=self.headers)
        assert response.status_code == 400
        assert response.json['Error'].strip() == 'Book name cannot be empty'

        payload = '{"book_id": 21 , "book_name": "test_book", "book_author":""}'
        response = self.client.post(url, data=payload, headers=self.headers)
        assert response.status_code == 400
        assert response.json['Error'].strip() == 'Author name cannot be empty'

    def test_get_list_of_all_books(self):
        url = f"{self.server_url}books/"
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.json == [
            {'book_author': 'test_author', 'book_available': True, 'book_id': 1, 'book_name': 'test_book'},
            {'book_author': 'test_author2', 'book_available': True, 'book_id': 2, 'book_name': 'test_book'}]

    def test_get_particular_book(self):
        url = f"{self.server_url}books/1"
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.json == {'book_author': 'test_author', 'book_available': True, 'book_id': 1,
                                 'book_name': 'test_book'}

    def test_get_particular_book_with_invalid_details(self):
        url = f"{self.server_url}books/21"
        response = self.client.get(url)
        assert response.status_code == 400
        assert response.json['Error'] == 'No book with that ID'

    def test_delete_particular_book(self):
        url = f"{self.server_url}books/2"
        response = self.client.delete(url)
        assert response.status_code == 204

    #######################################################################################
    def test_create_entry_for_borrowing(self):
        url = f"{self.server_url}books/"
        response = self.client.get(url)
        assert response.json == [
            {'book_name': 'test_book', 'book_author': 'test_author', 'book_available': True, 'book_id': 1}]

        url = f"{self.server_url}borrows/"
        payload = '{"book_id": 1 , "user_id": 1, "till_date": "2022-02-03", "borrowing_date":"2020-02-19"}'
        response = self.client.post(url, data=payload, headers=self.headers)
        assert response.status_code == 200
        assert response.json['Message'] == 'Successfully borrowed'

        url = f"{self.server_url}books/"
        response = self.client.get(url)
        assert response.json == [
            {'book_id': 1, 'book_name': 'test_book', 'book_available': False, 'book_author': 'test_author'}]

    def test_create_entry_for_borrowing_with_invalid_details(self):
        url = f"{self.server_url}borrows/"
        payload = '{"book_id": 1 , "user_id": 1, "till_date": "2022-02-03", "borrowing_date":"2020-02-19"}'
        response = self.client.post(url, data=payload, headers=self.headers)
        assert response.status_code == 400
        assert response.json['Error'] == 'Book not available'

        url = f"{self.server_url}borrows/"
        payload = '{"book_id": 21 , "user_id": 21, "till_date": "2022-02-03", "borrowing_date":"2020-02-19"}'
        response = self.client.post(url, data=payload, headers=self.headers)
        assert response.status_code == 400
        assert response.json['Error'].strip() == 'No user with that ID'

        url = f"{self.server_url}borrows/"
        payload = '{"book_id": 21 , "user_id": 1, "till_date": "2022-02-03", "borrowing_date":"2020-02-19"}'
        response = self.client.post(url, data=payload, headers=self.headers)
        assert response.status_code == 400
        assert response.json['Error'].strip() == 'No book with that ID'

    def test_get_info_using_borrow_id(self):
        url = f"{self.server_url}borrows/1"
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.json == {'till_date': '2022-02-03', 'borrowing_date': '2020-02-19',
                                 'book_id': 1, 'user_id': 1, 'is_returned': False}

    def test_get_info_using_borrow_id_with_invalid_details(self):
        url = f"{self.server_url}borrows/12"
        response = self.client.get(url)
        assert response.status_code == 400
        assert response.json['Error'] == 'No details found with that ID'

    def test_get_all_available_books(self):
        url = f"{self.server_url}borrows/availablebooks"
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.json == []

    ####################################################################################################################
    def test_generate_bill_with_invalid_details(self):
        url = f"{self.server_url}bills/"
        payload = '{"borrow_id": 1 , "return_date": "2018-02-20"}'
        response = self.client.post(url, data=payload, headers=self.headers)
        assert response.status_code == 400
        assert response.json['Error'].strip() == 'Return date cannot be in past'

    def test_generate_bill(self):
        url = f"{self.server_url}borrows/availablebooks"
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.json == []

        url = f"{self.server_url}bills/"
        payload = '{"borrow_id": 1 , "return_date": "2022-02-20"}'
        response = self.client.post(url, data=payload, headers=self.headers)
        assert response.status_code == 200
        assert response.json['Message'].strip() == 'Bill generated'

        response = self.client.post(url, data=payload, headers=self.headers)
        assert response.status_code == 400
        assert response.json['Error'].strip() == 'Book already returned'

        url = f"{self.server_url}borrows/availablebooks"
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.json == [
            {'book_name': 'test_book', 'book_available': True, 'book_id': 1, 'book_author': 'test_author'}]

    def test_get_bill_using_billing_id(self):
        url = f"{self.server_url}bills/1"
        response = self.client.get(url)
        assert response.json == {'bill_amount': '7490.0', 'return_date': '2022-02-20', 'borrow_id': 1}
        assert response.status_code == 200

    def test_get_bill_using_billing_id_with_invalid_details(self):
        url = f"{self.server_url}bills/21"
        response = self.client.get(url)
        assert response.status_code == 400
        assert response.json['Error'].strip() == 'No bill with that ID'
