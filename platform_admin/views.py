from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from accounts.models import Account
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages

from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from accounts.forms import (RegistrationForm, AccountAuthenticationForm, 
                            AccountUpdateForm, UserProfileUpdateForm)
from accounts.models import Account, Profile
from django.conf import settings
from .forms import MarketSectorForm, MarketSectorBulkDataForm
from .models import MarketSectorBulkData, MarketSector
from .tasks import create_new_customers
from utility.models import Country
# Create your views here.


@login_required
def dashboard(request):
    users = Account.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'platform_admin/dashboard.html', context)




@login_required
def edit_account_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    user_id = kwargs.get("user_id")
    account = Account.objects.get(pk=user_id)
    if account.pk != request.user.pk:
        return HttpResponse("You cannot edit someone elses profile.")
    context = {}
    if request.POST:
        form = AccountUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Account updated successfully.")
            new_username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            return redirect("platform_admin:edit-account", user_id=account.pk)
        else:
            form = AccountUpdateForm(request.POST, instance=request.user,
                    initial={
                        "id": account.pk,
                        "email": account.email,
                        "username": account.username,
                        "first_name": account.first_name,
                        "last_name": account.last_name,
                    })
            context['form'] = form
    else:
        form = AccountUpdateForm(
			initial={
					"id": account.pk,
					"email": account.email,
					"username": account.username,
					"first_name": account.first_name,
					"last_name": account.last_name,
				}
			)
        context['form'] = form
    context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    return render(request, 'platform_admin/edit_account.html', context)




class UpdatePassword(PasswordChangeView):
    form_class = PasswordChangeForm
    # success_url = '/user/edit-profile'
    template_name = 'platform_admin/change-password.html'

    def get_success_url(self):
        return reverse('platform_admin:update_password')
    
    def form_valid(self, form):
        messages.success(self.request, "Password changed successfully.")
        return HttpResponseRedirect(self.get_success_url())

