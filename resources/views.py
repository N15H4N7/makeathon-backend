from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from PyPDF2 import PdfFileWriter, PdfFileReader
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def all_resources(request):
    resources = Resource.objects.order_by('-id')
    context = {
        'resources' : resources,
    }
    return render(request, 'resources/all_resources.html', context)

@login_required
def post_resource(request):
    if request.method == "POST":
        form = NewResourceForm(request.POST, request.FILES)
        if form.is_valid():
            print("help")
            f = form.save()
            pages_to_keep = [1] # page numbering starts from 0
            infile = PdfFileReader(f.pdf_file, 'rb')
            output = PdfFileWriter()

            for i in pages_to_keep:
                p = infile.getPage(i)
                output.addPage(p)

            with open('media/preview/'+str(f.id)+'_preview.pdf', 'wb+') as fi:
                output.write(fi)    

            f.preview = 'media/preview/'+str(f.id)+'_preview.pdf'
            f.owner_id = request.user
            f.save()

            return redirect('all-resources')

    else:
        form = NewResourceForm()

    context = {
        'form' : form,
    }

    return render(request, 'resources/resource_form.html', context)

@login_required
def like_resource(request, pk):
    resource = get_object_or_404(Resource, id=pk)
    if(resource.buyer.filter(id=pk)):
        resource.liked_by.add(request.user)
        resource.save()
    else:
        messages.add_message(request, messages.INFO, 'You\'ll need to buy this course to like it.')
    return redirect('all-resources')

@login_required
def dislike_resource(request, pk):
    res = get_object_or_404(Resource, id=pk)
    res.liked_by.remove(request.user)
    res.save()
    return redirect('all-resources')

@login_required
def update_resource(request, pk):
    resource = Resource.objects.get(id=pk)
    if(Resource.objects.get(id=pk).owner == request.user):
        if(request.method == 'POST'):
            form = UpdateResourceForm(request.POST, instance = resource)
            if form.is_valid():
                form.save()
                return redirect('all-resources')
        form = UpdateResourceForm(instance = resource)
        context = {
            'form' : form,
        }
    else:
        return redirect('all-resources')
    return render(request, 'resources/resource_update.html', context)

@login_required
def delete_resource(request, pk):
    resource = get_object_or_404(Resource, id=pk)
    if(request.user == resource.owner):
        if not resource.buyer.exists():
            resource.delete()
        else:
            messages.add_message(request, messages.INFO, 'The resources that have been sold cannot be deleted.')
    return redirect('all-resources')

@login_required
def my_posted_resources(request):
    resources = Resource.objects.filter(owner=request.user)
    context = {
        'resources': resources,
    } 
    return render(request, 'resources/my_posted_resources.html', context)

@login_required
def my_bought_resources(request):
    resources = Resource.objects.filter(buyer=request.user)
    context = {
        'resources': resources,
    } 
    return render(request, 'resources/my_bought_resources.html', context)
