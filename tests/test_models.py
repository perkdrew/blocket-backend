from unittest import TestCase
from mixer.backend.sqlalchemy import mixer


class TestAdvertisement(TestCase):
    def setUp(self):
        self.advertisement = mixer.blend("models.Advertisement")

    def test_model_id(self):
        self.assertTrue(type(self.advertisement.id), type(int))

    def test_model_subject(self):
        self.assertTrue(type(self.advertisement.subject), type(str))

    def test_model_body(self):
        self.assertTrue(type(self.advertisement.body), type(str))

    def test_model_null_price(self):
        self.assertTrue(type(self.advertisement.price), type(None))

    def test_model_email(self):
        self.assertTrue(type(self.advertisement.email), type(str))
