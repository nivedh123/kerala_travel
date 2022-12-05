from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import spot,districts,remark,reviewmodel,profilemodel,cluster
from django.views.generic import ListView,DetailView,CreateView,TemplateView
from django.views.generic.edit import DeleteView,CreateView
from django.contrib.auth.views import LoginView,LogoutView
from .forms import spotform,searchFormbyDistrict,reviewForm,profileform,UserCreationForm
from django.shortcuts import render,redirect
from django.db.models import Q
from django.contrib.auth import logout
import operator
from functools import reduce
from django.core.paginator import Paginator
from .customfunct import RatingChartFeed
from blog.models import blogmodel
#-------------------------------------------------------
def home(request):
    serchdistrict=searchFormbyDistrict
    adition=cluster.objects.filter(publish=True)
    if request.method == 'POST':
        filled_form=searchFormbyDistrict(request.POST)
        if filled_form.is_valid():   
            results=filled_form.cleaned_data['district']
            results=results.split()
            query = reduce(operator.or_, (Q(name__icontains=result)|Q(short_discription__icontains=result)|
                                        Q(district__district__icontains=result)|Q(discription__icontains=result)|
                                        Q(type__alert__icontains=result)|Q(cluster__name__icontains=result)|
                                        Q(key_words__icontains=result) for result in results))
            note=spot.objects.filter(query,verify=True)
            return render(request,'home/list.html',{'notes':note,'value':results,'searchdis':serchdistrict})
    remarks=remark.objects.all()
    district_ten = districts.objects.all()
    return render(request,'home/tourist-places-in-kerala.html',{'adition':adition,'district':district_ten,'remarks':remarks,'searchdis':serchdistrict})

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
            return redirect('listuser')
        return render(request,'home/edit.html',{'form':form,'edit':edit_object,'note':note})
    return render(request,'home/edit.html',{'form':form,'edit':edit_object})
#-------------------------------------------------------
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
    def get(self, request, *args, **kwargs):
        self.object = spot.objects.get(pk=kwargs.get('pk'),user=request.user)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
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
    success_url='/spotsuser/' 
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
    blog=blogmodel.objects.filter(user=request.user)
    try:
        profile=profilemodel.objects.get(user=request.user)
    except:
        return redirect('profilecreate')
    url=str(profile.id)
    return render(request,'home/listuser.html',{'blog':blog,'profile':profile,'url':url,'notes':spots})

#-------------------------------------------------------





