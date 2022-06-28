from email.message import EmailMessage
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.contrib.auth.models import User

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.core.mail import send_mail

from cart.views import _cart_id
from cart.models import Cart, CartItem

import requests

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password =request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            try:
                cart=Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exist= CartItem.objects.filter(cart=cart).exists()
                print(is_cart_item_exist)
                if is_cart_item_exist:
                    cart_item = CartItem.objects.filter(cart=cart)

                    #getting product variation by cart id
                    product_variation=[]
                    for item in cart_item:
                        variation=item.variations.all()
                        product_variation.append(list(variation))

                    # get the cart item for the user to access his product variaions.
                    cart_item = CartItem.objects.get(user=user).exist()
                    ex_var_list = []
                    id= []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)   

                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quntity += 1
                            item.user=user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user=user
                                item.save()
                    # for item in cart_item:
                    #     item.user = user
                    #     item.save()
            except:
                pass
            auth.login(request, user)
            messages.success(request, 'You are logged in.')

            # Dyanmically adding the url path

            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                # next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                print(params)
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
                
            except:
                return redirect('dashboard')
            
        else:
            messages.error(request, 'Invalid credentals')

    return render(request, 'myproject/login.html')

def logout(request):

    # When form is used
    # if request.method == 'POST':
    #     auth.logout(request)
    #     messages.success(request, 'You now logged out.')

    #when form is not used
    auth.logout(request)
    messages.success(request, 'You now logged out.')
    return redirect('home')

def register(request):

    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname= request.POST['lastname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            # check username
            if User.objects.filter(username=firstname).exists():
                messages.error(request, "The username is taken")
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'email is used')
                    
                else:
                    user = User.objects.create_user(username=firstname, first_name=firstname, last_name=lastname, password=password1, email= email)
                    user.save()
                    
                    #User activation
                    current_site = get_current_site(request)
                    email_subject= "Please activate your account"
                    message =render_to_string('myproject/account_verification_email.html', {
                        'user': user, 
                        'domain':current_site.domain,
                        'uid':urlsafe_base64_encode(force_bytes(user.pk)), 
                        'token': default_token_generator.make_token(user),
                    })
                    to_email =email
                    email =EmailMessage(email_subject, message, to=[to_email])
                    email.send()
                    # send_mail(
                    #     'Subject here',
                    #     'Here is the message.',
                    #     'ranamagar.prashant@gmail.com',
                    #     [to_email],
                    #     fail_silently=False,
                    # )


                    messages.success(request, 'Thank you for registring with us. We have send you a verification email. Please verify it.')
                    
                    return redirect('login')
        else:
            messages.error(request, 'Your password didnot match.')


    return render(request, 'myproject/register.html')


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'myproject/dashboard.html')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.ObjectDoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_staff = True
        user.save()
        messages.success(request, 'Congratulation! Your account is activated')
        return redirect('login')
    else:
        messages.error(request, 'Invalid Activation Link')
        return redirect('register')
    

def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            #User activation
            current_site = get_current_site(request)
            email_subject= "Reset Your Password"
            message =render_to_string('myproject/reset_password_email.html', {
                'user': user, 
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)), 
                'token': default_token_generator.make_token(user),
            })
            to_email =email
            email =EmailMessage(email_subject, message, to=[to_email])
            email.send() 

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        
        else:
            messages.errror(request, 'Account doesnot exist.')
            return redirect('forgotpassword')

    return render(request, 'myproject/forgotpassword.html') 


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.ObjectDoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] =uid
        messages.success(request, 'Please reset your password.')
        return redirect('resetpassword')
    else:
        messages.error(request, 'This link has been expired.')
        return redirect('login')
   

def resetpassword(request):
    if request.method =='POST':
        password1 = request.POST['create_password']
        password2 = request.POST['confirm_password']

        if password1 == password2:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password1)
            user.save()
            messages.success(request, 'Password reset successfull')
            return redirect('login')
        else:
            messages.error(request, 'Password did not match')
            return redirect ('resetpassword')
        
        
    return render(request, 'myproject/resetpassword.html')