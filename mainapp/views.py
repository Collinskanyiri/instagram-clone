from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import UpdateProfileForm,CreateNewPostForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from mainapp.models import *
from django.shortcuts import get_object_or_404
from django.urls import reverse
import cloudinary
import cloudinary.uploader
import cloudinary.api


@login_required(login_url='login')
def index(request):
    message="Welcome to Instagram"
    images = Image.objects.all()
    return render(request, 'insta/index.html', {'images':images, 'message':message })

@login_required(login_url='login')
def profile(request):
    current_user =request.user
    profile_photo = Image.objects.filter(user_id=current_user.id)

    profile = Profile.objects.filter(user_id=current_user.id).first()
    return render(request, 'profile.html', {" profile_photo":  profile_photo, "profile": profile})

@login_required(login_url='login')
def save_image(request):
    if request.method == 'POST':
        image_name = request.POST['image_name']
        image_caption = request.POST['image_caption']
        image_file = request.FILES['image_file']
        image_file = cloudinary.uploader.upload(image_file)
        image_url = image_file['url']

        image = Image(image_name=image_name, image_file=image_file,image_caption=image_caption, image=image_url,
                      profile_id=request.POST['user_id'], user_id=request.POST['user_id'])
        image.save_image()

        return redirect('/profile', {'success': 'Image Uploaded Successfully'})
    else:
        return render(request, 'profile.html', {'message':'Upload image!'})

@login_required(login_url='login')
def like_image(request, id):
    likes = Likes.objects.filter(image_id=id).first()
    if Likes.objects.filter(image_id=id, user_id=request.user.id).exists():
        # This will unlike
        likes.delete()
        image = Image.objects.get(id=id)
        if image.likes == 0:
            image.likes = 0
            image.save()
        else:
            image.likes -= 1
            image.save()
        return redirect('home')
    else:
        likes = Likes(image_id=id, user_id=request.user.id)
        likes.save()
        image = Image.objects.get(id=id)
        image.likes = image.likes + 1
        image.save()
        return redirect('home')

@login_required(login_url='login')
def single_image(request, id):
    image = Image.objects.get(id=id)
    related_images = Image.objects.filter(
        user_id=image.user_id).order_by('-image_date')
    title = image.image_name
    if Image.objects.filter(id=id).exists():
        comments = Comment.objects.filter(image_id=id)
        return render(request, 'Image.html', {'image': image, 'comments': comments, 'images': related_images, 'title': title})
    else:
        return redirect('home')

@login_required(login_url='login')
def save_comment(request):
    if request.method == 'POST':
        comment = request.POST['comment']
        image_id = request.POST['image_id']
        image = Image.objects.get(id=image_id)
        user = request.user
        comment = Comment(comment=comment, image_id=image_id, user_id=user.id)
        comment.save_comment()
        image.comments = image.comments + 1
        image.save()
        return redirect('/picture/' + str(image_id))
    else:
        return redirect('home')

@login_required(login_url='login')
def user_profile(request, id):

    if User.objects.filter(id=id).exists():
        user = User.objects.get(id=id)

        profile = Profile.objects.filter(user_id=id).first()
        profile_photo = request.FILES['profile_pic']
        profile_photo = cloudinary.uploader.upload( profile_photo)
        return render(request, 'user_profile.html', {'results':  profile_photo, 'profile': profile, 'user': user})
    else:
        return redirect('home')

@login_required(login_url='login')
def create_post(request):

    post = Image(user = request.user)
    if request.method == 'POST':
        form = CreateNewPostForm(request.POST,request.FILES,instance=post)
        if form.is_valid():
            form.save()
            messages.success(request,"Post created!")
        return redirect('home')
    else:
        form = CreateNewPostForm(instance=post)
        return render(request,'new_post.html',{'form':form})

@login_required(login_url='login')
def update_profile(request):

    if request.method == 'POST':
        form = UpdateProfileForm(request.POST,instance=request.user.profile)
        profile_photo = request.FILES['profile_pic']
        profile_photo = cloudinary.uploader.upload( profile_photo)
        if form.is_valid():
            form.save() 
            return redirect('user_profile',request.user.pk)
        else:
            form = UpdateProfileForm(instance=request.user.profile)
            return render(request,'update_profile.html',{"form":form})
    else:
        form = UpdateProfileForm(instance=request.user.profile)
        return render(request,'update_profile.html',{"form":form})

@login_required(login_url='login')
def search_images(request):
    if 'search' in request.GET and request.GET['search']:
        search_term = request.GET.get('search').lower()
        results = Image.search_by_image_name(search_term)

        message = f'{search_term}'
        params = {
            'results': results,
            'message': message
        }

        return render(request, 'search.html',params)
    else:
        message = 'Enter your search keyword'
        return render(request, 'search.html', {'message': message})


