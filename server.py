from flask import Flask, redirect, url_for, request

from db import GolinksDatabase 
  
app = Flask(__name__)

@app.route(
        '/create',
        methods=['POST', 'GET'])
def create():
    link_text = request.args.get('link_text') or ''
    url = request.args.get('url') or ''
    description = request.args.get('description') or ''

    if link_text and url and description:
      db = GolinksDatabase()
      db.insert_row(
        link_text=link_text,
        destination_url=url,
        description=description)
      db.commit()
      return f'''
        Successfully created go/{link_text} as an alias to {url}!
        <a href="/">See all golinks here.</a>
      '''

    form = f'''
    <form action="create">
      <li>
        Alias (go/<alias>):
        <input type="text" name="link_text" value="{link_text}"/>
      </li>
      <li>URL: <input type="text" name="url" value="{url}"/></li>
      <li>
        Short description:
        <input type="text" name="description" value="{description}"/>
      </li>
      <input type="submit">
    </form>
    '''
    return form
  
@app.route('/', defaults={'path':''},methods=['POST','GET'])
@app.route('/<path:path>')
def default_handle(path):
    if not path:
      db = GolinksDatabase()
      all_rows = db.select_summary()

      enumerated_links = '<ul>'
      for row in all_rows:
          enumerated_links += f'<li>go/{row[1]} -> {row[2]}: {row[3]}</li>'
      enumerated_links += '</ul>'

      return f'''
      Welcome to Sammy\'s golink server!
      <a href="create">Create a new link here.</a><br/>
      {enumerated_links}
      '''

    db = GolinksDatabase()
    url = db.select_url_by_link_text(path)
    if url:
      return redirect(url, code=302)
      
    return f'go/{path} does not exist. <a href="create">Create it?</a>'
  
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
