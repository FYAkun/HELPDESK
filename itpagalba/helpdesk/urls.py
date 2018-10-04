from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # ex: /helpdesk/
    url(r'^$', views.neatlikti, name='neatlikti'),
    # ex: /helpdesk/visi/
    url(r'^visi/$', views.visi, name='visi'),
    # ex: /helpdesk/atlikti/
    url(r'^atlikti/$', views.atlikti, name='atlikti'),
    # ex: /helpdesk/tipai/5 su regex paimame tipas_id, kad panaudotume tarp view
    url(r'^tipai/(?P<tipas_id>[0-9]+)/$', views.perziura_tipai, name='perziura_tipai'),
    # ex: /helpdesk/irasai/5 su regex paimame irasas_id, kad panaudtume tarp view
    url(r'^irasai/(?P<irasas_id>[0-9]+)/$', views.perziura_vienas, name='perziura_vienas'),
    # ex: /helpdesk/naujas/
    url(r'^naujas/$', views.naujas, name='naujas'),
    # ex: /helpdesk/prisijungimas/
    url(r'^vart_kurimas/$', views.nvartotojas, name='nvartotojas'),
    # ex: /helpdesk/login/
    url(r'^login/$', auth_views.login, name='login'),
    # ex: /helpdesk/logout/ next+page padeda nusirodyti i koki puslapi nukreipti atsijungus
    url(r'^logout/$', auth_views.logout, {'next_page': '../../helpdesk/login'}, name='logout')
]