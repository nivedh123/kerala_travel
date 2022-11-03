from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from .models import spot
from django.views.generic import ListView,DetailView
from django.views.generic.edit import DeleteView
from django.contrib.auth.views import LoginView,LogoutView
from .forms import spotform,CustomUserCreationForm,searchFormbyDistrict
from django.shortcuts import redirect, render  
#-------------------------------------------------------
@login_required(login_url='/spots/')
def updateTemp(request,pk):
    edit_object=spot.objects.get(pk=pk)
    form=spotform(instance=edit_object)
    if request.method == 'POST':
        filled_form=spotform(request.POST,request.FILES,instance=edit_object)
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
    last_ten = spot.objects.all()[:10]
    return render(request,'home/home.html',{'spots':last_ten})
#-------------------------------------------------------
def register(request):  
    if request.method == 'POST':  
        form = CustomUserCreationForm
        filled_form=CustomUserCreationForm(request.POST)
        if filled_form.is_valid():  
            filled_form.save()  
            note='new account created'
            context = {  
                'note':note,
                'form':form 
            } 
            return render(request, 'home/signup.html', context)  

    else:  
        form = CustomUserCreationForm  
        note='new  not account created'
        context = {  
                'note':note,
                'form':form 
            } 
        return render(request, 'home/signup.html', context)  

class LogoutTemp(LogoutView):
    template_name='home/logout.html'


class LoginTemp(LoginView):
    template_name='home/login.html'
    success_url='login/'

#-------------------------------------------------------
class ListofSpotuser(LoginRequiredMixin,ListView):
    model=spot
    context_object_name='notes'
    template_name='home/listuser.html'
    login_url='/login/'
    def get_queryset(self):
        return self.request.user.spot.all()
#-------------------------------------------------------






def ListofSpot(request):
    serchdistrict=searchFormbyDistrict
    if request.method == 'POST':
        filled_form=searchFormbyDistrict(request.POST)
        print('stage1')
        if filled_form.is_valid():
            print('stage2')
            result=filled_form.cleaned_data['distri']
            note=spot.objects.filter(district=result)
            return render(request,'home/list.html',{'notes':note,'searchdis':serchdistrict})
    notes=spot.objects.all()
    return render(request,'home/list.html',{'notes':notes,'searchdis':serchdistrict})





#-------------------------------------------------------
class DetailofSpot(DetailView):
    model=spot
    context_object_name='note'
    template_name='home/detail.html'

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
            form=spotform
            return render(request,'home/create.html',{"form":form,'note':note})
        note='ERROR OCCURED!!'
        form=spotform
        return render(request,'home/create.html',{"form":nform,'note':note})
    return render(request,'home/create.html',{"form":nform})

#-------------------------------------------------------