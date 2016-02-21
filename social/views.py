from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from social.models import Member, Profile, Message, Invitation
from difflib import SequenceMatcher
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import PBKDF2PasswordHasher
import datetime as D
#cbkjdsd

appname = 'Facemagazine'
# decorator that tests whether user is logged in
def loggedin(f):
    def test(request):
        if 'username' in request.session:
            return f(request)
        else:
            template = loader.get_template('social/not-logged-in.html')
            context = RequestContext(request, {})
            return HttpResponse(template.render(context))
    return test

def index(request):
    template = loader.get_template('social/index.html')
    context = RequestContext(request, {
    		'appname': appname,
    	})
    return HttpResponse(template.render(context))

def signup(request):
    template = loader.get_template('social/signup.html')
    context = RequestContext(request, {
    		'appname': appname,
    	})
    return HttpResponse(template.render(context))

def register(request):
    u = request.POST['user']
    p = request.POST['pass']

    template = loader.get_template('social/novalues.html')
    context = RequestContext(request, {
                'appname': appname
                    })

    if p=="" or u=="" or (" " in p) or (" " in u) or ('^[A-Za-z0-9_-]+$' in u)==True :
        return HttpResponse(template.render(context))
    else:
     hasher = PBKDF2PasswordHasher() #using PBKDF2 algorithm to hash
     hashedp = hasher.encode(password= p, salt='salt', iterations = 50000) #hashing password
     user = Member(username=u, password=hashedp)
     user.save()
    template = loader.get_template('social/user-registered.html')
    context = RequestContext(request, {
        'appname': appname,
        'username' : u
        })
    return HttpResponse(template.render(context))

def login(request):
    if 'username' not in request.POST:
        template = loader.get_template('social/login.html')
        context = RequestContext(request, {
                'appname': appname,
            })
        return HttpResponse(template.render(context))
    else:
        u = request.POST['username']
        p = request.POST['password']
        hasher = PBKDF2PasswordHasher() #using PBKDF2 algorithm to hash
        hashedp = hasher.encode(password= p, salt='salt', iterations = 50000) #hashing login password
        template = loader.get_template('social/user-doesnt-exist.html')
        context = RequestContext(request, {
                'appname': appname,
            })
        try:
            member = Member.objects.get(pk=u)
            print(member.password)
        except Member.DoesNotExist:
            return HttpResponse(template.render(context))
        if hashedp == member.password:
            print("right")
            request.session['username'] = u;
            request.session['password'] = p;
            response = HttpResponse('Hello World')
            return render(request, 'social/login.html', {
                'appname': appname,
                'username': u,
                'loggedin': True}
                )
        else:
            template = loader.get_template('social/wrongpass.html')
            context = RequestContext(request, {
               'appname': appname,
            })
        return HttpResponse(template.render(context))

@loggedin
def friends(request):
    username = request.session['username']
    member_obj = Member.objects.get(pk=username)
    if 'unfriend' in request.GET:
        friend = request.GET['unfriend']
        friend_obj = Member.objects.get(pk=friend)
        member_obj.following.remove(friend_obj)
        member_obj.save()
    # list of people I'm friends with
    following = member_obj.following.all()
    followers = Member.objects.filter(following__username=username)
    # get friends of friends of the user, then exclude their friends, them and finally remove duplicate items
    recommendations=Member.objects.filter(following__following__username=username).exclude(following=username).exclude(pk=username).distinct()
    invitations = Invitation.objects.filter(to_user=username)
    # render response
    return render(request, 'social/friends.html', {
        'appname': appname,
        'username': username,
        'members': members,
        'recommended': recommendations,
        'invitations':invitations,
        'following': following,
        'followers': followers,
        'loggedin': True}
        )

@loggedin
def logout(request):
    if 'username' in request.session:
        u = request.session['username']
        request.session.flush()        
        template = loader.get_template('social/logout.html')
        context = RequestContext(request, {
                'appname': appname,
                'username': u
            })
        return HttpResponse(template.render(context))
    else:
        raise Http404("Can't logout, you are not logged in")

def member(request, view_user):
    username = request.session['username']
    member = Member.objects.get(pk=view_user)
    if 'view' in request.GET:
        view = request.GET['view']
    else:
        view = username
    recip = Member.objects.get(pk=view)
    # If message was deleted
    if 'erase' in request.GET:
        msg_id = request.GET['erase']
        Message.objects.get(id=msg_id).delete()
    # If text was posted then save on DB
    if 'text' in request.POST:
        text = request.POST['text']
        pm = request.POST['pm'] == "0"
        message = Message(user=username,recip=recip,pm=pm,time=timezone.now(),text=text)
        message.save()
    messages = Message.objects.filter(recip=recip)
    profile_obj = Member.objects.get(pk=view).profile
    profile = profile_obj.text if profile_obj else ""
    if view_user == username:
        greeting = "Your"
    else:
        greeting = view_user + "'s"

    if member.profile:
        text = member.profile.text
    else:
        text = ""
    invitations = Invitation.objects.filter(to_user=username)
    return render(request, 'social/member.html', {
        'appname': appname,
        'username': username,
        'view_user': view_user,
        'messages': messages,
        'invitations':invitations,
        'greeting': greeting,
        'profile': text,
        'loggedin': True}
        )

