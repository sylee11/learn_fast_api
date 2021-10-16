import sys
from pathlib import Path

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.app.app_factory import create_app, db
from src.app.repository.tables import *


app = create_app()
migrate = Migrate(app, db, compare_type=True)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
