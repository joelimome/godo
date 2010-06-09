
# Show that lib is on path.

import blammo

@task
def ping():
    assert blammo.runner() == 3
