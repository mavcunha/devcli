import os

CONFIG_DIRECTORY = os.environ.get("DEVCLI_CONFIG_DIRECTORY",
                                  os.path.join(os.environ.get("HOME"), ".devcli"))


# generic get this project root path
def project_root(filename=None):
    parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if filename is None:
        return parent
    else:
        return os.path.join(parent, filename)


def config_path(filename):
    if os.path.exists(CONFIG_DIRECTORY):
        return os.path.join(os.path.abspath(CONFIG_DIRECTORY), filename)
    else:
        return os.path.join(project_root("conf"), filename)
