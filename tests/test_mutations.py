import pytest
from graphene.test import Client
from unittest import TestCase
from mixer.backend.sqlalchemy import mixer

from main import schema


@pytest.mark.skip
class TestMutation(TestCase):
    def setUp(self):
        self.advertisement = mixer.blend("models.Advertisement")
        self.client = Client(schema)

    def test_create_new_advertisement(self):
        executed = self.client.execute('''mutation CreateNewAdvertisement{ createNewAdvertisement } }''',
                                       variables={'subject': 'TestSubject',
                                                  'body': 'TestBody',
                                                  'price': 1000,
                                                  'email': 'test@testmail.com'},
                                       context={'ok'})
        ok = executed.get("data").get("advertisementsById").get("ok")
        assert ok

    def test_update_advertisement(self):
        executed = self.client.execute('''mutation UpdateAdvertisement{ updateAdvertisement }''',
                                       variables={'id': self.advertisement.id,
                                                  'body': 'I am an updated test body.'},
                                       context={'ok'})
        ok = executed.get("data").get("advertisementsById").get("ok")
        assert ok

    def test_delete_advertisement(self):
        executed = self.client.execute('''mutation { deleteAdvertisement }''',
                                       variables={'id': self.advertisement.id},
                                       context={'ok'})
        ok = executed.get("data").get("advertisementsById").get("ok")
        assert ok
