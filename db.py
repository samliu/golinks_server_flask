import datetime
import pathlib 
import sqlite3
import textwrap

class bcolors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class GolinksDatabase(object):
  def __init__(self, db_name='golinks.db'):

    self.db = sqlite3.connect(db_name)
    self.c = self.db.cursor()
  def __del__(self):
    self.db.close() 

  def create_db(self):
    try:
      self.c.execute("""CREATE TABLE golinks 
          (link_text,
           row_id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
           destination_url TEXT,
           description TEXT,
           timestamp INTEGER)""")
    except Exception as e:
      print(e)

    try:
      createSecondaryIndex = "CREATE UNIQUE INDEX index_link_text ON golinks(link_text)"
      self.c.execute(createSecondaryIndex)
    except Exception as e:
        print(e)
    self.db.commit()

  def commit(self):
    self.db.commit()

  def insert_row(self, link_text: str, destination_url: str, description: str):
    timestamp = round(datetime.datetime.now().timestamp())
    try:
      self.c.execute(f'INSERT OR REPLACE INTO golinks(link_text, destination_url, description, timestamp) VALUES ("{link_text}", "{destination_url}", "{description}", "{timestamp}")')
      return True
    except Exception as e:
      print(e)
      return False

  def select_all(self):
    _SELECT_ALL_QUERY = "SELECT * FROM golinks"
    rows = self.c.execute(_SELECT_ALL_QUERY).fetchall()
    return rows

  def select_count(self):
    _SELECT_COUNT_QUERY = "SELECT COUNT(*) FROM golinks"
    rows = self.c.execute(_SELECT_COUNT_QUERY).fetchall()
    return rows[0][0]

  def select_summary(self):
    _SELECT_SUMMARY_QUERY = "SELECT row_id, link_text, destination_url, description, timestamp FROM golinks"
    return self.c.execute(_SELECT_SUMMARY_QUERY).fetchall()

  def select_url_by_link_text(self, link_text: str):
    _SELECT_BY_LINK_TEXT_QUERY = f'SELECT row_id, link_text, destination_url, description, timestamp FROM golinks WHERE link_text="{link_text}"'
    rows = self.c.execute(_SELECT_BY_LINK_TEXT_QUERY).fetchall()
    if rows:
      return rows[0][2]
    return None

def cli():
  # Create the DB if it doesn't already exist.
  db = GolinksDatabase()
  db.create_db()

  # This is how you add a row. Default is upsert, so it will override if the link_text already exists.
  # db.insert_row(link_text='blog', destination_url='http://google.com', description='My blog! yay')
  # db.commit() 
  # db.select_all()

  # This is how you fetch the row from text.
  # print(db.select_url_by_link_text('blog'))

  print('\nEnumerating rows:')
  print('='*80)
  for row in db.select_summary():
    print(row)
  print('='*80 + '\n')

  print(f'Row Count: {db.select_count()}')


if __name__ == "__main__":
  cli()

