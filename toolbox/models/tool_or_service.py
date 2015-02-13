# -*- coding: utf-8 -*-
from django.db import models
from common import CommonFields
  
class ToolOrService(CommonFields):
    
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
    
    """
        
        Until there is time for someone to make this a symmetrical m2m relation I think it should go.. 
        
            
        alt_services= models.ManyToManyField ( 
                                            'Service',
                                            verbose_name    = 'Alternatieve Dienst',
                                            related_name    = "%(class)s_alt_services",
                                            blank           = True
                                            )
    """                                          
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
        abstract = True