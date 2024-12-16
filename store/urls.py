from django.urls import path
import store.views


urlpatterns = [
    path('',store.views.index,name='index'),
    path('index',store.views.index,name='index'),
    path('user_home',store.views.user_home,name='user_home'),
    path('admin_home',store.views.admin_home,name='admin_home'),
    path('about',store.views.about,name='about'),
    path('admin_reg',store.views.admin_reg,name='admin_reg'),
    path('user_reg',store.views.user_reg,name='user_reg'),  
    path('delivery_boy_reg', store.views.delivery_boy_reg, name='delivery_boy_reg'),
    path('login',store.views.log,name='login'),
    path('logout',store.views.logout,name='logout'),
    path('add_category',store.views.add_category,name='add_category'), 
    path('demo_category',store.views.demo_category,name='demo_category'), 
    path('category',store.views.category,name='category'),
    path('demo_products/<cat_id>', store.views.demo_products,name='demo_products'),
    path('products/<cat_id>', store.views.products, name='products'),
    path('add_products/<cat_id>', store.views.add_products, name='add_products'),
    path('product_edit/<hy>',store.views.product_edit, name='product_edit'),
    path('product_delete/<hy>',store.views.product_delete, name='product_delete'),
    path('user_category',store.views.user_category,name='user_category'),
    path('user_products/<cat_id>', store.views.user_products, name='user_products'),
    path('add_to_cart/<int:product_id>/', store.views.add_to_cart, name='add_to_cart'),
    path('cart', store.views.cart, name='cart'),
    path('remove_from_cart/<int:item_id>/', store.views.remove_from_cart, name='remove_from_cart'),
    path('update_cart/<int:item_id>/', store.views.update_cart, name='update_cart'),
    path('checkout',store.views.checkout, name='checkout'),
    path('order_success',store.views.order_success, name='order_success'),
    path('orders_list', store.views.orders_list, name='orders_list'),
    path('order_history',store.views.order_history, name='order_history'),
    path('search',store.views.search, name='search'),
    path('user_search',store.views.user_search, name='user_search'),
    path('suggestion', store.views.suggestion, name='suggestion'),
    path('rate_product/<int:order_id>/<int:product_id>/', store.views.rate_product, name='rate_product'),
    path('rate_success',store.views.rate_success, name='rate_success'),
    path('user/profile/<str:username>/', store.views.user_profile, name='user_profile'),
    path('user/profile/update_username', store.views.update_username, name='update_username'),
    path('user/profile/update_email', store.views.update_email, name='update_email'),
    path('change-password/', store.views.change_password, name='change_password'),
    path('add_address/', store.views.add_address, name='add_address'),
    path('add_new_address/', store.views.add_new_address, name='add_new_address'),
    path('edit_address/<int:address_id>/', store.views.edit_address, name='edit_address'),
    path('remove_address/<int:address_id>/', store.views.remove_address, name='remove_address'),
    path('delivery_boy_home', store.views.delivery_boy_home, name='delivery_boy_home'),
    path('update_status/<str:status>/', store.views.update_status, name='update_status'),
    path('assign_delivery_boy/<int:order_id>/', store.views.assign_delivery_boy, name='assign_delivery_boy'),
    path('assigned-orders/', store.views.assigned_orders_list, name='assigned_orders_list'),
    path('update-delivery-boy-location/', store.views.update_delivery_boy_location, name='update_delivery_boy_location'),
    path('delivery-boy-details/', store.views.delivery_boy_details, name='delivery_boy_details'),
    path('track-delivery/<int:order_id>/', store.views.track_delivery, name='track_delivery'),
    path('api/live-distance/<int:order_id>/', store.views.get_live_distance, name='get_live_distance'),
    path('order/<int:order_id>/', store.views.order_detail, name='order_detail'),
    

 
    

 

    

    

  

   


   

    
    


   

  
  

]
