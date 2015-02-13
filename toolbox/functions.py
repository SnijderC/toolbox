from uuid import uuid4

def randomized_file(instance, filename, path=""):
    """
        A good way to rename image uploads to [path]/[UUID].[ext].
    """ 
    ext = filename.split('.')[-1]
    # set filename as random string
    filename = '{}.{}'.format(uuid4().hex, ext)
    # return the filename
    return path + filename


def path_and_rename(path):
    """
        Was used for Django's built-in image-types, not in use now.
    """
    def wrapper(instance, filename):
        return randomized_file(instance, filename, path) 
    return wrapper