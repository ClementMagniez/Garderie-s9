from django.urls import path
from django.contrib.auth.decorators import permission_required
from . import views

url_admin=[
        path('admin/tauxhoraire/', views.NewHourlyRateView.as_view(), name='hourly_rate_form'),
        path('admin/factures/', views.BillsListView.as_view(), name='bills_list'),
        path('admin/staff/add/', views.NewStaffView.as_view(), name='add_staff'),
        path('admin/staff/', views.StaffListView.as_view(), name='staff_list'),
        path('parent/', views.ParentListView.as_view(), name='parent_list'),
        path('parent/add/', views.NewUserView.as_view(), name='add_parent'),
        path('admin/user/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
        path('admin/password-reset/', views.ResetPasswordView.as_view(), name='password_reset_form'),
        path('admin/settings/', views.EditConfigView.as_view(), name='edit_config'),

]
url_parent=[
        path('parent-redirect/', views.ParentRedirectView.as_view(), name='parent_index'),
        path('parent/<int:pk>/', views.ParentProfileView.as_view(), name='parent_profile'),
        path('parent/<int:pk>/create_child/', views.ParentCreateChildView.as_view(), name='parent_create_child'),
        path('parent/<int:pk>/create_reliable/', views.CreateReliableView.as_view(), name='parent_create_reliable'),
        path('parent/<int:pk>/update/', views.ParentUpdateView.as_view(), name='parent_update'),
        path('parent/<int:pk>/delete_reliable/', views.ParentDeleteReliableView.as_view(), name='reliable_person_delete'),
]

url_enfant=[
        path('enfant/', views.ChildrenListView.as_view(), name='children_list'),
        path('enfant/add/', views.NewChildView.as_view(), name='add_child'),
        path('enfant/<int:pk>/', views.ChildProfileView.as_view(), name='child_profile'),
        path('enfant/<int:pk>/update/', views.ChildUpdateView.as_view(), name='child_update'),
        path('enfant/<int:pk>/delete/', views.ChildDeleteView.as_view(), name='child_delete'),
        path('enfant/<int:pk>/presence/register/', views.CreatePresenceView.as_view(), name='schedule_register'),
        path('enfant/<int:fk>/presence/<int:pk>/delete/', views.PresenceDeleteView.as_view(), name='presence_delete'),
        path('enfant/<int:fk>/schedule/<int:pk>/delete/', views.ScheduleDeleteView.as_view(), name='schedule_delete'),
        path('enfant/schedule/<int:pk>/edit/', views.EditScheduleView.as_view(), name='schedule_edit'),
]

url_ajax=[
        path('ajax/enter_hour_arrival/', views.AjaxChildCreateArrival, name='ajax_arrival'),
        path('ajax/enter_hour_departure/', views.AjaxChildCreateDeparture, name='ajax_departure'),
        path('ajax/edit_hour_arrival/', views.AjaxChildEditArrival, name='ajax_edit_arrival'),
        path('ajax/edit_hour_departure/', views.AjaxChildEditDeparture, name='ajax_edit_departure'),
        path('ajax/remove_arrival/', views.AjaxChildRemoveArrival, name='ajax_remove_arrival'),
        path('ajax/show_schedule_form_modal/', views.AjaxShowScheduleFormModal, name='ajax_show_schedule_form_modal'),
        path('ajax/children_here/', views.AjaxShowChildrenHereThisDay, name='ajax_children_here_day'),
        path('ajax/bills/admin/modal/', views.AjaxShowBillsModalAdmin, name='ajax_show_bill_modal'),
        path('ajax/bills/admin/display/', views.AjaxSwapDisplayBillsAdmin, name='ajax_swap_bills_display'),
        path('ajax/bills/admin/recap/', views.AjaxShowRecapPresence, name='ajax_show_recap'),
        path('ajax/bills/parent/display/', views.AjaxSwapDisplayBillsParent, name='ajax_swap_bills_parent'),
        path('ajax/bills/parent/modal/', views.AjaxShowBillsModalParent, name='ajax_show_bill_modal_parent'),
]


url_redirect=[
        path('index-redirect/', views.IndexRedirectView.as_view(), name='index_redirect'),
        path('admin/accueil/', views.AdminIndexView.as_view(), name='admin_index'),
        path('educ-redirect/', views.EducRedirectView.as_view(), name='educ_index'),
]


urlpatterns = [ 
        path('', views.HomeRedirectView.as_view(), name='home_redirect'),
        path('help/', views.HelpView.as_view(), name='help'),
] + url_admin + url_parent + url_enfant + url_ajax + url_redirect

