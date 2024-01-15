from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from myApp.forms import ToLetModelForm
from myApp.models import toLet_model, rentApplyModel
from django.db.models import Count, Q
from datetime import datetime, timedelta
from myApp.models import *
from notifications.signals import notify
from myApp.models import Custom_User
from django.core.files.storage import FileSystemStorage  # Import for file storage


# home page 
def homePage(request):
    if request.user.is_authenticated:
        return redirect('homePage')

    return render(request, 'home.html')


def signupPage(request):

    if request.method == "POST":

        user_name= request.POST.get('username')
        displayname= request.POST.get('display_name')
        mail= request.POST.get('email')
        pass_word= request.POST.get('password')
        usertype= request.POST.get('user_type')

        user = Custom_User.objects.create_user(username=user_name,password=pass_word)
        user.display_name=displayname
        user.email=mail
        user.user_type=usertype
        user.save()

        profile=profileProfile.objects.create(user=user)

        if user.user_type == 'profile':
            profile=profileProfile.objects.create(user=user)
            profile.save()

        return redirect("signinPage")

    return render(request,'signup.html')

@login_required
def logoutPage(request):

    logout(request)

    return redirect('homePage')


def signinPage(request):

    if request.method == "POST":

        user_name= request.POST.get('username')
        password= request.POST.get('password')
        user = authenticate(username=user_name, password=password)

        print(user)

        if user:
            login(request,user)
            return redirect("dashboardPage")


    return render(request,'login.html')


@login_required
def dashboardPage(request):
    # Retrieve all posts
    search = request.GET.get("search")
    print(search)
    if search:
        # allPost = toLet_model.objects.filter(rent_title__icontains=search)
        allPost = toLet_model.objects.filter(Q(rent_title__icontains=search) | Q(location__icontains=search)).order_by('-create_at')
        print(allPost)
        
    else:
        allPost = toLet_model.objects.all().order_by('-create_at')

    # Retrieve recent posts (assuming you have a date field named create_at)
    recent_posts = toLet_model.objects.order_by('-create_at')[:5]  # Retrieve the 5 most recent posts

    # Total post count
    total_post_count = allPost.count()

    # Last 7 days post count
    seven_days_ago = datetime.now() - timedelta(days=7)
    last_7_days_post_count = toLet_model.objects.filter(create_at__gte=seven_days_ago).count()

    context = {
        'all_posts': allPost,
        'recent_posts': recent_posts,
        'total_post_count': total_post_count,
        'last_7_days_post_count': last_7_days_post_count,
    }


    return render(request, 'dashboard.html', context)


def viewrentPage(request):

    rent=toLet_model.objects.all()

    context={
        'rent':rent
    }
    return render(request,"viewrent.html",context)


@login_required
def add_rent_Page(request):
    user = request.user
    if request.method == 'POST':
        rent_title = request.POST.get('rent_title')
        location = request.POST.get('location')
        homeDescription = request.POST.get('homeDescription')  # Correct field name
        rentDescription = request.POST.get('rentDescription')  # Correct field name
        deadline = request.POST.get('deadline')
        nid = request.POST.get('nid')
        homePicture = request.FILES.get('homePicture')

        rent=toLet_model(
            rent_title=rent_title,
            location=location,
            homeDescription=homeDescription,  # Correct field name
            rentDescription=rentDescription,  # Correct field name
            deadline=deadline,
            nid=nid,
            homePicture=homePicture,
            rent_creator=user,
        )
        rent.save()

        profile = Custom_User.objects.filter(user_type='profile')
        verb = "Added a New rent!"
        actor = request.user
        print('actor', actor,'-- profile', profile, '--verb', verb, '---recipient', profile)
        notify.send(actor, recipient=profile, verb=verb,target_content_type=rent, action_object=rent)
        return redirect("viewrentPage")
    
    return render(request,'user/Addrent.html')

@login_required
def deletePage(request,myid):

    rent=toLet_model.objects.filter(id=myid)
    rent.delete()

    return redirect("viewrentPage")

@login_required
def editPage(request,myid):

    rent=toLet_model.objects.filter(id=myid)

    return render(request,'user/editrent.html',{'rent':rent})

@login_required
def updatePage(request):

    user = request.user
    if request.method == 'POST':

        rent_id=request.POST.get('rentid')
        rent_title=request.POST.get('rent_title')
        location=request.POST.get('location')
        homeDescription=request.POST.get('homeDescription')
        rentDescription=request.POST.get('rentDescription')
        deadline=request.POST.get('deadline')
        nid=request.POST.get('nid')
        image= request.FILES.get('homePicture')
        rent=toLet_model(
            id=rent_id,
            rent_title=rent_title,
            location=location,
            homeDescription=homeDescription,
            rentDescription=rentDescription,
            deadline=deadline,
            homePicture=image,
            nid=nid,
            rent_creator=user,
        )
        rent.save()
        return redirect("viewrentPage")


