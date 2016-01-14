from django.conf.urls import patterns

urlpatterns = patterns('api.views',
    (r'^api/dealers/$', 'api_dealers'),
    (r'^api/dealers/(?P<dealer_id>\d+)$', 'api_dealer'),
    
    (r'^api/documents/(?P<doc_type>[\w\-]+)/$', 'get_document_list'),
    (r'^api/documents/(?P<doc_type>[\w\-]+)/(?P<doc_sys_no>\d+)/$', 'get_document'),
    
    (r'^api/ebridge/documents/$', 'ebridge_documents'),
    (r'^api/ebridge/document/$', 'ebridge_document'),

    (r'^api/email/test/$', 'email_test'),

    (r'^api/inventory/$', 'api_inventory'),
    
    (r'^api/model/inventory/(?P<dealer_id>\d+)/create/$', 'api_model_inventory_create'),
    (r'^api/model/inventory/(?P<dealer_id>\d+)$', 'api_model_inventory_list'),
    (r'^api/model/inventory/(?P<dealer_id>\d+)/(?P<model_inventory_id>\d+)/$', 'api_model_inventory'),
    
    (r'^api/order/duplicate/$', 'api_order_duplicate'),
    (r'^api/order/(?P<order_id>\d+)/email', 'api_order_email'),
    (r'^api/order/new/$', 'api_order_new'),
    (r'^api/order/prebook/options/$', 'api_order_prebook_options'),
    (r'^api/order/sources/$', 'api_order_sources'),
    
    (r'^api/orders/$', 'api_orders'),
    (r'^api/orders/(?P<order_id>\d+)/$', 'api_order'),
    (r'^api/orders/(?P<order_id>\d+)/data/$', 'api_order_data'),
    (r'^api/orders/(?P<order_id>\d+)/details/$', 'api_order_details'),
    (r'^api/orders/(?P<order_id>\d+)/details/(?P<order_detail_id>\d+)/$', 'api_order_detail'),
    (r'^api/orders/(?P<order_id>\d+)/save/$', 'api_order_save'),
    (r'^api/orders/(?P<order_id>\d+)/submit/$', 'api_order_submit'),
    
    (r'^api/product/styles/$', 'api_product_styles'),
    (r'^api/product/styles/(?P<product_style_id>\d+)/$', 'api_product_style'),
    (r'^api/product/styles/(?P<product_style_id>\d+)/detail/$', 'api_product_style_detail'),
    
    (r'^api/product/items/(?P<product_style_id>\d+)/$', 'product_item_list'),
    (r'^api/product/items/grid/(?P<product_style_id>\d+)/$', 'product_item_grid'),
    (r'^api/product/skus/(?P<product_item_id>\d+)/$', 'product_sku_list'),
    
    (r'^api/reps/$', 'api_reps'),
    (r'^api/reps/(?P<rep_id>\d+)$', 'api_rep'),
    
    (r'^api/user_profiles/$', 'api_user_profiles'),
    (r'^api/user_profiles/(?P<user_profile_id>\d+)/$', 'api_user_profile'),
    (r'^api/user_profiles/(?P<user_profile_id>\d+)/addresses/$', 'api_user_profile_addresses'),
    (r'^api/user_profiles/(?P<user_profile_id>\d+)/addresses/(?P<user_address_id>\d+)/$', 'api_user_profile_address'),
    
    (r'^api/user_profile/terms/$', 'user_profile_terms'),
    (r'^api/user_profile/term/$', 'user_profile_term'),
)

urlpatterns += patterns('api.warranty',
    (r'^api/warranties/$', 'api_warranties'),
    (r'^api/warranties/(?P<warranty_id>\d+)/$', 'api_warranties_warranty'),
    (r'^api/warranty/colors/$', 'api_warranty_colors'),
    (r'^api/warranty/defects/$', 'api_warranty_defects'),
    (r'^api/warranty/styles/$', 'api_warranty_styles'),
    (r'^api/warranty/(?P<warranty_id>\d+)/$', 'api_warranty'),
    (r'^api/warranty/(?P<warranty_id>\d+)/history/$', 'api_warranty_history'),
    (r'^api/warranty/(?P<warranty_id>\d+)/status/$', 'api_warranty_status'),
    (r'^api/warranty/(?P<warranty_id>\d+)/images/$', 'api_warranty_images'),
    (r'^api/warranty/(?P<warranty_id>\d+)/images/(?P<warranty_image_id>\d+)/$', 'api_warranty_images_image'),

    (r'^api/warranty/create/claims/$', 'api_warranty_create_claims'),
    (r'^api/warranty/create/data/$', 'api_warranty_create_data'),
)

urlpatterns += patterns('api.report',
    (r'^api/report/warranty/$', 'api_report_warranty'),
    (r'^api/report/test/$', 'api_report_test'),
)