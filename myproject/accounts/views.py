from email.message import EmailMessage
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
                        variation=item.variation.all()
                        product_variation.append(list(variation))

                    # get the cart item for teh user to access his product variaions.
                    cart_item = CartItem.objects.get(user=user).exist()
                    ex_var_list = []
                    id= []
                    for item in cart_item:
                        existing_variation = item.variation.all()
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
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=')for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
                return redirect(dashboard)
            except:
                pass
            
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
                    user = User.objects.create_user(username=firstname, password=password1, email= email)
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
                    # email =EmailMessage(email_subject, message, to=[to_email])
                    # email.send()
                    send_mail(
    'Subject here',
    'Here is the message.',
    'fighterufc2@gmail.com',
    [to_email],
    fail_silently=False,
)


                    messages.success(request, 'You are registerd and you can login')
                    return redirect('login')
        else:
            messages.error(request, 'Your password didnot match.')


    return render(request, 'myproject/register.html')


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'myproject/dashboard.html')


def activate(request):
    return

