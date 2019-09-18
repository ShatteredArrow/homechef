from app import app, db
from app.models import Recipe, Tag

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'recipe': Recipe, 'tag': Tag}