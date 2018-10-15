from django.conf.urls import url
from django.contrib import admin
from boards import views
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #Homepage
    #Homepage view for Function based view
    #url(r'^$', views.home, name='home'),
    #Homepage Generic Class Based View
    url(r'^$', views.BoardListView.as_view(), name='home'),

    #Boards URLs
    #Board Topics using Function based View Url
    #url(r'^boards/(?P<pk>\d+)/$', views.board_topics, name='board_topics'),

    #Board Topics using CLass based View Url
    url(r'^boards/(?P<pk>\d+)/$', views.TopicListView.as_view(), name='board_topics'),
    

    url(r'^boards/(?P<pk>\d+)/new/$', views.new_topic, name='new_topic'),

    #Board Messages URL
    # Function based view
    #url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', views.topic_posts, name='topic_posts'),
    #Class based View
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', views.PostListView.as_view(), name='topic_posts'),

    #Login URLs
    url(r'signup/$',accounts_views.signup, name='signup'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    #Logout URLs
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),


    #Password Reset URLs
    url(r'^reset/$',
    auth_views.PasswordResetView.as_view(
        template_name='password_reset/password_reset.html',
        email_template_name='password_reset/password_reset_email.html',
        subject_template_name='password_reset/password_reset_subject.txt'
    ),
    name='password_reset'),
    url(r'^reset/done/$',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset/password_reset_done.html'),
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset/password_reset_confirm.html'),
        name='password_reset_confirm'),
    url(r'^reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'),
        name='password_reset_complete'),
    

    #Password Change URLs
    url(r'^settings/password/$', auth_views.PasswordChangeView.as_view(template_name='password_change/password_change.html'),
    name='password_change'),
    url(r'^settings/password/done/$', auth_views.PasswordChangeDoneView.as_view(template_name='password_change/password_change_done.html'),
        name='password_change_done'),

    #Reply to Post URLs
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$', views.reply_topic, name='reply_topic'),

    #### Class Based Views URLs ####
    # url(r'^new_post/$', views.NewPostView.as_view(), name='new_post'),
    url(r'^index/$', views.ContactList.as_view()),
    #### Generic Class Based Views URLs ####

    #Post Update URL
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/edit/$',
        views.PostUpdateView.as_view(), name='edit_post'),

    #User Account Url
    url(r'^settings/account/$', accounts_views.UserUpdateView.as_view(), name='my_account') 

]
