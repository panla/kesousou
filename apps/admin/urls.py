import os

from django.urls import re_path
from django.conf import settings

from admin.views.index import IndexView
from admin.views.user import UserJWTView, UsersView, UserView
from admin.views.expert import ExpertsView, ExpertView
from admin.views.achievement import AchievementsView, ExpertAchievementsView, AchievementView
from admin.views.conference import ConferencesView, ExpertConferencesView, ConferenceView
from admin.views.patent import PatentsView, ExpertPatentsView, PatentView
from admin.views.periodical import PeriodicalsView, ExpertPeriodicalsView, PeriodicalView

app_name = 'admin'
urlpatterns = [
    re_path(r'^token/$', UserJWTView.as_view(), name='create_token'),
    re_path(r'^users/$', UsersView.as_view(), name='user_list_create'),
    re_path(r'^users/(?P<pk>\d+)/$', UserView.as_view(), name='user_detail'),
    re_path(r'^experts/$', ExpertsView.as_view(), name='expert_list_create'),
    re_path(r'^experts/(?P<pk>\d+)/$', ExpertView.as_view(), name='expert_detail'),
    re_path(
        r'^experts/(?P<expert_id>\d+)/conferences/$', ExpertConferencesView.as_view(), name='expert_conference_list'
    ),
    re_path(r'^conferences/$', ConferencesView.as_view(), name='conference_list'),
    re_path(r'^conferences/(?P<pk>\d+)/$', ConferenceView.as_view(), name='conference_detail'),
    re_path(r'^experts/(?P<expert_id>\d+)/patents/$', ExpertPatentsView.as_view(), name='expert_patent_list'),
    re_path(r'^patents/$', PatentsView.as_view(), name='patent_list'),
    re_path(r'^patents/(?P<pk>\d+)/$', PatentView.as_view(), name='patent_detail'),
    re_path(
        r'^experts/(?P<expert_id>\d+)/achievements/$', ExpertAchievementsView.as_view(), name='expert_achievement_list'
    ),
    re_path(r'^achievements/$', AchievementsView.as_view(), name='achievement_list'),
    re_path(r'^achievements/(?P<pk>\d+)/$', AchievementView.as_view(), name='achievement_detail'),
    re_path(
        r'^experts/(?P<expert_id>\d+)/periodicals/$', ExpertPeriodicalsView.as_view(), name='expert_periodical_list'
    ),
    re_path(r'^periodicals/$', PeriodicalsView.as_view(), name='periodical_list'),
    re_path(r'^periodicals/(?P<pk>\d+)/$', PeriodicalView.as_view(), name='periodical_detail'),
]

if settings.DISPLAY_DOCS:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if os.path.join(BASE_DIR, 'core/local/docs.py'):
        try:
            from core.local.docs import admin_schema_view

            urlpatterns += [
                re_path(r'^doc/$', admin_schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
            ]
        except Exception as exc:
            raise Exception('need a local docs settings')
    else:
        raise Exception('need a local docs settings')
