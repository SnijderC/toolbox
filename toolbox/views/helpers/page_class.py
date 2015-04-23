import settings
from copy import deepcopy

class Page(object):
    """
        This is just a class that holds specific information about a page.
        
        It holds some variables and makes it slightly easier to access them:
        e.g.: page.title vs page['title']
    """
    def __init__(self):
        self.data = {}
        self.debug = settings.DEBUG
        self.index = True
        self.title = ""
        self.show_filters = False
        self.playlist = False
        self.meta = deepcopy(settings.meta_tags)
