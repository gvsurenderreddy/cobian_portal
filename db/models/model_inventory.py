from django.db import models


class ModelInventory(models.Model):
    user_profile = models.ForeignKey("UserProfile", related_name='model_inventory', null=True)
    model_sku = models.CharField("Model Sku", max_length=50, null=True)
    model_inventory = models.IntegerField("Model Inventory", null=False, default=0)
    inventory_sku = models.CharField("Inventory Sku", max_length=50, null=True)
    inventory = models.IntegerField("Inventory", null=False, default=0)
    replacement_sku = models.CharField("Replacement Sku", max_length=50, null=True)
    pending = models.IntegerField("Pending", null=False, default=0)
    threshold = models.IntegerField("Threshold", null=False, default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "{} - {}".format(self.pk, self.model_sku)

    def convert_to_dict(self):
        return {
            "id": self.pk,
            "dealerId": self.user_profile.pk,
            "modelSku": self.model_sku,
            "modelInventory": self.model_inventory,
            "inventorySku": self.inventory_sku,
            "inventory": self.inventory,
            "replacementSku": self.replacement_sku,
            "pending": self.pending,
            "threshold": self.threshold,
            "active": self.active,
        }
        
    class Meta:
        app_label = "db"
        verbose_name = "Model Inventory"
        verbose_name_plural = "Model Inventory"
        ordering = ["model_sku"]