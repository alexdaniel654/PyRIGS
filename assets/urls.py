from django.conf.urls import url
from django.urls import path
from assets import views, models
from RIGS import versioning

from django.contrib.auth.decorators import login_required
from django.views.decorators.clickjacking import xframe_options_exempt
from PyRIGS.decorators import has_oembed, permission_required_with_403

urlpatterns = [
    path('', login_required(views.AssetList.as_view()), name='asset_index'),
    path('asset/list/', login_required(views.AssetList.as_view()), name='asset_list'),
    path('asset/id/<str:pk>/', has_oembed(oembed_view="asset_oembed")(views.AssetDetail.as_view()), name='asset_detail'),
    path('asset/create/', permission_required_with_403('assets.add_asset')
         (views.AssetCreate.as_view()), name='asset_create'),
    path('asset/id/<str:pk>/edit/', permission_required_with_403('assets.change_asset')
         (views.AssetEdit.as_view()), name='asset_update'),
    path('asset/id/<str:pk>/duplicate/', permission_required_with_403('assets.add_asset')
         (views.AssetDuplicate.as_view()), name='asset_duplicate'),
    path('asset/id/<str:pk>/history/', permission_required_with_403('assets.view_asset')(views.AssetVersionHistory.as_view()),
         name='asset_history', kwargs={'model': models.Asset}),
    path('activity', permission_required_with_403('assets.view_asset')
         (views.ActivityTable.as_view()), name='asset_activity_table'),

    path('cabletype/list/', permission_required_with_403('assets.view_cable_type')(views.CableTypeList.as_view()), name='cable_type_list'),
    path('cabletype/create/', permission_required_with_403('assets.add_cable_type')(views.CableTypeCreate.as_view()), name='cable_type_create'),
    path('cabletype/<int:pk>/update/', permission_required_with_403('assets.change_cable_type')(views.CableTypeUpdate.as_view()), name='cable_type_update'),
    path('cabletype/<int:pk>/detail/', permission_required_with_403('assets.view_cable_type')(views.CableTypeDetail.as_view()), name='cable_type_detail'),

    path('asset/search/', views.AssetSearch.as_view(), name='asset_search_json'),
    path('asset/id/<str:pk>/embed/',
         xframe_options_exempt(
                               login_required(login_url='/user/login/embed/')(views.AssetEmbed.as_view())),
         name='asset_embed'),
    path('asset/id/<str:pk>/oembed_json/',
         views.AssetOembed.as_view(),
         name='asset_oembed'),

    path('asset/audit/', permission_required_with_403('assets.change_asset')(views.AssetAuditList.as_view()), name='asset_audit_list'),
    path('asset/id/<str:pk>/audit/', permission_required_with_403('assets.change_asset')(views.AssetAudit.as_view()), name='asset_audit'),

    path('supplier/list', views.SupplierList.as_view(), name='supplier_list'),
    path('supplier/<int:pk>', views.SupplierDetail.as_view(), name='supplier_detail'),
    path('supplier/create', permission_required_with_403('assets.add_supplier')
         (views.SupplierCreate.as_view()), name='supplier_create'),
    path('supplier/<int:pk>/edit', permission_required_with_403('assets.change_supplier')
         (views.SupplierUpdate.as_view()), name='supplier_update'),
    path('supplier/<int:pk>/history/', views.SupplierVersionHistory.as_view(),
         name='supplier_history', kwargs={'model': models.Supplier}),

    path('supplier/search/', views.SupplierSearch.as_view(), name='supplier_search_json'),
]