@login_required
def applyPage(request, myid):
    rent = get_object_or_404(toLet_model, id=myid)

    if request.method == 'POST':
        nid = request.POST.get('nid')

        # Check if NID and NID image are provided
        if nid and request.FILES.get('nid_image'):
            profile = request.user

            # Save NID image to media directory
            nid_image = request.FILES['nid_image']
            fs = FileSystemStorage()
            filename = fs.save(f'nid_images/{nid_image.name}', nid_image)

            # Create rent application object
            application = rentApplyModel.objects.create(
                rent=rent,
                applicant=profile,
                nid=nid,
                nid_image=filename,  # Save the filename in the model
            )
            application.save()

            # Update the is_applied field in the toLet_model model
            rent.is_applied = True
            rent.save()

            messages.success(request, 'Application submitted successfully.')
            return redirect("myaccount")
        else:
            messages.error(request, 'Error in the application form, please check it.')

    context = {
        'rent': rent
    }

    return render(request, 'user/applyrent.html', context)

# ProfilePage
@login_required
def myaccount(request):
    
    
    return render(request,'myaccount.html')


@login_required
def EditProfilePage(request):
    user=request.user
    
    if request.method == "POST":
        user_id= request.POST.get('user_id')
        first_name= request.POST.get('first_name')
        last_name= request.POST.get('last_name')
        display_name= request.POST.get('display_name')
        nid= request.POST.get('nid')
        about= request.POST.get('about')
        email= request.POST.get('email')
        image= request.FILES.get('profile_picture')
        entered_password= request.POST.get('password')

        if not check_password(entered_password,user.password):
            messages.error(request,'Profile not updated,Wrong Password')
            return redirect("EditProfilePage")
        
        profile=profileProfile.objects.get(user=user)
        profile.nid=nid
        profile.save()

        user.id=user_id
        user.first_name=first_name
        user.last_name=last_name
        user.display_name=display_name
        user.about=about
        user.email=email

        if image:
            user.profile_picture=image
        user.save()

        messages.success(request,'Profile Updated Successfully')

        return redirect("profilepage")

    return render(request,'Editprofile.html')

def changePasswordPage(request):

    user=request.user

    if request.method =='POST':
        old_password=request.POST.get('currentPassword')
        newPassword=request.POST.get('newPassword')
        confirmPassword=request.POST.get('confirmPassword')

        if not check_password(old_password,user.password):
            messages.error(request,'Wrong Password')
            return redirect("changePasswordPage")
        
        if newPassword!=confirmPassword:
            messages.error(request,'Password Not Matched')
            return redirect("changePasswordPage")
        
        else:
            user.set_password(confirmPassword)

            user.save()
            return redirect("signinPage")

    return render(request,'changepassword.html')

def createdrentByProfile(request):
    user=request.user

    creator=toLet_model.objects.filter(rent_creator=user)

    context={
        'creator':creator
    }

    return render(request,'createdrent.html',context)
    

def edit_post(request, post_id):
    post = get_object_or_404(toLet_model, pk=post_id)

    if post.user_can_edit(request.user):
        # User has permission to edit the post
        if request.method == 'POST':
            form = ToLetModelForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                # Redirect to the post detail page or another appropriate view
                return redirect('post_detail', post_id=post_id)
        else:
            form = ToLetModelForm(instance=post)

        return render(request, 'edit_post.html', {'form': form, 'post': post})
    else:
        # User doesn't have permission to edit the post
        return HttpResponseForbidden("You don't have permission to edit this post.")
    
@login_required
def applied_rents(request):
    # Assuming you have a ForeignKey relationship in rentApplyModel pointing to toLet_model
    applied_rents = rentApplyModel.objects.filter(applicant=request.user)

    if request.method == 'POST':
        rent_apply_id = request.POST.get('rent_apply_id')
        delete_rent_apply = rentApplyModel.objects.filter(id=rent_apply_id, applicant=request.user)
        
        if delete_rent_apply.exists():
            delete_rent_apply.delete()
            messages.success(request, 'Applied Rent deleted successfully.')
        else:
            messages.error(request, 'Error deleting the Applied Rent.')

        return redirect('applied_rents')

    return render(request, 'user/applied_rents.html', {'applied_rents': applied_rents})


# applicant details 
@login_required
def post_details(request, post_id):
    post = get_object_or_404(toLet_model, id=post_id)
    applicants = rentApplyModel.objects.filter(rent=post)

    context = {
        'post': post,
        'applicants': applicants,
    }

    return render(request, 'post_details.html', context)

def notifications_page(request):
    
    return render(request, 'notifications.html')


@login_required
def chatPage(request):
    # Your chat logic here
    return render(request, 'chat.html')


@login_required
def profilepage(request):
    return render(request, 'profilepage.html')



