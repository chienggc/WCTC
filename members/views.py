from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import Award
from django.views.generic.edit import FormView
from .forms import RegisterUserForm, EditProfileForm, AwardForm, GiveAwardForm
from UserManagement.models import PointLog, Redemption
from datetime import datetime, date
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
import string, random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

POINT = 100
QUOTES = ["Happiness depends upon ourselves.",
          "Dream big, start small.", "Do it right now!",
          "Always striving, never settling",
          "Success is 99% failure.", "Reach for the stars.",
          "Make your own sunshine.",
          "Talent works, genius creates.",
          "Let your sparkle shine!", "Turn wounds into wisdom."]

def user_login(request):
    if request.method == "POST":
        username = request.POST['useremail']
        password = request.POST['userpassword']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            month = datetime.today().strftime("%m")
            now = datetime.now()

            if int(month) % 2 == 0:
                even_date = datetime.now().replace(hour=23, minute=30, second=0, microsecond=0)
                if now < even_date:
                    cond = add_point(user)
                    if cond:
                        messages.success(request, ("On Time Bonus Received !!!"))

            else:
                odds_date = datetime.now().replace(hour=23, minute=30, second=0, microsecond=0)
                if now < odds_date:
                    cond = add_point(user)
                    if cond:
                        messages.success(request, ("On Time Bonus Received !!!"))

            return redirect('dash_board')
        else:
            messages.success(request, ("Unable To Login, Please Try Again..."))
            return redirect('user_login')
    else:
        if request.user.is_authenticated:
            return redirect('dash_board')
            pass
        else:
            return render(request, 'authenticate/login.html')
            pass

def user_logout(request):
    logout(request)
    # messages.success(request, "You Were Logged Out !!!")
    return redirect('user_login')

def add_point(user):
    single_point_obj = PointLog.objects.filter(user_id=user).latest('point_date')
    point_date = datetime.strftime(single_point_obj.point_date, '%y-%m-%d')
    today_date = datetime.strftime(datetime.today(), '%y-%m-%d')

    if point_date == today_date:
        return False
    else:
        latest_point = single_point_obj.latest_point
        prev_point = single_point_obj.latest_point
        award_obj = Award.objects.get(award_name='Login Award')
        award_point = award_obj.award_point
        p = PointLog(user_id=user, previous_point=latest_point, latest_point=(int(prev_point) + int(award_point)),
                     point_date=datetime.now(),
                     action="Received " + award_obj.award_name)
        p.save()
        return True


def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            created_username = request.POST['username']
            user_obj = User.objects.get(username=created_username)
            p = PointLog(user_id=user_obj, previous_point=0, latest_point=0, point_date=datetime.now(),
                         action="New Member Registration")
            p.save()
            messages.success(request, ('Registration Successfull'))
            return redirect('user_login')
    else:
        form = RegisterUserForm()
    return render(request, 'authenticate/register_user.html', {'form': form})


def add_award(request):
    submitted = False
    if request.method == "POST":
        form = AwardForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ('Award Added Successfully !!'))
            return redirect('add_award')
    else:
        form = AwardForm()
    return render(request, 'award/add_award.html', {'form': form, 'submitted': submitted})


def edit_award(request, award_id):
    award = Award.objects.get(pk=award_id)
    form = AwardForm(request.POST or None, instance=award)
    if award.award_name == 'Login Award':
        form.disabled_field()
    if form.is_valid():
        form.save()
        return redirect('list_award')
    return render(request, 'award/edit_award.html', {'award': award, 'form': form})


def list_user(request):
    user_list = User.objects.all().exclude(pk=request.user.id)
    for user in user_list:
        single_point_obj = PointLog.objects.filter(user_id=user).latest('point_date')
        user.point = single_point_obj.latest_point
    return render(request, 'authenticate/user_listing.html', {'user_list': user_list})


class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'authenticate/edit_profile.html'
    success_url = reverse_lazy('edit_profile')

    def form_valid(self, form):
        messages.success(self.request, "Update successfully!!!")
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

    def get_object(self):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.object.is_staff:
            form.fields['is_staff'].widget.attrs['disabled'] = True
        return form




def AdminEditView(request, user_id):
    user = User.objects.get(pk=user_id)
    form = EditProfileForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect('list_profile')
    return render(request , 'authenticate/edit_profile.html', {'form': form})



def delete_award(award_id):
    award = Award.objects.get(pk=award_id)
    award.delete()
    return redirect('list_award')



class AwardListView(ListView):
    model = Award
    template_name = 'award/award_listing.html'
    context_object_name = 'award_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def get_queryset(self):
        return Award.objects.all()

def list_award(request):
    award_list = Award.objects.all()
    context = {
        'award_list': award_list,
        'user': request.user,
    }
    return render(request, 'award/award_listing.html', context)



def give_award(request, user_id):
    if request.method == "POST":
        user = User.objects.get(pk=user_id)
        single_point_obj = PointLog.objects.filter(user_id=user).latest('point_date')
        latest_point = single_point_obj.latest_point
        prev_point = single_point_obj.latest_point
        award = request.POST['award']
        award_obj = Award.objects.get(pk=award)
        award_point = award_obj.award_point
        p = PointLog(user_id=user, previous_point=latest_point, latest_point=(int(prev_point)+int(award_point)), point_date=datetime.now(),
                     action="Received " + award_obj.award_name+" Award")
        p.save()
        current_user = request.user
        page_obj = {
            "name" : current_user.first_name,
            "color" : award_obj.color_code,
            "award_name": award_obj.award_name,
            "quote" : random.choice(QUOTES),
            "details" :"",
            "project" :"",
            "point" : award_obj.award_point,
            "date": datetime.strftime(datetime.now(),'%d %B, %Y'),
            "message" : request.POST['message']
        }
        email_message = EmailMultiAlternatives(subject=request.POST['subject'], body='123', from_email='chienggc8555@gmail.com' , to=[user.email])
        html_template = get_template('award/received_award.html').render({'page_obj' : page_obj})
        email_message.attach_alternative(html_template, 'text/html')
        email_message.send()
        messages.success(request, (string.capwords(user.first_name) + ' Has Received ' + award_obj.award_name +' Award'))
        return redirect('list_profile')
    else:
        user = User.objects.get(pk=user_id)
        form = GiveAwardForm(request.POST or None, initial= {'award': Award.pk})
        form.set_initial(user.first_name)
    return render(request , 'award/give_award.html', {'form': form , 'user': user})

def dashboard(request):
    current_user = request.user
    redeem_list = Redemption.objects.filter(redeemer=current_user).exclude(status='Completed')[:5]
    point_objs = PointLog.objects.order_by('-point_date').filter(user_id=current_user)[:10]
    for point_obj in point_objs:
        point_obj.point = int(point_obj.latest_point) - int(point_obj.previous_point)
    point_details = calculated_reedemed_point(request)
    context = {
        'redeem_list': redeem_list,
        'point_objs' : point_objs,
        'latest_point' : point_objs[0].latest_point,
        'reedemed_point' : point_details[0],
        'reedemed_award_count': point_details[1],
    }
    return render(request , 'authenticate/dashboard.html', context)

def calculated_reedemed_point(request):
    point_objs = PointLog.objects.filter(user_id=request.user, action='Redeem Award')
    r_point = 0
    r_count= 0
    for point_obj in point_objs:
        r_point += point_obj.previous_point - point_obj.latest_point
        r_count +=1
    return r_point, r_count



