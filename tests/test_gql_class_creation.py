import unittest
import context
from datetime import datetime
from grapinator import settings, log, schema_settings
from grapinator.schema import *

class TestStringMethods(unittest.TestCase):

    def test_gql(self):
        for c in schema_settings.get_gql_classes():
            self.assertTrue(
                issubclass(globals()[c['gql_class']], SQLAlchemyObjectType)
                ,"test_gql failed!"
                )

    def test_gql_connection(self):
        for c in schema_settings.get_gql_classes():
            self.assertTrue(
                issubclass(globals()[c['gql_conn_class']], relay.Connection)
                ,"test_gql_connection failed!"
                )
