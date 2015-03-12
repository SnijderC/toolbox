# -*- coding: utf-8 -*-
from django.db import models
from terms import Terms
import re, markdown

class GenericFields(models.Model):


    slug        = models.CharField   (     
                                         verbose_name    = 'Slug',
                                         max_length      = 60,
                                         help_text       = "slug"
                                     )

    def save(self, *args, **kw):
        
        #make slug..
        self.slug = re.sub("[^a-zA-Z0-9\-]","-",self.slug).strip("-").lower()
        
        super(GenericFields, self).save(*args, **kw)

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
        pat = re.compile(r'(?<!\\)\!(?:\[.*\])?\[([a-zA-Z0-9\-\+\_\.\ ]{4,200})\]')
        arr_images = re.findall(pat,str_md)
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
            
    def cache_md(self, arr_markdown, arr_extensions=['extra','nl2br','smarty', 'toc']):
        '''
            Generic function for caching HTML from MD files.
        '''
        # Set md object
        md = markdown.Markdown(arr_extensions,output_format='html5')
        
        # Cache wordlist
        wordlist = "\n"
        for term_obj in Terms.objects.all():
            terms = term_obj.term.split(";")
            if "topic" in self.__dict__:
                topics = self.topic.split(";")
            else:
                topics = []
            for term in terms:
                if term not in topics:
                    wordlist += "*[%s]: %s\n" % (term, term_obj.description_html)
        arr_return=[]
        for str_md in arr_markdown:        
            arr_return.append(md.convert(str_md+wordlist).encode("utf-8"))
            return arr_return

    class Meta:
        """
            Change display of model in Django admin
        """ 
        app_label = "toolbox"
        abstract = True