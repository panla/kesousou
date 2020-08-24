# -*- encoding=utf-8 -*-

from django.urls import re_path, path

from api.views.expert import ExpertListView, ExpertDetailView
from api.views.conference import ConferencesView, ExpertConferencesView, ConferenceView
from api.views.patent import PatentsView, ExpertPatentsView, PatentView
from api.views.achievement import AchievementsView, ExpertAchievementsView, AchievementView
from api.views.periodical import PeriodicalsView, ExpertPeriodicalsView, PeriodicalView


app_name = 'api'
urlpatterns = [
    re_path(r'^experts/$', ExpertListView.as_view(), name='expert_list'),
    re_path(r'^experts/(?P<pk>\d+)/$', ExpertDetailView.as_view(), name='expert_detail'),
    re_path(
        r'^experts/(?P<expert_id>\d+)/conferences/$', ExpertConferencesView.as_view(), name='expert_conference_list'
    ),
    re_path(r'^conferences/$', ConferencesView.as_view(), name='conference_list'),
    re_path(r'^conferences/(?P<pk>\d+)/$', ConferenceView.as_view(), name='conference_read'),
    re_path(r'^experts/(?P<expert_id>\d+)/patents/$', ExpertPatentsView.as_view(), name='expert_patent_list'),
    re_path(r'^patents/$', PatentsView.as_view(), name='patent_list'),
    re_path(r'^patents/(?P<pk>\d+)/$', PatentView.as_view(), name='patent_read'),
    re_path(
        r'^experts/(?P<expert_id>\d+)/achievements/$', ExpertAchievementsView.as_view(), name='expert_achievement_list'
    ),
    re_path(r'^achievements/$', AchievementsView.as_view(), name='achievement_list'),
    re_path(r'^achievements/(?P<pk>\d+)/$', AchievementView.as_view(), name='achievement_read'),
    re_path(
        r'^experts/(?P<expert_id>\d+)/periodicals/$', ExpertPeriodicalsView.as_view(), name='expert_periodical_list'
    ),
    re_path(r'^periodicals/$', PeriodicalsView.as_view(), name='periodical_list'),
    re_path(r'^periodicals/(?P<pk>\d+)/$', PeriodicalsView.as_view(), name='periodical_list'),
]
