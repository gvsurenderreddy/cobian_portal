from django.contrib import admin
from django.forms import TextInput
from django import forms
from db.models import *


# Forms
class UserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "{} - {} {}".format(obj.username, obj.first_name, obj.last_name)


class AccountRepChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "{} - {} {}".format(obj.account_id, obj.user.first_name, obj.user.last_name)


class DealerChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "{} - {} {}".format(obj.account_id, obj.user.first_name, obj.user.last_name)


class UserProfileForm(forms.ModelForm):
    user = UserChoiceField(queryset=User.objects.all().order_by('username'))
    account_rep = AccountRepChoiceField(queryset=UserProfile.objects.filter(user_type="REP").order_by('account_id'))

    class Meta:
        model = UserProfile
        exclude = []


class UserProfileDealerForm(forms.ModelForm):
    user_profile = DealerChoiceField(queryset=UserProfile.objects.filter(user_type="DEALER").order_by('account_id'))

    class Meta:
        model = UserProfile
        exclude = []


# Inlines
class MediaPlayerSlideInline(admin.TabularInline):
    model = MediaPlayerSlide
    ordering = ("sort_order", "title",)
    extra = 0
    fields = (
        "sort_order",
        "slide_type", 
        "video_code", 
        "media_file", 
        )


class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    ordering = ("sku",)
    extra = 0
    fields = (
        "quantity",
        "sku", 
        "item_number", 
        "style", 
        "description", 
        "size", 
        "upc", 
        "cost", 
        "price", 
        )


class UserProfileInline(admin.TabularInline):
    model = UserProfile
    ordering = ("account_id",)
    extra = 0
    verbose_name = "Dealer"
    verbose_name_plural = "Dealers"
    readonly_fields = (
        "account_id",
        "company", 
        )
    fields = (
        "account_id",
        "company", 
        )


class UserAddressInline(admin.TabularInline):
    model = UserAddress
    ordering = ("address_type",)
    extra = 0
    fields = (
        "address_type",
        "name",
        "address_id",
        "address1", 
        "address2", 
        "city", 
        "state", 
        "postal_code", 
        "country", 
        )


class BuyerInline(admin.TabularInline):
    model = Buyer
    ordering = ("buyer_type",)
    extra = 0
    fields = (
        "buyer_type",
        "name", 
        "phone", 
        "email",
        "not_available",
        )


class WarrantyHistoryInline(admin.TabularInline):
    model = WarrantyHistory
    ordering = ("action",)
    extra = 0
    can_delete = False
    readonly_fields = (
        "user_profile",
        "action",
        "action_date",
        )
    fields = (
        "user_profile",
        "action",
        "action_date",
        )


# Custom Admins
class DataOptionAdmin(admin.ModelAdmin):
    list_display = ("option_type", "description", "value", "sort_order", "active")
    list_filter = ("option_type",)
    ordering = ("option_type", "sort_order", "description",)
    search_fields = ("description", "value",)


class MediaFileAdmin(admin.ModelAdmin):
    list_display = ("thumbnail", "title", "file_name", "file_type",)
    list_filter = ("file_type", "file_extension",)
    ordering = ("title",)
    search_fields = ("title", "file_path",)
    fields = ("title", "file_type", "file_path", "description",)
    formfield_overrides = {
            models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        }


class MediaPlayerAdmin(admin.ModelAdmin):
    list_display = ("title", "audience", "enabled",)
    list_filter = ("audience", "enabled",)
    inlines = (MediaPlayerSlideInline,)


class MediaPlayerSlideAdmin(admin.ModelAdmin):
    list_display = ("title", "slide_type", "sort_order",)
    list_filter = ("media_player", "slide_type",)
    ordering = ("sort_order", "title",)
    search_fields = ("title",)


class MessageAdmin(admin.ModelAdmin):
    list_display = ("title", "message_type", "message_date", "enabled", )
    list_filter = ("message_type",)
    ordering = ("-message_date",)
    search_fields = ("title", )


class ModelInventoryAdmin(admin.ModelAdmin):
    form = UserProfileDealerForm


class OrderAdmin(admin.ModelAdmin):
    list_display = ("pk", "user_profile", "order_date", "status", "status_date", "prebook_date",)
    list_filter = ("user_profile", "status",)
    ordering = ("-order_date",)
    search_fields = ("id", "user_profile__company")
    inlines = (OrderDetailInline,)


class OrderSourceAdmin(admin.ModelAdmin):
    list_display = ("description", "value", "sort_order", "active")
    list_filter = ("description", "value")
    ordering = ("sort_order", "description",)
    search_fields = ("description", "value",)


class ProductItemAdmin(admin.ModelAdmin):
    list_display = ("item_number", "description", "available", "pk", )
    list_filter = ("product_style",)
    ordering = ("item_number",)
    search_fields = ("item_number", "description",)


class ProductSkuAdmin(admin.ModelAdmin):
    list_display = ("sku", "style", "description", "size", "wholesale", "active")
    list_filter = ("style", "description", "size", "active")
    ordering = ("sku",)
    search_fields = ("sku", "style", "description")


class ProductStyleAdmin(admin.ModelAdmin):
    list_display = ("style_sku", "style", )
    ordering = ("style_sku", "style", )
    search_fields = ("style_sku", "style", )


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("pk", "account_id", "company", "user_type", "terms_uploaded", "terms_accepted")
    list_filter = ("account_id", "company", "user_type", "terms_uploaded", "terms_accepted")
    search_fields = ("id", "account_id", "company")
    #readonly_fields = ("account_id", "user", "user_type", "account_rep", )
    ordering = ("account_id",)
    inlines = (UserAddressInline, UserProfileInline, BuyerInline)
    form = UserProfileForm


class WarrantyAdmin(admin.ModelAdmin):
    list_display = ("claim_number", "name", "status", "status_date", )
    ordering = ("claim_number", "name", "status", "status_date", )
    search_fields = ("claim_number", "name", "status", )
    list_filter = ("status",)
    inlines = (WarrantyHistoryInline,)
    #form = WarrantyHistoryForm


# Register
admin.site.register(DataOption, DataOptionAdmin)
admin.site.register(MediaFile, MediaFileAdmin)
admin.site.register(MediaPlayer, MediaPlayerAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(ModelInventory, ModelInventoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetail)
admin.site.register(OrderSource, OrderSourceAdmin)
admin.site.register(ProductItem, ProductItemAdmin)
admin.site.register(ProductSku, ProductSkuAdmin)
admin.site.register(ProductStyle, ProductStyleAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Warranty, WarrantyAdmin)
admin.site.register(WarrantyColor)
admin.site.register(WarrantyHistory)
admin.site.register(WarrantyImage)
admin.site.register(WarrantyStyle)
