from filer.models.imagemodels import Image as FilerImage
import markdown, re
from markdown_extensions import BootstrapTabExtension
from django.db import models

class ToolboxMD(markdown.Markdown):
    
    bs_tab_ext = BootstrapTabExtension()
    std_extensions=[
                    'markdown.extensions.extra',
                    'markdown.extensions.nl2br',
                    'markdown.extensions.smarty',
                    'markdown.extensions.toc', 
                    bs_tab_ext,
                   ]
    def __init__(self, extensions=std_extensions, cached_wordlist=True, output_format='html5'):
        # pattern for  filter_abbr_anchored()
        self.abbr_anchor_pat    = re.compile(r"(<a(?![a-z]).*?>.*?)<abbr.*>(.*)</abbr>(.*?</a>)",flags=re.MULTILINE)
        # pattern for process_inline_images()
        self.inline_img_pat     = re.compile(r'(?<!\\)\!(?:\[.*\])?\[([a-zA-Z0-9\-\+\_\.\ ]{4,200})\]')
        self.cached_wordlist    = cached_wordlist
        self.wordlist = None
        
        super(ToolboxMD, self).__init__(extensions,output_format=output_format)
                
    def generate_wordlist(self, topics):
        
        terms_model = models.get_model('toolbox', 'Terms')
        
        wordlist = "\n"
        for term_obj in terms_model.objects.all():
            terms = term_obj.term.split(";")
            for term in terms:
                if term not in topics:
                    wordlist += "*[%s]: %s\n" % (term, term_obj.description_html)
        return wordlist
        
    def convert(self, str_markdown, topics=[]):
        '''
            Generic function for converting MD to HTML.
            
            Functions tasks:
            - Convert MD to HTML
            - Find all terms in the terms list and generate the MD code to make popovers with explanations.
            - Find all popovers that would have been placed inside of url's and filter them out of them (HTML):

        '''
        if self.cached_wordlist:
            if self.wordlist == None or self.topics != topics:
                self.topics = topics
                self.wordlist = self.generate_wordlist(topics)
            wordlist = self.wordlist
        else:
            wordlist = self.generate_wordlist(topics)
        
        return self.filter_abbr_anchored(super(ToolboxMD, self).convert(str_markdown+self.wordlist).encode("utf-8"))
    
    def process_inline_images(self,str_md):
        """
            Place filer images in markdown code
            
            FOR EVERY: ![Alt text][id] OR ![id]
            ADD      : [id]: url/to/image  "Optional title attribute"
            
            
            
            Pattern: /(?<!\\)\!(?:\[.*\])?\[([a-zA-Z0-9\-\+\_\.\ \]{4,200})\]/
            Finds what is between in the [id] block only, alt text is ignored.
            Alt text can contain anything except likebreaks.
            ID's can contain [ a-Z 0-9 - + _ . ] and space, min 4, max 200 tekens.    
            
        """

        # Items to be added..
        arr_images = re.findall(self.inline_img_pat,str_md)
        str_img = ""
        errors = ""
        for image in arr_images:
            fi = FilerImage.objects.filter(name=image)
            if len(fi) > 0:
                str_img += "\n[%s]: %s  \"%s\"\n" % (image, fi.first().url, fi.first().default_caption) 
            else:
                errors += "No file found for %s.\n" % image
        if len(errors) > 0:
            raise ValidationError(errors.strip("\n"))
        else:
            return str_img 
            
    
    def filter_abbr_anchored(self, str_html):
        '''
            Markdown automatically generates links.
            Markdown automatically generates <abbr> tags for wordlists (add-on).
            
            In the toolbox we now use popovers for <abbr> tags. 
            It looks pretty bad when these show up wrapped inside links..
            
            Preventing it from happening seems pretty hard so to hack around this issue I remove the 
            <abbr...><abbr> with regex magic.
            The pattern: (<a(?![a-z]).*?>.*?)<abbr.*>(.*)</abbr>(.*?</a>)
            
            It consists of multiple groups:
             1. (<a(?![a-z]).*?>.*?)
             x  <abbr.*>
             2. (.*)
             x  </abbr>
             3. (.*?</a>)
             
            1. Grabs the start of the anchor and it's contents up to the start of the <abbr> tag.
            x  <abbr.*> should be discarded
            2. Captures anything inside the <abbr> tag (that should not be lost).
            x  </abbr> is the end of the <abbr> tag and should be discarded
            3. Is the last bit of text before the anchor is closed, including the anchor's closing tag.
            
            Replacement string is simply all capturing groups combined.
        '''
            
        return re.sub(self.abbr_anchor_pat, "\\1\\2\\3", str_html)