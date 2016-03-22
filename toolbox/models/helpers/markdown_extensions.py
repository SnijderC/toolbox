"""
Bootstrap TAB's for Markdown
=========================================

This extension provides a conversion from this format:

/ Tab 1\_________
|Contents of tab 1
___/Tab 2\_______
|Contents of tab 2

__/Tab 2\___
|sloppy^formatted


to....:

<div role="tabpanel">
    <ul class="nav nav-tabs" role="tablist">
        <li class="active" role="presentation">
            <a aria-controls="tab1" data-toggle="tab" href="#tab1" role="tab">
                Tab 1
            </a>
        </li>
        <li role="presentation">
            <a aria-controls="tab2" data-toggle="tab" href="#tab2" role="tab">
                Tab 2
            </a>
        </li>
        <li role="presentation">
            <a aria-controls="tab2-1" data-toggle="tab" href="#tab2-1" role="tab">
                Tab 2
            </a>
        </li>
    </ul>
    <div class="tab-content">
        <div class="tab-pane active" id="tab1" role="tabpanel">
            <p>Contents of tab 1</p>
        </div>
        <div class="tab-pane active" id="tab2" role="tabpanel">
            <p>Contents of tab 2</p>
        </div>
        <div class="tab-pane active" id="tab2-1" role="tabpanel">
            <p>sloppy^formatted</p>
        </div>
    </div>
</div>

Dependencies:
* [Python 2.4+](http://python.org)
* [Markdown 2.0+](http://packages.python.org/Markdown/)

USAGE EXAMPLE (requires extension "extra" for the code block!):

import markdown
import markdown_extensions
myext = markdown_extensions.BootstrapTabExtension()
md = markdown.Markdown(extensions=[myext,'extra'])
print md.convert('''
/ Tab 1\_________
|Contents of tab 1
___/Tab 2\_______
|Contents of tab 2

__/Tab 2\___
|sloppy^formatted
''')


"""

from markdown.extensions import Extension
from markdown.blockprocessors import BlockProcessor
from markdown.util import etree
import re


class BootstrapTabBlockProcessor(BlockProcessor):

    # Detect tab sections
    MATCH_RE = re.compile(r'[_]{0,77}\/([\w\W]*?)\\[_]{3,74}((?:\r?\n\|.*)*)')
    SLUG_RE = re.compile(r'[^a-zA-Z0-9\-]')

    uq_list = []

    def test(self, parent, block):
        return bool(self.MATCH_RE.search(block))

    def run(self, parent, blocks):

        sibling = self.lastChild(parent)
        first = False

        if (sibling is not None and
                sibling.tag == "div" and sibling.get("role") == "tabpanel"):
            # The last child was a tabblock, append this block to the tab
            # block.

            # loop through the parent's children to locate the tablist (ul) and
            # the tab-content (div)
            for ul in sibling.findall("ul"):
                if ul.get("class") == "nav nav-tabs":
                    tablist = ul
            for div in sibling.findall("div"):
                if div.get("class") == "tab-content":
                    tabcontent = div

        else:
            # Add a new tab block
            tabblock = etree.SubElement(parent, 'div', role="tabpanel")
            tablist = etree.SubElement(
                tabblock, 'ul', **{'role': "tablist", 'class': "nav nav-tabs"})
            tabcontent = etree.SubElement(
                tabblock, 'div', **{'class': "tab-content"})

            # self.uq_list = []

            first = True

        block = blocks.pop(0)
        # blocks may be attached (no newline)
        for m in re.finditer(self.MATCH_RE, block):
            list_kw = {'role': "presentation"}
            div_kw = {'role': "tabpanel", 'class': "tab-pane"}
            if first:
                list_kw['class'] = "active"
                div_kw['class'] = "tab-pane active"
                first = False

            uq_id = re.sub(self.SLUG_RE, "", m.group(1)).strip("-").lower()
            iteration = 0
            while uq_id in self.uq_list:
                uq_id = uq_id.rstrip("-%s" % iteration)
                iteration += 1
                uq_id = "%s-%s" % (uq_id, iteration)

            self.uq_list.append(uq_id)
            div_kw['id'] = uq_id

            a_kw = {'href': "#%s" % uq_id, 'aria-controls': uq_id,
                    'role': "tab", 'data-toggle': "tab"}

            listitem = etree.SubElement(tablist, "li", **list_kw)
            a = etree.SubElement(listitem, "a", **a_kw)
            a.text = m.group(1)

            content = etree.SubElement(tabcontent, "div", **div_kw)

            self.parser.parseChunk(content, m.group(2).replace("\n|", "\n"))


class BootstrapTabExtension(Extension):

    def extendMarkdown(self, md, md_globals):
        """ Add BootstrapTabBlockParser to the Markdown instance. """
        # md.registerExtension(self)

        md.parser.blockprocessors.add(
            'bootstrap_tab', BootstrapTabBlockProcessor(md.parser), "<hr")


def makeExtension(configs=None):
    return BootstrapTabExtension(configs=configs)
