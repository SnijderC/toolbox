from uuid import uuid4
import re


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


def fix_anchor_abbr(str_html):
    """
        Markdown automatically generates links.
        Markdown automatically generates <abbr> tags for wordlists (add-on).

        In the toolbox we now use popovers for <abbr> tags.
        It looks pretty bad when these show up wrapped inside links..

        Preventing it from happening seems pretty hard so to hack around this
        issue I remove the <abbr...><abbr> with regex magic.
        The pattern: (<a(?![a-z]).*?>.*?)<abbr.*>(.*)</abbr>(.*?</a>)

        It consists of multiple groups:
         1. (<a(?![a-z]).*?>.*?)
         x  <abbr.*>
         2. (.*)
         x  </abbr>
         3. (.*?</a>)

        1. Grabs the start of the anchor and it's contents up to the start of
           the <abbr> tag.
        x  <abbr.*> should be discarded
        2. Captures anything inside the <abbr> tag (that should not be lost).
        x  </abbr> is the end of the <abbr> tag and should be discarded
        3. Is the last bit of text before the anchor is closed, including the
           anchor's closing tag.

        Replacement string is simply all capturing groups combined.

        This should be cached because it may be CPU intensive.
    """

    return re.sub(
        r"(<a(?![a-z]).*?>.*?)<abbr.*>(.*)</abbr>(.*?</a>)",
        "\\1\\2\\3",
        str_html,
        flags=re.MULTILINE
    )
