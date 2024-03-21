import os
import unittest
import tempfile
from sqlalchemy import text

from src.database import set_database, Session


class StrongboxTest(unittest.TestCase):


  @classmethod
  def setUpClass(self):
    self.db_file = tempfile.mktemp(suffix=".db")

    with open("test_db.sql", "r") as dump_file:
      self.engine = set_database(f"sqlite:///{self.db_file}")

      for statement in dump_file.read().split(";"):
        if statement.strip():
          with Session() as session:
            session.execute(text(statement))
            session.commit()               


  @classmethod
  def tearDownClass(self):
      self.engine.dispose()
      os.remove(self.db_file)
    