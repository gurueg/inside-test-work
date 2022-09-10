import unittest
import requests
import sqlalchemy
from hashlib import md5

import settings
from app import db
import models


class RestTest(unittest.TestCase):
    _url = 'http://' + ':'.join([settings.HOST, settings.PORT])

    @classmethod
    def setUpClass(cls):
        cls._engine = sqlalchemy.create_engine(settings.POSTGRE_URI)
        db.metadata.create_all(cls._engine)
        cls._session = sqlalchemy.orm.Session(bind=cls._engine)


    @classmethod
    def tearDownClass(cls):
        user = cls._session.query(models.User).\
            filter_by(name='TestUser').\
            one()
        cls._session.query(models.Message).\
            filter_by(author=user.id).\
            delete()
        cls._session.query(models.User).\
            filter_by(name='TestUser').\
            delete()
        cls._session.commit()


    def testHealth(self):
        response = requests.get(self._url + '/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'OK')


    def testRegister(self):
        response = requests.post(self._url + '/register',
            json={
                'name': 'TestUser',
                'password': 'test_pass'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json()['token'])


    def testLogin(self):
        response = requests.post(self._url + '/login',
            json={
                'name': 'TestUser',
                'password': 'test_pass'
            }
        )
        self.assertEqual(response.status_code, 200)

        user = models.User.by_name('TestUser')
        self.assertEqual(response.json()['token'], user.token)

        response = requests.post(self._url + '/login',
            json={
                'name': 'TestUser',
                'password': 'wrong_pass'
            }
        )
        self.assertEqual(response.status_code, 401)

        response = requests.post(self._url + '/login',
            json={
                'name': 'WrongUser',
                'password': 'test_pass'
            }
        )
        self.assertEqual(response.status_code, 401)


    def testSendingMessage(self):
        user = models.User.by_name('TestUser')
        response = requests.post(self._url + '/message',
            json={
                'name': 'TestUser',
                'message': 'SendTestMessage'
            },
            headers={
                'Authorization': 'Bearer_' + user.token
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['text'], 'SendTestMessage')


    def testCheckingMessages(self):
        user = models.User.by_name('TestUser')
        response = requests.post(self._url + '/message',
            json={
                'name': 'TestUser',
                'message': 'history 6'
            },
            headers={
                'Authorization': 'Bearer_' + user.token
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['text'], 'SendTestMessage')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(RestTest('testHealth'))
    suite.addTest(RestTest('testRegister'))
    suite.addTest(RestTest('testLogin'))
    suite.addTest(RestTest('testSendingMessage'))
    suite.addTest(RestTest('testCheckingMessages'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())