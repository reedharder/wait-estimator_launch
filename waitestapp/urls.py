from django.conf.urls import patterns, url
from waitestapp import views

urlpatterns = patterns('',
    url(r'^1/$', views.waitapp_capacity, name='capacity'),

    ##url(r'^2/$', views.waitapp_aff, name='aff'),
    ##url(r'^3/$', views.waitapp_attr, name='attributes'),

    url(r'^2/$', views.waitapp_prof, name='prof'),
    ##url(r'^4/$', views.waitapp_contrule, name='contrules'),
    ##url(r'^3/$', views.waitapp_delrule, name='delrules'),
    url(r'^3/$', views.waitapp_utilization, name='utilization'),
    url(r'^results/$', views.waitapp_results, name='results'),
    url(r'^scenario/1/$', views.scenario_1, name='capacity_s'),
    url(r'^scenario/2/$', views.scenario_2, name='aff_s'),
    ##url(r'^scenario/3/$', views.scenario_attr, name='attributes_s'),
    ##url(r'^scenario/4/$', views.scenario_contrule, name='contrules_s'),
    ##url(r'^scenario/5/$', views.scenario_delrule, name='delrules_s'),
    ##url(r'^scenario/6/$', views.scenario_utilization, name='utilization_s'),
    ##url(r'^scenario/results/$', views.scenario_results, name='results_s'),
    url(r'^$', views.home_view, name='home'),
    
)

