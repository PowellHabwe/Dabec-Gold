from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm
from orders.models import Order, OrderProduct
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# from orders.models import Order, OrderProduct

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from carts.views import _cart_id
from carts.models import Cart, CartItem
import requests

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()
            # return redirect('login')

            # USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            # messages.success(request, 'Thank you for registering with us. We have sent you a verification email to your email address [rathan.kumar@gmail.com]. Please verify it.')
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        current_user = request.user

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:

                    cart_item = CartItem.objects.get(cart=cart)
                    # print('cart_item1', cart_item.product)

                    # Get the cart items from the user to access his product variations
                    cart_item2 = CartItem.objects.get(user= user)
                    # print('cart_item2', cart_item2.product)

                    if cart_item.product == cart_item2.product:
                        # print('yess')
                        item = CartItem.objects.get(user=user)
                        item.quantity += 1
                        item.user = user
                        item.save()
                    else:
                        # print('noo')
                        cart_item = CartItem.objects.filter(cart=cart)
                        for item in cart_item:
                            item.user = user
                            item.save()
                    # for item in cart_item:
                    #     existing_variation = item
                    #     ex_var_list.append(existing_variation)
                    #     print('ex_var_list', ex_var_list)
                    #     id.append(item.id)
                    #     # print('existing_variation', existing_variation)
                    # if 
                    #         item = CartItem.objects.get(id=item_id)
                    #         item.quantity += 1
                    #         item.user = user
                    #         item.save()
                    #     else:
                    #         cart_item = CartItem.objects.filter(cart=cart)
                    #         for item in cart_item:
                    #             item.user = user
                    #             item.save()
            except:
                pass
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                # next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')

# def login(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']
#         user = auth.authenticate(email=email, password=password)

#         if user is not None:
#             try:
#                 cart = Cart.objects.get(cart_id=_cart_id(request))
#                 is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
#                 if is_cart_item_exists:

#                     cart_item = CartItem.objects.filter(cart=cart)
#                     # print('cart_item', cart_item)

#                     # Getting the product variations by cart id
#                     product_variation = []

#                     for item in cart_item:
#                         variation = item
#                         product_variation.append(variation)
#                         print('product_variation', product_variation)

#                     # Get the cart items from the user to access his product variations
#                     cart_item = CartItem.objects.filter(user=user)
#                     # print('cart_item', cart_item)

#                     ex_var_list = []
#                     id = []
#                     for item in cart_item:
#                         existing_variation = item
#                         ex_var_list.append(existing_variation)
#                         print('ex_var_list', ex_var_list)
#                         id.append(item.id)
#                         # print('existing_variation', existing_variation)
#                     for pr in product_variation:
#                         if pr in ex_var_list:
#                             print('yessssss')
#                             index = ex_var_list.index(pr)
#                             item_id = id[index]
#                             item = CartItem.objects.get(id=item_id)
#                             item.quantity += 1
#                             item.user = user
#                             item.save()
#                         else:
#                             cart_item = CartItem.objects.filter(cart=cart)
#                             for item in cart_item:
#                                 item.user = user
#                                 item.save()
#             except:
#                 pass
#             auth.login(request, user)
#             messages.success(request, 'You are now logged in.')
#             return redirect('cart')
#         else:
#             messages.error(request, 'Invalid login credentials')
#             return redirect('cart')
#     return render(request, 'accounts/login.html')

# def login(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']
#         user = auth.authenticate(email=email, password=password)

#         if user is not None:
#             try:
#                 cart = Cart.objects.get(cart_id=_cart_id(request))
#                 is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
#                 if is_cart_item_exists:
#                     cart_item = CartItem.objects.filter(cart=cart)

#                     for item in cart_item:
#                         item.user = user
#                         item.save()
#             except:
#                 pass
#             auth.login(request, user)
#             messages.success(request, 'You are now logged in.')
#             return redirect('dashboard')
#         else:
#             messages.error(request, 'Invalid login credentials')
#             return redirect('dashboard')
#     return render(request, 'accounts/login.html')


@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')

@login_required(login_url = 'login')
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()

    # userprofile = UserProfile.objects.get(user_id=request.user.id)
    context = {
        'orders_count': orders_count,
    #     'userprofile': userprofile,
    }
    return render(request, 'accounts/dashboard.html', context)


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')

def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has expired!')
        return redirect('login')

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # auth.logout(request)
                messages.success(request, 'Password updated successfully.')
                return redirect('change_password')
            else:
                messages.error(request, 'Please enter the valid current password')
                return redirect('change_password')
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('change_password')
    return render(request, 'accounts/change_password.html')

@login_required(login_url='login')
def my_orders(request): 
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'accounts/my_orders.html', context)

@login_required(login_url='login')
def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity

    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,
    }
    return render(request, 'accounts/order_detail.html', context)