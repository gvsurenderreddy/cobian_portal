from django.db import models


class OrderLog(models.Model):
    order = models.ForeignKey("Order", verbose_name="Order", related_name='order_logs', blank=True, null=True)
    user_profile = models.ForeignKey("UserProfile", verbose_name="User Profile", related_name='order_logs', blank=True, null=True)
    log_date = models.DateTimeField(auto_now_add=True)
    log = models.TextField("Log", blank=True, null=True)

    def __str__(self):
        return "Order #{} - {}: {}".format(self.order.pk, self.log_date, self.log)
        
    class Meta:
        app_label = "db"
        verbose_name = "Order Log"
        verbose_name_plural = "Order Logs"
        ordering = ["log_date"]