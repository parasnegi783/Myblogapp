from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_otp')
    otp = models.CharField(max_length=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} - OTP: {self.otp}"

class Blog(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, default="Untitled Blog")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog')
    meta = models.CharField(max_length=300, default="No meta information available.")
    content = models.TextField(default="Content coming soon...")
    thumbnail_img = models.ImageField(null=True, blank=True, upload_to="images/")
    category = models.CharField(max_length=255, default="uncategorized")
    time = models.DateField(auto_now_add=True, null=True, blank=True)
    favorited_by = models.ManyToManyField(User, related_name='favorites', blank=True)
    certificate = models.FileField(upload_to='certificates/', null=True, blank=True)  # New field for certificate

    def __str__(self):
        return self.title

class BlogImage(models.Model):
    blog = models.ForeignKey(Blog, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog_images/')

class Technology(models.Model):
    name = models.CharField(max_length=50)
    icon_class = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    meta = models.CharField(max_length=300, default="No meta information available.",null=True, blank=True)
    description = models.TextField(default="Description coming soon...")
    technologies = models.ManyToManyField(Technology)
    github_link = models.URLField(blank=True, null=True)
    demo_link = models.URLField(blank=True, null=True)
    P_favorited = models.ManyToManyField(User, related_name='P_favorites', blank=True)
    category = models.CharField(max_length=255, default="uncategorized", null=True, blank=True)



    def __str__(self):
        return self.title

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='projects/')


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Optional ForeignKey to User
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, null=True, blank=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"


class Skill(models.Model):
    SkillName = models.CharField(max_length=100)
    level = models.IntegerField(default=0)  # Level from 0 to 100

    def __str__(self):
        return self.SkillName

class AboutMe(models.Model):
    name = models.CharField(max_length=100)
    introduction = models.TextField()
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    skills = models.ManyToManyField(Skill, related_name='about_me', blank=True)

    def __str__(self):
        return "About Me"

