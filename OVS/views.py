from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from service.models import  *
from django.core.exceptions import ObjectDoesNotExist


@login_required
def Home(request):
    return render(request,'Home.html', {})

from django.contrib.auth.models import User
from service.models import Profile  # if using Profile model

def Register(request):
    if request.method == "POST":
        username = request.POST['username']
        name = request.POST['s_name']
        email = request.POST['email']
        number = request.POST['number']
        password = request.POST['password']
        college = request.POST['college']   # 👈 NEW

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=name
        )

        # Save extra data
        Profile.objects.create(
            user=user,
            college=college
        )

        return redirect('loginpage')

    return render(request, 'register.html')

def Login(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=name, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse('Error, user does not exist')
    return render(request,'Login.html', {})

def logoutuser(request):
    logout(request)
    return redirect('loginpage')

def Aboutus(request):
    return render(request,'Aboutus.html', {})

def Services(request):
    return render(request,'Services.html', {})

def Contactus(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        messages = request.POST['add']
        ins = Contact(username=username,add=messages, email=email)
        ins.save()
        print("ok")
    return render(request,'Contactus.html', {})

from service.models import Poll, Profile
from django.shortcuts import render, redirect

def poll_list(request):
    if not request.user.is_authenticated:
        return redirect('loginpage')

    profile, created = Profile.objects.get_or_create(user=request.user)

    polls = Poll.objects.filter(college=profile.college)

    return render(request, 'poll_list.html', {
        'polls': polls,
        'user_profile': profile   # 👈 IMPORTANT
    })


from django.shortcuts import render, get_object_or_404, redirect
from service.models import Poll, Choice, Vote

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


def poll_view(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    ip = get_client_ip(request)

    # 🚫 Check if already voted
    if Vote.objects.filter(poll=poll, ip_address=ip).exists():
        return render(request, 'already_voted.html', {'poll': poll})

    if request.method == "POST":
        choice_id = request.POST.get('choice')
        choice = Choice.objects.get(id=choice_id)

        choice.votes += 1
        choice.save()

        # Save vote
        Vote.objects.create(poll=poll, ip_address=ip)

        return redirect('results', poll_id=poll.id)

    return render(request, 'polling.html', {'poll': poll})

def results_view(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    total_votes = sum(choice.votes for choice in poll.choices.all())

    return render(request, 'results.html', {
        'poll': poll,
        'total_votes': total_votes
    })

from django.http import HttpResponse

def vote(request, poll_id):
    poll = Poll.objects.get(id=poll_id)
    profile = Profile.objects.get(user=request.user)

    if poll.college != profile.college:
        return HttpResponse("You are not allowed to access this poll")

    return render(request, 'vote.html', {'poll': poll})