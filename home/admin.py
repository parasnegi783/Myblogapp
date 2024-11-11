from django.contrib import admin
from django import forms
from home.models import Blog, Project, Technology, ProjectImage, Contact, AboutMe, Skill, UserOTP
from django.utils.translation import gettext_lazy as _

admin.site.site_header = "MyPortfolioAdmin"
admin.site.site_title = "MyPortfolioAdmin Portal"
admin.site.index_title = "Welcome to MyPortfolio Admin"

# Blog Admin
class BlogAdminForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'id': "richtext_field"}))

    class Meta:
        model = Blog
        fields = "__all__"

class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm
    list_display = ('title', 'category', 'time', 'user')
    search_fields = ('title', 'content', 'category', 'user__username')
    list_filter = ('category', 'time')

admin.site.register(Blog, BlogAdmin)

# Project Admin
class ProjectAdminForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'id': "richtext_field_project"}))

    class Meta:
        model = Project
        fields = "__all__"

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1

class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm
    inlines = [ProjectImageInline]
    list_display = ('title', 'get_technologies', 'github_link', 'demo_link')
    search_fields = ('title', 'description')
    list_filter = ('technologies',)  # Allows filtering by technologies

    def get_technologies(self, obj):
        return ", ".join([tech.name for tech in obj.technologies.all()])
    get_technologies.short_description = 'Technologies Used'

admin.site.register(Project, ProjectAdmin)

# Technology Admin
@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_class')
    search_fields = ('name',)

# Contact Admin
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'submitted_at')
    search_fields = ('name', 'email')
    list_filter = ('submitted_at',)
    readonly_fields = ('submitted_at',)

admin.site.register(Contact, ContactAdmin)

# Skill Admin
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('SkillName', 'level')
    search_fields = ('SkillName',)

# AboutMe Admin
@admin.register(AboutMe)
class AboutMeAdmin(admin.ModelAdmin):
    list_display = ('introduction',)
    search_fields = ('introduction',)
    filter_horizontal = ('skills',)


# @admin.register(UserOTP)
# class UserOTPAdmin(admin.ModelAdmin):
#     list_display = ('user', 'otp', 'created_at')
#     search_fields = ('user__username', 'otp')
#     list_filter = ('created_at')