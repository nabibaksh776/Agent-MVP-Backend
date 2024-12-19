# urls.py

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView
from .views import HANDLE_CUSTOMER,LoginCustomer,CREATE_AGENTS,VISITOR_VIEW_CLASS,SALES_TECHNIQUES,CHAT_CLASS,UpdteCustomer,CreateCustomer,ADMIN_MANAGE,HandleCurrentUser,LogoutView,AdminManageAgents,UpdateAgentByAdmin,ManageAgentDocx
urlpatterns = [
    path('current_user/', HandleCurrentUser.as_view(), name="createCustomer"),
    path('customer/', HANDLE_CUSTOMER.as_view(), name="createCustomer"),
    path('customer/<int:customer_id>/', HANDLE_CUSTOMER.as_view(), name="getCustomer"),
    path('customer/update/<int:customer_id>/', UpdteCustomer.as_view(), name="update-customer"),
    path('customer/create/', CreateCustomer.as_view(), name="RegisterUser"),
    path('login/', LoginCustomer.as_view(), name="loginUser"),
    path('agent/', CREATE_AGENTS.as_view(), name="createAgent"),
    path('agent/<int:agent_id>/', CREATE_AGENTS.as_view(), name="getAgent"),
    path('visitor/', VISITOR_VIEW_CLASS.as_view(), name="get_visitors"),
    path('visitor/<int:visitor_id>/', VISITOR_VIEW_CLASS.as_view(), name="get_single_visitors"),
    path('sales-techniques/', SALES_TECHNIQUES.as_view(), name="sales_techniques"),
    path('sales-techniques/<int:technique_id>/', SALES_TECHNIQUES.as_view(), name="getSingleSalesTechniques"),
    path('chat/', CHAT_CLASS.as_view(), name="chat"),
    path('chat/<int:chat_id>/', CHAT_CLASS.as_view(), name="getchats"),
    path('admin/', ADMIN_MANAGE.as_view(), name="admin_manage"),
    path('admin/<int:admin_id>/', ADMIN_MANAGE.as_view(), name="admin_manage"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='loguot'),


    # admin Routes 
    path('admin/agents/<int:customer_id>/', AdminManageAgents.as_view(), name='getAllAgentsByCustomer'),
    path('admin/agents/', AdminManageAgents.as_view(), name='CreateAgents'),
    path('admin/agents/v2/<int:agent_id>/', UpdateAgentByAdmin.as_view(), name='editAgent'),
    path('admin/agentdocs/v2/<int:doc_id>/', ManageAgentDocx.as_view(), name='manageAgentDocx'),
    path('admin/agentdocs/v2/', ManageAgentDocx.as_view(), name='manageAgentDocx'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)