@loggedin
def members(request):
    username = request.session['username']
    member_obj = Member.objects.get(pk=username)
    if 'search' in request.POST:
        search_obj = request.POST['search']
        members = Member.objects.all().exclude(pk=username)
        lst = []
        for person in members:
            print('hello')
            sm = SequenceMatcher(None, search_obj, person.__str__())
            x = sm.ratio()
            if x >= 0.7:
                lst.append(Member.objects.get(pk=person))
                print(lst)
        # list of people I'm following
        following = member_obj.following.all()
        # list of people that are following me
        followers = Member.objects.filter(following__username=username)
        invitations = Invitation.objects.filter(to_user=username)
                # render response
        return render(request, 'social/members.html', {
            'appname': appname,
            'username': username,
            'query': search_obj,
            'invitations': invitations,
            'following': following,
            'followers': followers,
            'results': lst,
            'loggedin': True}
            )
    # send a friend request
    if 'invite' in request.GET:
        friend = request.GET['invite']
        friend_obj = Member.objects.get(pk=friend)
        # If they are already friends
        if Member.objects.filter(username=username, following=friend).exists():
            pass # do nothing as they are already friends
        # If invitee has already sent a request to the user, make them friends
        elif Invitation.objects.filter(to_user=username, from_user=friend).exists():
            member_obj.following.add(friend_obj)
            member_obj.save()
            Invitation.objects.filter(to_user=member_obj, from_user=friend).delete()
        # Not friends and no invitation exists
        else:
            print("not friends and invitation may or may not have already been sent")
            print(friend)
            print(friend_obj)#interesting to note that while the two print statement will display the same thing
                            # only friend_obj can be passed to the database as its required to be an instance
            Invitation.objects.update_or_create(to_user=friend_obj, from_user=member_obj, status='pending', defaults={'timestamp':timezone.now()})
    # view user profile
    if 'view' in request.GET:
        return member(request, request.GET['view'])
    else:
        # list of all other members
        members = Member.objects.exclude(pk=username)
        # list of people I'm following
        following = member_obj.following.all()
        # list of people that are following me
        followers = Member.objects.filter(following__username=username)
        invitations = Invitation.objects.filter(to_user=username)
        # render response
        return render(request, 'social/members.html', {
            'appname': appname,
            'username': username,
            'members': members,
            'invitations': invitations,
            'following': following,
            'followers': followers,
            'loggedin': True}
            )

@loggedin
def invites(request):
    username = request.session['username']
    member_obj = Member.objects.get(pk=username)
    # cancel friend request
    if 'cancel' in request.GET:
        friend = request.GET['cancel']
        Invitation.objects.filter(to_user=friend, from_user=username).delete()
    # accept friend request
    if 'accept' in request.GET:
        friend = request.GET['accept']
        friend_obj = Member.objects.get(pk=friend)
        member_obj.following.add(friend_obj)
        member_obj.save()
    # once we have accepted the friend request we no longer have need of the original invitation, so we delete from the database
        Invitation.objects.filter(to_user=member_obj, from_user=friend).delete()
    # decline friend invitation
    if 'decline' in request.GET:
        friend = request.GET['decline']
        Invitation.objects.filter(to_user=member_obj, from_user=friend).delete()
    # view user profile
    if 'view' in request.GET:
        return member(request, request.GET['view'])
    else:
        # list of all other members
        members = Member.objects.exclude(pk=username)
        # get all invitations sent to me
        invitations = Invitation.objects.filter(to_user=username)
        # render response
        return render(request, 'social/invites.html', {
            'appname': appname,
            'username': username,
            'invites': members,
            'invitations': invitations,
            'loggedin': True}
            )

@loggedin
def profile(request):
    u = request.session['username']
    member = Member.objects.get(pk=u)
    if 'text' in request.POST:
        text = request.POST['text']
        if member.profile:
            member.profile.text = text
            member.profile.save()
        else:
            profile = Profile(text=text)
            profile.save()
            member.profile = profile
        member.save()
    else:
        if member.profile:
            text = member.profile.text
        else:
            text = ""
    invitations = Invitation.objects.filter(to_user=u)
    return render(request, 'social/profile.html', {
        'appname': appname,
        'username': u,
        'invitations':invitations,
        'text' : text,
        'loggedin': True}
        )

@loggedin
def messages(request):
    username = request.session['username']
    user = Member.objects.get(pk=username)
    # Whose message's are we viewing?
    if 'view' in request.GET:
        view = request.GET['view']
    else:
        view = username
    recip = Member.objects.get(pk=view)
    # If message was deleted
    if 'erase' in request.GET:
        msg_id = request.GET['erase']
        Message.objects.get(id=msg_id).delete()
    # If text was posted then save on DB
    if 'text' in request.POST:
        text = request.POST['text']
        pm = request.POST['pm'] == "0"
        message = Message(user=user,recip=recip,pm=pm,time=timezone.now(),text=text)
        message.save()
    messages = Message.objects.filter(recip=recip)
    profile_obj = Member.objects.get(pk=view).profile
    profile = profile_obj.text if profile_obj else ""
    invitations = Invitation.objects.filter(to_user=username)
    return render(request, 'social/messages.html', {
        'appname': appname,
        'username': username,
        'invitations':invitations,
        'profile': profile,
        'view': view,
        'messages': messages,
        'loggedin': True}
        )

def checkuser(request):
    if 'user' in request.POST:
        u = request.POST['user']
        try:
            member = Member.objects.get(pk=u)
        except Member.DoesNotExist:
            member = None
        if member is not None:
            return render(request, "social/username_taken.html", RequestContext(request, locals()))
        else:
            return render(request, "social/username_free.html", RequestContext(request, locals()))
