from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import spot,districts,remark,reviewmodel,profilemodel
from django.views.generic import ListView,DetailView,CreateView
from django.views.generic.edit import DeleteView,CreateView
from django.contrib.auth.views import LoginView,LogoutView
from .forms import spotform,searchFormbyDistrict,reviewForm,profileform,UserCreationForm
from django.shortcuts import render,redirect
from django.db.models import Q
from django.contrib.auth import logout




#-------------------------------------------------------

@login_required(login_url='/login/')
def updateTemp(request,pk):
    edit_object=spot.objects.get(pk=pk,user=request.user)
    form=spotform(instance=edit_object)
    if request.method == 'POST':
        filled_form=spotform(request.POST,request.FILES,instance=edit_object)
        if filled_form.is_valid():
            filled_form.save()
            form=filled_form
            note="updated"
            return render(request,'home/edit.html',{'form':form,'edit':edit_object,'note':note})
    return render(request,'home/edit.html',{'form':form,'edit':edit_object})

def profileeditview(request,pk):
    edit_object=profilemodel.objects.get(pk=pk,user=request.user)
    form=profileform(instance=edit_object)
    if request.method == 'POST':
        filled_form=profileform(request.POST,request.FILES,instance=edit_object)
        if filled_form.is_valid():
            filled_form.save()
            form=filled_form
            note="updated"
            return render(request,'home/edit.html',{'form':form,'edit':edit_object,'note':note})
    return render(request,'home/edit.html',{'form':form,'edit':edit_object})

#-------------------------------------------------------

class DeleteTemp(LoginRequiredMixin,DeleteView):
    model=spot
    login_url='/spots/'
    success_url='/spotsuser/'
    template_name='home/delete.html'
#-------------------------------------------------------
def home(request):
    remarks=remark.objects.all()
    district_ten = districts.objects.all()
    return render(request,'home/home.html',{'district':district_ten,'remarks':remarks})
#-------------------------------------------------------


class register(CreateView):
    
    form_class=UserCreationForm
    template_name='home/signup.html'
    success_url='/creteprofile/'
    def get(self, request, *args, **kwargs):
        logout(request)
        self.object = None
        return super().get(request, *args, **kwargs)
#-------------------------------------------------------
class profileview(LoginRequiredMixin,CreateView):
    login_url='/login/'
    model=profilemodel
    form_class=profileform
    context_object_name='form'
    template_name='home/profilecreate.html'
    success_url='/spots/' 
    def form_valid(self, form):
        self.object=form.save(commit=False)
        self.object.user=self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
#-------------------------------------------------------
class profileDisplay(DetailView):
    model=profilemodel
    template_name='home/profile.html'
    context_object_name='profile'
    
#-------------------------------------------------------
class LogoutTemp(LogoutView):
    template_name='home/logout.html'

#-------------------------------------------------------
class LoginTemp(LoginView):
    template_name='home/login.html'
    success_url=''

#-------------------------------------------------------
def ListofSpotuser(request):
    spots=spot.objects.filter(user=request.user)
    profile=profilemodel.objects.get(user=request.user)
    return render(request,'home/listuser.html',{'profile':profile,'notes':spots})

#-------------------------------------------------------






def ListofSpot(request):
    serchdistrict=searchFormbyDistrict
    if request.method == 'POST':
        filled_form=searchFormbyDistrict(request.POST)
        if filled_form.is_valid():
            result=filled_form.cleaned_data['district']
            print(result)
            note=spot.objects.filter(Q(name=result)|Q(discription__icontains=result),verify=True)
            newfilled_form=searchFormbyDistrict
            return render(request,'home/list.html',{'notes':note,'searchdis':newfilled_form})
    notes=spot.objects.filter(verify=True)
    return render(request,'home/list.html',{'notes':notes,'searchdis':serchdistrict})
#-------------------------------------------------------
def deleteReview(request,pk,pk1):
    reviewmodel.objects.get(pk=pk).delete()
    return redirect(DetailofSpot,pk=pk1)
#-------------------------------------------------------
def DetailofSpot(request,pk):
    details=spot.objects.get(pk=pk,verify=True)
    addreview=reviewForm
    note=''
    if request.method=='POST':
        filled_form=reviewForm(request.POST)
        if filled_form.is_valid():
            profile=filled_form.save(commit=False)
            profile.user=request.user
            profile.spot=details
            profile.save()
            note='your review Posted'
            request.method=None
            ratings=reviewmodel.objects.filter(spot=details)
            return redirect(DetailofSpot,pk=details.pk)
    try:
        ratings=reviewmodel.objects.filter(spot=details).order_by('-date')
        return render(request,'home/detail.html',{'note':details,'ratings':ratings,'addingreview':addreview,'pop':note})
    except:
         return render(request,'home/detail.html',{'note':details,'addingreview':addreview})
        




#-------------------------------------------------------
@login_required(login_url='/login/')
def cretingView(request):
    nform=spotform
    if request.method == 'POST':
        filled_form=spotform(request.POST,request.FILES)
        if filled_form.is_valid():
            profile=filled_form.save(commit=False)
            profile.user=request.user
            profile.save()
            place_name=filled_form.cleaned_data['name']
            note="%s added" %place_name
            nform=spotform
            return redirect(cretingView)
        note='ERROR OCCURED!!'
        form=spotform
        return render(request,'home/create.html',{"form":nform,'note':note})
    return render(request,'home/create.html',{"form":nform})

#-------------------------------------------------------
def districtView(request,value):
    serchdistrict=searchFormbyDistrict
    if request.method == 'POST':
        filled_form=searchFormbyDistrict(request.POST)
        if filled_form.is_valid():   
            result=filled_form.cleaned_data['district']
            note=spot.objects.filter(name=result,verify=True)
            return render(request,'home/list.html',{'notes':note,'searchdis':serchdistrict})
    district=spot.objects.filter(district__district=value,verify=True)
    return render(request,'home/list.html',{'notes':district,'searchdis':serchdistrict})
#-------------------------------------------------------
def remarkView(request,value):
    serchdistrict=searchFormbyDistrict
    if request.method == 'POST':
        filled_form=searchFormbyDistrict(request.POST)
        if filled_form.is_valid():   
            result=filled_form.cleaned_data['district']
            note=spot.objects.filter(name=result,verify=True)
            return render(request,'home/list.html',{'notes':note,'searchdis':serchdistrict})
    remark=spot.objects.filter(type__alert=value,verify=True)
    return render(request,'home/list.html',{'notes':remark,'searchdis':serchdistrict})

