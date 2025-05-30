import unittest
from start import app
from unittest.mock import MagicMock, patch
from sweater import Users, Requests

class PageTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    #Homepage
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Help Your Business', response.data)

    def test_home_page_2(self):
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Help Your Business', response.data)

    #Sign up

    #GET
    def test_sign_up_page(self):
        response = self.client.get('/sign_up')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Регистрация'.encode('utf-8'), response.data)

    #Succesfull post
    def test_success_up(self):
        response = self.client.post('/sign_up', data={
            'login': 'testssdqwdhwSvkdcndbvser',
            'password': '1234',
            'check_password': '1234'
        }, follow_redirects=False)

        self.assertEqual(response.status_code, 302)

        self.assertIn('/sign_in', response.headers['Location'])

    #Login already exists
    def test_login_up(self):
        response = self.client.post('/sign_up', data={
            'login': 'dasha',
            'password': '1234',
            'check_password': '1234'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'login', response.data)

    #Passwords not the same
    def test_passwords_up(self):
        response = self.client.post('/sign_up', data={
            'login': 'testuserchchfx',
            'password': '1234',
            'check_password': '12344'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Passwords', response.data)

    #Login is empty
    def test_empty_login_up(self):
        response = self.client.post('/sign_up', data={
            'login': '',
            'password': '1234',
            'check_password': '1234'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Field', response.data)

    # Password is empty
    def test_empty_pass_up(self):
        response = self.client.post('/sign_up', data={
            'login': 'testusevjtytyr',
            'password': '',
            'check_password': ''
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Field', response.data)


    #Sign in
    #GET
    def test_sign_in(self):
        response = self.client.get('/sign_in')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Вход'.encode('utf-8'), response.data)

    #Success in
    def test_success(self):
        response = self.client.post('/sign_in', data={
            'login': 'dasha',
            'password': '123'
        }, follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/user', response.headers['Location'])

    # Login is empty
    def test_empty_login_in(self):
        response = self.client.post('/sign_in', data={
            'login': '',
            'password': '123',
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Field', response.data)


    #Password is empty
    def test_empty_pass_in(self):
        response = self.client.post('/sign_in', data={
            'login': 'dasha',
            'password': '',
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Field', response.data)

    #Login not exist
    def login_not_exist(self):
        response = self.client.post('/sign_in', data={
            'login': 'popko',
            'password': '123'
        }, follow_redirect=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'login', response.data)

    # Password is wrong
    def pass_wrong(self):
        response = self.client.post('/sign_in', data={
            'login': 'dasha',
            'password': '1238'
        }, follow_redirect=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Password', response.data)


    # New request
    #Get
    def index_get(self):
        response = self.client.get('/new_request')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Разработаем'.encode('utf-8'), response.data)

    def index_post(self):
        response = self.client.post('/new_request', data='Приветик если вы это читаете :)')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Результат'.encode('utf-8'), response.data)


    # Requests Story
    #GET
    def requests_get(self):
        response = self.client.get('/requests')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Ваши'.encode('utf-8'), response.data)


    # User menu
    #get
    def user_get(self):
        response = self.client.get('/user')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Опишите'.encode('utf-8'), response.data)


    # Logout
    def logout(self):
        response = self.client.get('/logout', follow_redirect=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/', response.headers['Location'])

