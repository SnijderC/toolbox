# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from tool_or_service import ToolOrService
import re
  
class Service(ToolOrService):
            
    def i_am(self):
        """ 
            Return the name of the model.
        """
        return "service"

    def url_slug(self):
        """
            Return the item type slug of the model.
        """
        return "diensten"

    class Meta:
        """
            Change display of model in Django admin
        """
        app_label = "toolbox"
        verbose_name = "Dienst"
        verbose_name_plural = "Diensten"