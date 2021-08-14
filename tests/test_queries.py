import pytest
from graphene.test import Client
from unittest import TestCase
from mixer.backend.sqlalchemy import mixer

from main import schema


@pytest.mark.skip
class TestQuery(TestCase):
    def setUp(self):
        self.advertisement = mixer.blend("models.Advertisement")
        self.client = Client(schema)

    def test_all_advertisements_sort_0(self):
        executed = self.client.execute('''query{ allAdvertisements }''',
                                       variables={'sort': 0},
                                       context={'createdAt'})
        advertisements = executed.get("data").get("allAdvertisements")
        assert len(advertisements)

    def test_all_advertisements_sort_1(self):
        executed = self.client.execute('''query{ allAdvertisements }''',
                                       variables={'sort': 1},
                                       context={'price'})
        advertisements = executed.get("data").get("allAdvertisements")
        assert len(advertisements)

    def test_all_advertisements(self):
        executed = self.client.execute('''query { allAdvertisements }''',
                                       context={'id'})
        advertisements = executed.get("data").get("allAdvertisements")
        assert len(advertisements)

    def test_advertisements_by_id(self):
        executed = self.client.execute('''query { advertisementsById }''',
                                       context={'advertisement_id': self.advertisement.id})
        selected_id = executed.get("data").get("advertisementsById").get("ok")
        assert selected_id == self.advertisement.id
