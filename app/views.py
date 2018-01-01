from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction
from django.db.models.functions import Lower
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login, logout

# Create your views here.
from app.functions import bad_json, ok_json
from app.models import Users, UsersGroup
from dbg.values import USERS_GROUPS_CUSTOMERS_ID
from django.views.decorators.csrf import csrf_exempt


def addGlobalData(request, data):
    myuser = None
    authenticated = True if not request.user.is_anonymous() else False
    user = request.user
    if authenticated and Users.objects.filter(user=user).exists():
        myuser = Users.objects.get(user=user)
    data['myuser'] = myuser
    return data

def index(request):
    data = {'title': 'Welcome - Designed By Gerry'}
    addGlobalData(request, data)
    return render(request, 'base.html', data)

def logout_user(request):
    request.session['currentuser'] = None
    logout(request)
    response = HttpResponseRedirect("/")
    return response

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                user_group = UsersGroup.objects.get(pk=USERS_GROUPS_CUSTOMERS_ID)

                if 'first_name' in request.POST and request.POST['first_name']:
                    first_name = request.POST['first_name']
                else:
                    return bad_json(message='First name is required')

                last_name = ""
                if 'last_name' in request.POST and request.POST['last_name']:
                    last_name = request.POST['last_name']

                email = None
                if 'email' in request.POST and request.POST['email']:
                    email = request.POST['email'].lower()

                    if User.objects.annotate(email_lower=Lower('email')).filter(email_lower=email).exists():
                        return bad_json(message='Email already exists')

                    try:
                        validate_email(email)
                    except ValidationError:
                        return bad_json(message='Please enter a valid email address')

                else:
                    return bad_json(message='Email Address is required')

                if 'username' in request.POST and request.POST['username']:
                    if ' ' in request.POST['username']:
                        return bad_json(message="Username can't contain spaces")
                    username = request.POST['username'].lower()

                    if User.objects.annotate(username_lower=Lower('username')).filter(username_lower=username).exists():
                        return bad_json(message='Username already exists')
                else:
                    return bad_json(message='Username is required')



                if 'password' in request.POST and request.POST['password']:
                    password = request.POST['password'].lower()
                else:
                    return bad_json(message='The Password field is required')

                if 'confirm_password' in request.POST and request.POST['confirm_password']:
                    confirm_password = request.POST['confirm_password'].lower()
                else:
                    return bad_json(message='The Confirm Password field is required')

                if password != confirm_password:
                    return bad_json(message='The Confirm Password and Password field must match')

                # Create the users
                django_user = User(username=username,
                                   first_name=first_name,
                                   last_name=last_name)

                if email:
                    django_user.email = email

                django_user.set_password(password)
                django_user.save()

                myuser = Users(user=django_user, group=user_group)

                myuser.save()


                django_user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, django_user)


                logged_in_user = request.user.users

                # subscription_plans = [{'plan': STRIPE_SCHOOL_PLAN_FREE_ID, 'quantity': 0, 'users': [], 'plan_myclass_id': 0}]
                return ok_json(data={'message': 'Congratulations! You have successfully created an account. That was a genius move!'})

        except Exception as ex:
            return bad_json(error=1)