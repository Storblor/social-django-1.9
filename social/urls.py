from django.conf.urls import patterns, url

from social import views
#randon comments to test Git commits yall
#spazmatron69 was here.
#the fuck is bluemist anyway
#idiotic comments - see above
# who is an idiot now?? #trynum2
# you focking wut mate?
urlpatterns = [
	# main page
    url(r'^$', views.index, name='index'),
    # signup page
    url(r'^signup/$', views.signup, name='signup'),
    # register new user
	url(r'^register/$', views.register, name='register'),
    # login page
    url(r'^login/$', views.login, name='login'),
    # user doesnt exist webpage
    url(r'^user-doesnt-exist/$', views.login, name='user-doesnt-exist'),
    #page to show that the password is incorrect
    url(r'^wrongpass/$', views.login, name='wrongpass'),
    #webpage to show an error when a user tries to input nothing in the fields when signing up
    url(r'^novalues/$', views.register, name='novalues'),
    # logout page
    url(r'^logout/$', views.logout, name='logout'),
    # members page
    url(r'^members/$', views.members, name='members'),
    #invites page
    url(r'^invites/$', views.invites, name='invites'),
    # friends page
    url(r'^friends/$', views.friends, name='friends'),
    # user profile edit page
    url(r'^profile/$', views.profile, name='profile'),
    # messages page
    url(r'^messages/$', views.messages, name='messages'),
    # Ajax: check if user exists
    url(r'^checkuser/$', views.checkuser, name='checkuser'),
    #commiting again
]


