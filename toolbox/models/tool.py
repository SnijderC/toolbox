# -*- coding: utf-8 -*-
from django.db import models
from common import CommonFields
  
class Tool(CommonFields):
    
    # Risk Tuple
    RISK_TUPLE = (
                    ("L", "Laag"),
                    ("V", "Wees voorzichtig"),
                    ("H", "Hoog")
                )

    cost        = models.CharField   (
                                         verbose_name    = 'Prijs',
                                         max_length      = 40,
                                         blank           = True
                                     )
                                        
    url         = models.CharField   (      
                                        verbose_name    = 'Website',
                                        max_length      = 2000,
                                        blank           = True
                                     )
                                                           
    author      = models.CharField   (
                                        verbose_name    = 'Auteur',
                                        max_length      = 40,
                                        blank           = True
                                     )
                                                           
    author_url  = models.CharField   (
                                        verbose_name    = 'Website auteur',
                                        max_length      = 2000,
                                        blank           = True
                                     )
                                                                                                            
    license     = models.ForeignKey  (  
                                        'License',
                                        verbose_name    = 'Licentie',
                                        default         = None,
                                        blank           = True
                                     )
                                                                      
    pros        = models.ManyToManyField ( 
                                       'Property',
                                       verbose_name    = 'Voordeel',
                                       related_name    = "%(class)s_pros",
                                       blank           = True
                                     )
    cons        = models.ManyToManyField ( 
                                       'Property',
                                       verbose_name    = 'Nadeel',
                                       related_name    = "%(class)s_cons",
                                       blank           = True,
                                     )
    
    alternative = models.ManyToManyField( 
                                       'self',  # m2m on myself, if you are my friend I'm yours..
                                       blank           = True,
                                       verbose_name    = 'Alternatief'
                                       ) 
                                         
    risk        = models.CharField   (      
                                        verbose_name    = 'Privacy inbreuk risico',
                                        max_length      = 1,
                                        blank           = True,
                                        choices         = RISK_TUPLE
                                     )

    def is_free(self):
        """
            Return True if license is FOSS or 0 etc..

            Obviously this is not correct 100% of the time but you can add
            a asterisk or something to make your cost text not match one
            in the tuple below.
        """
        return self.cost in ("0", "Gratis", "Free", "FLOSS", "FOSS", "OSS")
    
    def format_cost(self):
        """
            Return the cost of the tool or service or GRATIS if it's free.
            
            Needs translation if this is going to be multilingual.. 
        """
        if self.is_free():
            cost = "GRATIS"
        else:
            cost = self.cost
        return cost    
    
    def risk_class(self):
        """
            Return the CSS classes that are associated with the risk level.
            
            This is done for simplicity in the templates..
        """
        if self.risk == "H":
            return "tb-eye risk high"
        elif self.risk == "V":
            return "tb-eye risk medium"
        else:
            return "tb-eye-blocked risk low"
    
    def risk_text(self):
        """
            Return the risk text that is associated with the risk level.
            
            This is done for simplicity in the templates..
            Needs translation if this is going to be multilingual.. 
        """
        if self.i_am() == "tool":
            str_tors = "tool"
        else:
            str_tors = "dienst"
        if self.risk == "H":
            return "Deze %s is niet privacy vriendelijk!" % str_tors
        elif self.risk == "V":
            return "Van deze %s is niet met zekerheid vast te stellen of hij privacy vriendelijk is." % str_tors
        else:
            return "Van deze %s is redelijk zeker dat hij privacy vriendelijk is." % str_tors
    
    class Meta:
        """
            Change display of model in Django admin
        """
        app_label = "toolbox"
        verbose_name = "Tools"
        verbose_name_plural = "Tools"
    
    def i_am(self):
        """ 
            Return the name of the model.
        """
        if hasattr(self,'app'):
            return 'app'
        else:
            return "tool"
        
class App(Tool):
    
    playstore  = models.CharField   (      
                                        verbose_name    = 'Playstore id',
                                        max_length      = 150,
                                        blank           = True,
                                        help_text       = "Vul het id in, niet een link dus: com.google.android.apps.maps"
                                     )
    
    appstore   = models.CharField   (      
                                        verbose_name    = 'Appstore',
                                        max_length      = 150,
                                        blank           = True,
                                        help_text       = "Vul het id in, niet een link dus: googlemaps"

                                     )
    marketplace= models.CharField   (      
                                        verbose_name    = 'Marketplace',
                                        max_length      = 150,
                                        blank           = True,
                                        help_text       = "Vul het id in, niet een link dus: c14e93aa-27d7-df11-a844-00237de2db9e"

                                     )

    def url_slug(self):
        """
            Return the item type slug of the model.
        """
        return "tools"
        
    def playstore_url(self):
        """
            Make a valid URL out of a playstore ID
        """
        return "http://play.google.com/store/apps/details?id=%s" % self.playstore
    
    def appstore_url(self):
        """
            Make a valid URL out of a appstore ID
        """
        return "http://appstore.com/%s" % self.appstore
   
    def marketplace_url(self):
        """
            Make a valid URL out of a marketplace ID
        """
        return "http://windowsphone.com/s?appId=%s" % self.marketplace
    
    def url_count(self):
        """
            Return the amount of filled in store ID's.
            
            This is done to simplify the templates.
        """
        
        count = 0
        for url in (self.playstore,self.appstore,self.marketplace,self.url):
            if url != "":
                count += 1
        return count
    
    class Meta:
        """
            Change display of model in Django admin
        """
        app_label = "toolbox"
        verbose_name = "Apps"
        verbose_name_plural = "Apps"

class Service(Tool):
    
    class Meta:
        """
            Change display of model in Django admin
        """
        app_label = "toolbox"
        verbose_name = "Diensten"
        verbose_name_plural = "Diensten"
    