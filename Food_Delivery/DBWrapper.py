from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login

from fooddelivery import settings
class DBWrapper():
    def SaveUser(username, password, email, fname, lname):
        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
    def SendMail(subject, message,email):
        from_email = settings.EMAIL_HOST_USER
        to_list = [email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

    def Validate(username, email, fname, lname, pass1, pass2):
        if User.objects.filter(username=username):
            return (False,"Username already exists, please try another username")
        if User.objects.filter(email=email):
            return (False,"Email already registered!")
        if len(username) > 10:
            return (False,"Username must be under 10 characters!")
        if pass1 != pass2:
            return (False,"Passwords don't match!")
        if not username.isalnum():
            return (False,"Username must be alphanumeric!")

        return (True, "")

    def TryAuthenticate(request, username, password):
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return (True, user.first_name)

        return (False, "")
