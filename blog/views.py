from django.shortcuts import render,redirect
from home.models import profilemodel
from django.core.paginator import Paginator
from .forms import reviewForm,blogform
from .models import blogmodel,reviewmodel_blog,profilemodel
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import DeleteView
from home.forms import searchFormbyDistrict
def Detailofblog(request,pk):
    details=blogmodel.objects.get(pk=pk)
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
            ratings=reviewmodel_blog.objects.filter(spot=details)
            return redirect(Detailofblog,pk=details.id)
    try:
        ratings=reviewmodel_blog.objects.filter(spot=details).order_by('-date')
        paginator = Paginator(ratings, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
       
        return render(request,'blog/blog.html',{'note':details,'ratings':page_obj,
                        'addingreview':addreview,'pop':note})
    except:
        
        return render(request,'blog/blog.html',{'note':details,'addingreview':addreview})
        
@login_required(login_url='/login/')    
def deleteReview(request,pk,pk1):
    reviewmodel_blog.objects.get(pk=pk).delete()
    return redirect(Detailofblog,pk=pk1)



@login_required(login_url='/login/')
def creatingView(request):
    nform=blogform
    try:
        check=request.user.profilemodel
        if request.method == 'POST':
            filled_form=blogform(request.POST,request.FILES)
            if filled_form.is_valid():
                profile=filled_form.save(commit=False)
                profile.user=request.user
                profile.save()

                nform=blogform
                return redirect('listuser')
            note='ERROR OCCURED!! Try again!!'
            form=blogform
            return render(request,'blog/create.html',{"form":form,'note':note})
        return render(request,'blog/create.html',{"form":nform})
    except:
        return redirect('profilecreate')

@login_required(login_url='/login/')
def updateTemp(request,pk):
    edit_object=blogmodel.objects.get(pk=pk,user=request.user)
    form=blogform(instance=edit_object)
    if request.method == 'POST':
        filled_form=blogform(request.POST,request.FILES,instance=edit_object)
        if filled_form.is_valid():
            filled_form.save()
            form=filled_form
            note="updated"
            return redirect('listuser')
        note='try again'
        return render(request,'blog/edit.html',{'form':form,'edit':edit_object,'note':note})
    return render(request,'blog/edit.html',{'form':form,'edit':edit_object})


def ListofBlog(request):
    serchdistrict=searchFormbyDistrict
    if request.method == 'POST':
        filled_form=searchFormbyDistrict(request.POST)
        if filled_form.is_valid():
            results=filled_form.cleaned_data['district']
            results=results.split()
            query = reduce(operator.or_, (Q(title__icontains=result)|Q(content__icontains=result)|
                                        Q(place__icontains=result)|Q(keyword__icontains=result)|
                                        Q(user__profilemodel__Name__icontains=result) for result in results))
            note=blogmodel.objects.filter(query,verify=True)
            newfilled_form=searchFormbyDistrict
            paginator = Paginator(note, 16)
            page_number = request.GET.get('page')
            note = paginator.get_page(page_number)
            return render(request,'blog/list.html',{'notes':note,'value':results,'searchdis':newfilled_form})
    notes=blogmodel.objects.filter(verify=True)
    paginator = Paginator(notes, 16)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    passn='kerala'
    return render(request,'blog/list.html',{'notes':page_obj,'value':passn,'searchdis':serchdistrict})


class DeleteTemp(LoginRequiredMixin,DeleteView):
    model=blogmodel
    login_url='/login/'
    success_url='/spotsuser/'
    template_name='blog/delete.html'
    def get(self, request, *args, **kwargs):
        self.object = blogmodel.objects.get(pk=kwargs.get('pk'),user=request.user)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)