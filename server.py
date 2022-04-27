from flask import Flask, redirect, render_template, request, url_for 

from db import GolinksDatabase 
  
app = Flask(__name__)


def sanitize_alias(link_text):
  if link_text.startswith('http://'):
    link_text = link_text[7:]
  if link_text.startswith('https://'):
    link_text = link_text[8:]
  if link_text.startswith('go/'):
    link_text = link_text[3:]
  link_text = link_text.replace("/","")
  link_text = link_text.replace(".","")
  link_text = link_text.replace("?","")
  link_text = link_text.replace("+","")
  link_text = link_text.replace("\"","")
  link_text = link_text.replace("'","")
  return link_text.strip()

def add_http(url_text):
  if (not url_text.startswith('http://')
      and not url_text.startswith('https://')):
    url_text = f'http://{url_text}'
  return url_text

@app.route(
        '/create',
        methods=['POST', 'GET'])
def create():
    link_text = request.args.get('link_text') or ''
    url = request.args.get('url') or ''
    description = request.args.get('description') or ''

    if link_text and url and description:
      link_text = sanitize_alias(link_text)
      url = add_http(url)
      description = description.replace('"', '\'') 

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

      rows = []
      for row in all_rows:
          rows.append({
              'alias': row[1], 
              'url': row[2], 
              'description': row[3]})

      return render_template(
        'index.html',
        title='Golinks Server',
        rows=rows)
      return f'''
      Welcome to Sammy\'s golink server!
      <a href="create">Create a new link here.</a><br/>
      {enumerated_links}
      '''

    db = GolinksDatabase()
    url = db.select_url_by_link_text(path)
    if url:
      return redirect(url, code=302)
      
    return f'''
    go/{path} does not exist. <a href="create?link_text={path}">Create it?</a>
    '''
  
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
