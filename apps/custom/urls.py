import os

from django.urls import re_path
from django.conf import settings

from custom.views.index import IndexView
from custom.views.expert import ExpertListView, ExpertDetailView
from custom.views.conference import ConferencesView, ExpertConferencesView, ConferenceView
from custom.views.patent import PatentsView, ExpertPatentsView, PatentView
from custom.views.achievement import AchievementsView, ExpertAchievementsView, AchievementView
from custom.views.periodical import PeriodicalsView, ExpertPeriodicalsView, PeriodicalView

app_name = 'custom'
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
    re_path(r'^periodicals/(?P<pk>\d+)/$', PeriodicalView.as_view(), name='periodical_list'),
]

if settings.DISPLAY_DOCS:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if os.path.join(BASE_DIR, 'core/local/docs.py'):
        try:
            from core.local.docs import custom_schema_view

            urlpatterns += [
                re_path(r'^doc/$', custom_schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
            ]
        except Exception as exc:
            raise Exception('need a right local docs settings')
    else:
        raise Exception('need a local docs settings')
