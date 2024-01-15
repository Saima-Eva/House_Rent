from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
from django.contrib.contenttypes.models import ContentType



class Custom_User(AbstractUser):
    USER=[
        ('profile','Profile')
    ]
    display_name=models.CharField(max_length=100)
    email=models.EmailField()
    password=models.CharField(max_length=100)
    confirm_password=models.CharField(max_length=100)
    about=models.TextField(null=True)
    user_type=models.CharField(choices=USER,max_length=120, null=True)
    profile_picture=models.ImageField(upload_to='media/profile_pic',null=True)
    def __str__(self):
        return self.display_name
    
    
class toLet_model(models.Model):

    rent_title=models.CharField(max_length=100,null=True)
    location=models.CharField(max_length=100,null=True)
    homeDescription=models.TextField(null=True)
    rentDescription=models.TextField(null=True)
    deadline=models.TextField(null=True)
    nid=models.TextField(null=True)
    create_at = models.DateTimeField(auto_now_add=True,null=True)
    update_at = models.DateTimeField(auto_now=True,null=True)
    rent_creator = models.ForeignKey(Custom_User,on_delete=models.CASCADE)
    homePicture=models.ImageField(upload_to='media/homePicture',null=True)

    def user_can_edit(self, user):
        return user == self.rent_creator

    def user_can_delete(self, user):
        return user == self.rent_creator

    class Meta:
        permissions = [
            ('can_edit_own_post', 'Can edit own post'),
        ]
    
    def __str__(self):
        return self.rent_title
    
    is_applied = models.BooleanField(default=False)

class profileProfile(models.Model):
    user = models.OneToOneField(Custom_User,on_delete=models.CASCADE,null=True, related_name='profileProfile')
    nid=models.CharField(max_length=100,null=True,blank=True)
    
    def __str__(self):
        return self.user.display_name
       


class rentApplyModel(models.Model):
    rent = models.ForeignKey(toLet_model, on_delete=models.CASCADE, null=True)
    applicant = models.ForeignKey(Custom_User, on_delete=models.CASCADE, null=True)
    nid = models.CharField(max_length=100, null=True)
    nid_image = models.ImageField(upload_to='nid_images/', null=True)  # Add this line for the NID image

    def get_applicant_profile(self):
        return self.applicant.profileProfile

    def __str__(self):
        return f"{self.applicant.display_name} Applied for {self.rent.rent_title}"