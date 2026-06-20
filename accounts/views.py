from itertools import product

from django.http import HttpResponse
from django.shortcuts import render, redirect
from accounts.forms import RegisterationForm
from accounts.models import Account
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
# email verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from carts.models import Cart, CartItem
from carts.views import _cart_id


# =========================
# REGISTER
# =========================
def register(request):

    if request.method == 'POST':
        form = RegisterationForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            username = email.split("@")[0]

            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password
            )

            user.phone_number = phone_number
            user.is_active = False  # IMPORTANT
            user.save()

            # EMAIL VERIFICATION
            current_site = get_current_site(request)

            message = render_to_string(
                'accounts/account_verification_email.html',
                {
                    'user': user,
                    'domain': current_site.domain,
                    'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                }
            )

            email_message = EmailMessage(
                'Please activate your account',
                message,
                to=[email]
            )
            email_message.send()

            messages.success(request, "Registration successful! Check your email to activate account.")
            return redirect('login')

    else:
        form = RegisterationForm()

    return render(request, 'accounts/register.html', {'form': form})


# =========================
# LOGIN
# =========================
def login(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = Account.objects.get(email=email)
        except Account.DoesNotExist:
            messages.error(request, "Invalid credentials")
            return redirect('login')

        if not user_obj.is_active:
            messages.error(request, "Account not activated. Check your email.")
            return redirect('login')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            try:
                cart= Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists= CartItem.objects.filter(product=product, cart=cart).exists()
                if is_cart_item_exists:
                    cart_item= CartItem.objects.filter(cart=cart)
                    
                    for item in cart_item:
                        item.user= user
                        item.save()
                
                
            except:
                pass
            auth_login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('store')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')

    return render(request, 'accounts/login.html')



# =========================
# LOGOUT
# =========================
def logout(request):
    auth_logout(request)
    messages.success(request, "You are logged out")
    return redirect('login')


# =========================
# ACTIVATE ACCOUNT
# =========================
def activate(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except:
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Account activated successfully!")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid")
        return redirect('register')
    
@login_required(login_url='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']

        if Account.objects.filter(email=email).exists():

            user = Account.objects.get(email__exact=email)
            
            
            
            #Reset password email

            current_site = get_current_site(request)

            mail_subject = 'Reset Your Password'

            message = render_to_string(
                'accounts/reset_password_email.html',
                {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                }
            )

            to_email= email
            send_email= EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(
                request,
                'Password reset email has been sent to your email address.'
            )

            return redirect('login')

        else:
            messages.error(request, 'Account does not exist.')
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')

def resetpassword_validate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Reset your password below')
        return redirect('resetPassword')
    else:
        messages.error(request, 'Invalid or expired link')
        return redirect('login')