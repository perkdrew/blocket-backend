from graphene.test import Client
from unittest import TestCase
from mixer.backend.sqlalchemy import mixer

from schemas import AdvertisementSchema

create_mutation = """mutation CreateNewAdvertisement{ 
  createNewAdvertisement(
    subject:"Promotional", body:"Here is my ad!", price: 300, email: "drewcperkins@gmail.com"
  ) { ok } }"""


class TestMutation(TestCase):
    def setUp(self):
        self.advertisement = mixer.blend("models.Advertisement")
        self.client = Client(AdvertisementSchema)

    def test_create_new_advertisement(self):
        executed = self.client.execute('''{ createNewAdvertisement }''',
                                       context={'sort': 0})
        ok = executed.get("data").get("advertisementsById").get("ok")
        assert ok

    def test_update_advertisement(self):
        executed = self.client.execute('''{ updateAdvertisement }''',
                                       context={'id': 1})
        ok = executed.get("data").get("advertisementsById").get("ok")
        assert ok

    def test_delete_advertisement(self):
        executed = self.client.execute('''{ deleteAdvertisement }''',
                                       context={'id': 1})
        ok = executed.get("data").get("advertisementsById").get("ok")
        assert ok

