# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from tool_or_service import ToolOrService
import re
  
class Tool(ToolOrService):
    
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
        
    def i_am(self):
        """ 
            Return the name of the model.
        """
        return "tool"

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
        verbose_name = "Tools"
        verbose_name_plural = "Tools"