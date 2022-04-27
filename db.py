import datetime
import pathlib 
import sqlite3
import textwrap

class GolinksDatabase(object):
  def __init__(self, db_name='golinks.db', in_mem=False):
    if in_mem:
      self.db = sqlite3.connect(":memory:")
    else:
      self.db = sqlite3.connect(db_name)
    self.c = self.db.cursor()

  def __del__(self):
    self.db.close() 

  def create_db(self):
    try:
      CREATE_TABLE = '''
        CREATE TABLE golinks 
          (link_text,
           row_id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
           destination_url TEXT,
           description TEXT,
           timestamp INTEGER)
      '''
      self.c.execute(CREATE_TABLE)
    except Exception as e:
      print(e)

    try:
      CREATE_INDEX= "CREATE UNIQUE INDEX index_link_text ON golinks(link_text)"
      self.c.execute(CREATE_INDEX)
    except Exception as e:
        print(e)

    self.db.commit()

  def commit(self):
    self.db.commit()

  def insert_row(self, link_text: str, destination_url: str, description: str):
    # Rounded seconds from the epoch.
    timestamp = round(datetime.datetime.now().timestamp())
    try:
      UPSERT_ROW = f'''
        INSERT OR REPLACE INTO
        golinks(link_text, destination_url, description, timestamp)
        VALUES
          ("{link_text}",
           "{destination_url}",
           "{description}",
           "{timestamp}")
      '''
      self.c.execute(UPSERT_ROW)
      return True
    except Exception as e:
      print(e)
      return False

  def select_all(self):
    SELECT_STAR = "SELECT * FROM golinks"
    rows = self.c.execute(SELECT_STAR).fetchall()
    return rows

  def select_count(self):
    SELECT_COUNT = "SELECT COUNT(*) FROM golinks"
    rows = self.c.execute(SELECT_COUNT).fetchall()
    return rows[0][0]

  def select_summary(self):
    SELECT_COLUMNS = "SELECT row_id, link_text, destination_url, description, timestamp FROM golinks"
    return self.c.execute(SELECT_COLUMNS).fetchall()

  def select_url_by_link_text(self, link_text: str):
    SELECT_BY_LINK_TEXT = f'''
      SELECT destination_url 
      FROM golinks
      WHERE link_text="{link_text}"
    '''
    rows = self.c.execute(SELECT_BY_LINK_TEXT).fetchall()
    if rows:
      return rows[0][0]
    return None

def cli():
  # Create the DB if it doesn't already exist.
  db = GolinksDatabase()
  db.create_db()

  # This is how you add a row. Default is upsert, so it will override if the
  # link_text already exists.
  # db.insert_row(
  #   link_text='blog',
  #   destination_url='http://google.com',
  #   description='My blog! yay')
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
