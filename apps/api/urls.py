# -*- encoding=utf-8 -*-

from django.urls import re_path, path

from api.views.expert import ExpertListView, ExpertDetailView
from api.views.conference import ConferenceListView, ConferenceDetailView
from api.views.patent import PatentListView, ExpertPatentsView, PatentDetailView

app_name = 'api'
urlpatterns = [
    re_path(r'^experts/$', ExpertListView.as_view(), name='expert_list'),
    re_path(r'^experts/(?P<pk>\d+)/$', ExpertDetailView.as_view(), name='expert_detail'),
    re_path(r'^conferences/$', ConferenceListView.as_view(), name='conference_list'),
    re_path(r'^conferences/(?P<pk>\d+)/$', ConferenceDetailView.as_view(), name='conference_read'),
    re_path(r'^experts/(?P<expert_id>\d+)/patents/$', ExpertPatentsView.as_view(), name='expert_patent_list'),
    re_path(r'^patents/$', PatentListView.as_view(), name='patent_list'),
    re_path(r'^patents/(?P<pk>\d+)/$', PatentDetailView.as_view(), name='patent_read'),
]
