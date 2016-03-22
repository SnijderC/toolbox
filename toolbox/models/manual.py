from common import CommonFields


class Manual(CommonFields):

    class Meta:

        """
            Change display of model in Django admin
        """
        app_label = "toolbox"
        verbose_name = "Handleiding"
        verbose_name_plural = "Handleidingen"

    def url_slug(self):
        """
            Return the item type slug of the model.
        """
        return "handleiding"
