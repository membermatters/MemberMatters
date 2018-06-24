from django.contrib.auth import login, authenticate
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *


def signup(request):
    if request.method == 'POST':
        user_form = SignUpForm(request.POST)
        profile_form = AddProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save()
            profile = profile_form.save(commit=False)

            if profile.user_id is None:
                profile.user_id = new_user.id
            profile.save()

            username = user_form.cleaned_data.get('username')
            raw_password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')

    else:
        user_form = SignUpForm()
        profile_form = AddProfileForm()

    return render(request, 'registration/signup.html', {'user_form': user_form, 'profile_form': profile_form})


def signin(request):
    return render(request, 'registration/login.html')


def error(request):
    return HttpResponse("Oops. This shouldn't be possible. You've entered a URL that's not valid.")


def home(request):
    return render(request, 'home.html')


@login_required()
def profile(request):
    return render(request, 'profile.html')


@login_required()
def member_list(request):
    if request.user.is_staff:
        members = User.objects.values('id', 'username', 'email', 'first_name', 'last_name', 'profile__member_type__name',
                                      'profile__state__name', 'profile__cause1__name', 'profile__cause2__name',
                                      'profile__cause3__name', 'profile__state')

        return render(request, 'memberlist.html', {'members': members})

    else:
        return HttpResponseForbidden("403 Access Forbidden")


def save_admin_edit_member_form(request, form, template_name, member_id):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    context = {'form': form, 'member_id': member_id}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required()
def admin_edit_member(request, member_id):
    user = get_object_or_404(Profile, user=member_id)
    if request.method == 'POST':
        form = AdminEditProfileForm(request.POST, instance=user)
    else:
        form = AdminEditProfileForm(instance=user)
    return save_admin_edit_member_form(request, form, 'partial_admin_edit_member.html', member_id)


#@login_required()
def edit_profile(request):
    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=request.user)
        profile_form = EditProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect('%s' % (reverse('profile')))
        else:
            pass
    else:
        user_form = EditUserForm(instance=request.user)
        profile_form = EditProfileForm(instance=request.user.profile)
        return render(request, 'edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})


def set_state(request, member_id, state):
    user = User.objects.get(id=member_id)
    user.profile.state = MemberState.objects.get(pk=state)
    user.profile.save()
    return JsonResponse({"success": True})


def loggedout(request):
    return render(request, 'loggedout.html')


def manage_doors(request):
    pass
