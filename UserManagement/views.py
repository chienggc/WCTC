from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import ProductForm
from members.forms import PasswordChangingForm
from .models import Product, PointLog, Redemption
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView, PasswordChangeForm
from datetime import datetime
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator
from django.contrib import admin




def delete_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    product.delete()
    return redirect('list-products')

def list_products(request):
    product_list = Product.objects.all()
    request.user
    context = {
        'product_list': product_list,
        'user' : request.user
    }
    return render(request, 'products/product_list.html', context)

def list_redemption(request):
    current_user = request.user
    if request.user.is_staff:
        redeem_list = Redemption.objects.all().order_by('-updated_date')
    else :
        redeem_list = Redemption.objects.filter(redeemer= current_user).order_by('-updated_date')

    context = {
        'redeem_list' : redeem_list,
        'user' : current_user,
    }
    return render(request, 'products/redeem_list.html', context)

def update_redemption(request, redemption_id, status):
    redemption = Redemption.objects.get(pk=redemption_id)
    if status == "New":
        redemption.status = "Processing"
    elif status == "Processing":
        redemption.status = "Completed"
    redemption.acknowledgeby = request.user
    redemption.updated_date = datetime.now()
    redemption.save()
    return redirect('list_redemption')

def reedem_product(request, prod_id):
    product_list = Product.objects.all()
    current_user = request.user
    single_point_obj = PointLog.objects.filter(user_id=current_user).latest('point_date')
    product_obj = Product.objects.get(pk=prod_id)
    l_point = single_point_obj.latest_point
    prd_point = product_obj.price
    if l_point > prd_point:
        messages.error(request, 'Award Redeemtion Request Submitted !!!', extra_tags='alert')
        p = PointLog(user_id=current_user, previous_point=l_point, latest_point=(int(l_point) - int(prd_point)),
                     point_date=datetime.now(),
                     action="Redeem Award")
        p.save()
        r = Redemption(redeemer=current_user, gift=product_obj, status='New', updated_date=datetime.now())
        r.save()
    else:
        messages.error(request,'Insufficient Point !!!', extra_tags='alert')
    return render(request , 'products/product_list.html', {'product_list': product_list})

def edit_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('list-products')
    return render(request, 'products/edit_product.html', {'product': product, 'form': form})


def add_product(request):
    submitted = False
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_product?submitted=True')
    else:
        form = ProductForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'products/add_product.html', {'form' : form, 'submitted': submitted})

class PasswordsChangeView(PasswordChangeView):
    form_class= PasswordChangingForm
    success_url = reverse_lazy('edit_profile')
    def form_valid(self, form):
        messages.success(self.request, "Password Update Successfully!!!")
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

def password_success(request):
    return render(request, 'authenticate/password_success.html', {})