def ListofSpot(request):
    serchdistrict=searchFormbyDistrict
    if request.method == 'POST':
        filled_form=searchFormbyDistrict(request.POST)
        if filled_form.is_valid():
            results=filled_form.cleaned_data['district']
            results=results.split()
            query = reduce(operator.or_, (Q(name__icontains=result)|Q(short_discription__icontains=result)|
                                        Q(district__district__icontains=result)|Q(discription__icontains=result)|
                                        Q(type__alert__icontains=result)|Q(cluster__name__icontains=result)|
                                        Q(key_words__icontains=result) for result in results))
            note=spot.objects.filter(query,verify=True)
            newfilled_form=searchFormbyDistrict
            paginator = Paginator(note, 16)
            page_number = request.GET.get('page')
            note = paginator.get_page(page_number)
            return render(request,'home/list.html',{'notes':note,'value':results,'searchdis':newfilled_form})
    notes=spot.objects.filter(verify=True)
    paginator = Paginator(notes, 16)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    passn='kerala'
    return render(request,'home/list.html',{'notes':page_obj,'value':passn,'searchdis':serchdistrict})
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
            if request.user.is_authenticated:

                profile=filled_form.save(commit=False)
                profile.user=request.user
                profile.spot=details
                profile.save()
            else:
                profile=filled_form.save(commit=False)
                user=profilemodel.objects.get(Name='anonymous')
                profile.user=user.user
                profile.spot=details
                profile.save()

            note='your review Posted'
            request.method=None
            ratings=reviewmodel.objects.filter(spot=details)
            return redirect(DetailofSpot,pk=details.pk)
    try:
        ratings=reviewmodel.objects.filter(spot=details).order_by('-date')
        paginator = Paginator(ratings, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        ratingchart=RatingChartFeed(details)
        print(ratingchart)
        return render(request,'home/detail.html',{'note':details,'ratings':page_obj,
                        'percentage':ratingchart,'addingreview':addreview,'pop':note})
    except:
        
        return render(request,'home/detail.html',{'note':details,'addingreview':addreview})
        
    



#-------------------------------------------------------
@login_required(login_url='/login/')
def cretingView(request):
    nform=spotform
    try:
        check=request.user.profilemodel
        if request.method == 'POST':
            filled_form=spotform(request.POST,request.FILES)
            if filled_form.is_valid():
                profile=filled_form.save(commit=False)
                profile.user=request.user
                profile.save()
                place_name=filled_form.cleaned_data['name']
                nform=spotform
                return redirect('listuser')
            note='ERROR OCCURED!! Try again!!'
            form=spotform
            return render(request,'home/create.html',{"form":nform,'note':note})
        return render(request,'home/create.html',{"form":nform})
    except:
        return redirect('profilecreate')
#-------------------------------------------------------
def districtView(request,value):
    serchdistrict=searchFormbyDistrict
    if request.method == 'POST':
        filled_form=searchFormbyDistrict(request.POST)
        if filled_form.is_valid():   
            results=filled_form.cleaned_data['district']
            results=results.split()
            query = reduce(operator.or_, (Q(name__icontains=result)|Q(short_discription__icontains=result)|
                                        Q(district__district__icontains=result)|Q(discription__icontains=result)|
                                        Q(type__alert__icontains=result)|Q(cluster__name__icontains=result)|
                                        Q(key_words__icontains=result) for result in results))
            note=spot.objects.filter(query,verify=True)
            paginator = Paginator(note, 16)
            page_number = request.GET.get('page')
            note = paginator.get_page(page_number)
            return render(request,'home/list.html',{'notes':note,'value':results,'searchdis':serchdistrict})
    district=spot.objects.filter(district__district=value,verify=True)
    paginator = Paginator(district, 16)
    page_number = request.GET.get('page')
    remark = paginator.get_page(page_number)
    return render(request,'home/list.html',{'notes':remark,'value':value,'searchdis':serchdistrict})
#-------------------------------------------------------
def remarkView(request,value):
    serchdistrict=searchFormbyDistrict
    if request.method == 'POST':
        filled_form=searchFormbyDistrict(request.POST)
        if filled_form.is_valid():   
            results=filled_form.cleaned_data['district']
            results=results.split()
            query = reduce(operator.or_, (Q(name__icontains=result)|Q(short_discription__icontains=result)|
                                        Q(district__district__icontains=result)|Q(discription__icontains=result)|
                                        Q(type__alert__icontains=result)|Q(cluster__name__icontains=result)|
                                        Q(key_words__icontains=result) for result in results))
            note=spot.objects.filter(query,verify=True)
            paginator = Paginator(note, 16)
            page_number = request.GET.get('page')
            remark = paginator.get_page(page_number)
            return render(request,'home/list.html',{'notes':remark,'value':results,'searchdis':serchdistrict})
    notes=spot.objects.filter(type__alert=value,verify=True)
    paginator = Paginator(notes, 16)
    page_number = request.GET.get('page')
    remark = paginator.get_page(page_number)
    return render(request,'home/list.html',{'notes':remark,'value':value,'searchdis':serchdistrict})

#-------------------------------------------------------
def clusterView(request,value):
    serchdistrict=searchFormbyDistrict
    if request.method == 'POST':
        filled_form=searchFormbyDistrict(request.POST)
        if filled_form.is_valid():   
            results=filled_form.cleaned_data['district']
            results=results.split()
            query = reduce(operator.or_, (Q(name__icontains=result)|Q(short_discription__icontains=result)|
                                        Q(district__district__icontains=result)|Q(discription__icontains=result)|
                                        Q(type__alert__icontains=result)|Q(cluster__name__icontains=result)|
                                        Q(key_words__icontains=result) for result in results))
            note=spot.objects.filter(query,verify=True)
            paginator = Paginator(note, 16)
            page_number = request.GET.get('page')
            remark = paginator.get_page(page_number)
            return render(request,'home/list.html',{'notes':remark,'value':results,'searchdis':serchdistrict})
    notes=spot.objects.filter(cluster__name=value,verify=True)
    paginator = Paginator(notes, 16)
    page_number = request.GET.get('page')
    remark = paginator.get_page(page_number)
    return render(request,'home/list.html',{'notes':remark,'value':value,'searchdis':serchdistrict})
#-------------------------------------------------------
class Aboutview(TemplateView):
    template_name='home/about.html'
#-------------------------------------------------------