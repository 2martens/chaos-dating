from django.test import TestCase


# Create your tests here.
class AlwaysPassTestCase(TestCase):
    def test_pass(self):
        self.assertEqual(True, True)
