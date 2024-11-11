from django.shortcuts import render, redirect, get_object_or_404
from home.models import Blog, Project, BlogImage,UserOTP,Project, ProjectImage, Technology, Contact, AboutMe
from django.contrib import messages
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.core.paginator import Paginator
from django.db.models import Q
import random
import re
from django.core.mail import EmailMessage
from django.utils.timezone import now, timedelta, make_aware, datetime
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import random
import string
from django.contrib.auth.decorators import login_required


def index (request):
    random_blogs = Blog.objects.all()
    context = {'random_blogs': random_blogs}
    return render(request, 'index.html', context)


def about(request):
    about_me = AboutMe.objects.first()  # Assuming there's only one instance
    latest_project = Project.objects.order_by('-id').first()  # Get the latest project by id (or use a date field)
    
    context = {
        'about_me': about_me,
        'latest_project': latest_project,
    }
    return render(request, 'about.html', context)


def thanks(request):
    return render(request, 'thanks.html')

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message_content = request.POST.get('message')
        invalid_input = ['', ' ']

        # Validate that no field is empty
        if name in invalid_input or email in invalid_input or phone in invalid_input or message_content in invalid_input:
            messages.error(request, 'One or more fields are empty!')
        else:
            # Email and phone regex patterns
            email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            phone_pattern = re.compile(r'^[0-9]{10}$')

            if not email_pattern.match(email):
                messages.error(request, 'Invalid email format!')
            elif not phone_pattern.match(phone):
                messages.error(request, 'Invalid phone number! Phone number must be 10 digits.')
            else:
                # Save the form data to the Contact model
                if request.user.is_authenticated:
                    user = request.user
                else:
                    user = None

                Contact.objects.create(
                    user=user,
                    name=name,
                    email=email,
                    phone=phone,
                    message=message_content
                )

                # Email sending logic using EmailMessage
                email_subject = "New Contact Form Query"
                email_body = f"Dear Admin,\n\nYou have received a new query from {name}.\n\nDetails:\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message_content}\n\nPlease respond accordingly."
                email = EmailMessage(subject=email_subject, body=email_body, to=['parasnegi783@gmail.com'])  # Use a valid email

                try:
                    email.send()
                    messages.success(request, 'Your query has been sent successfully!')
                except Exception as e:
                    messages.error(request, f"Failed to send your query. Error: {e}")

                return redirect('contact')


    return render(request, 'contact.html')


# ********************** Blog Related Views ********************** #

def blog(request):
    if request.GET.get('favorites') == 'true' and request.user.is_authenticated:
        blogs = Blog.objects.filter(favorited_by=request.user).prefetch_related('images').order_by('-time')
    elif request.GET.get('my_collection') == 'true' and request.user.is_authenticated:
        blogs = Blog.objects.filter(user=request.user).prefetch_related('images').order_by('-time')
    else:
        blogs = Blog.objects.all().prefetch_related('images').order_by('-time')

    paginator = Paginator(blogs, 3)
    page = request.GET.get('page')
    blogs = paginator.get_page(page)

    context = {'blogs': blogs}
    return render(request, 'blog.html', context)


def blogpost(request, id):
    blog = get_object_or_404(Blog, id=id)
    images = blog.images.all()
    
    context = {
        'blog': blog,
        'images': images
    }
    
    return render(request, 'blogpost.html', context)


@login_required
def add_blog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        meta = request.POST.get('meta')
        content = request.POST.get('content')
        category = request.POST.get('category')
        thumbnail_img = request.FILES.get('thumbnail_img')  # Optional thumbnail image
        images = request.FILES.getlist('images')  # Multiple images

        if not all([title, meta, content, category]):
            messages.error(request, "All fields except images are required.")
            return redirect('add_blog')

        # Create the Blog instance
        blog = Blog.objects.create(
            user=request.user,
            title=title,
            meta=meta,
            content=content,
            category=category,
            thumbnail_img=thumbnail_img  # This can be None if not provided/
        )

        # Handle multiple images
        for image in images:
            BlogImage.objects.create(blog=blog, image=image)

        messages.success(request, "Blog post created successfully!")
        return redirect('blogpost', id=blog.id)  # Redirect to the blog list or desired page
    else:
        return render(request, 'add_blog.html')


def search(request):
    query = request.GET.get('q')
    query_list = query.split()
    results = Blog.objects.none()
    for word in query_list:
        results = results | Blog.objects.filter(Q(title__contains=word) | Q(content__contains=word)).order_by('-time')
    paginator = Paginator(results, 3)
    page = request.GET.get('page')
    results = paginator.get_page(page)
    if len(results) == 0:
        message = "Sorry, no results found for your search query."
    else:
        message = ""
    return render(request, 'search.html', {'results': results, 'query': query, 'message': message})


def toggle_favorite(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    if blog.favorited_by.filter(id=request.user.id).exists():
        blog.favorited_by.remove(request.user)
    else:
        blog.favorited_by.add(request.user)
    return redirect('blog')


# ********************** Project Related Views ********************** #

@login_required
def add_project(request):
    technologies_dict = {
        'Python': 'fa-python',
        'JavaScript': 'fa-js',
        'HTML': 'fa-html5',
        'CSS': 'fa-css3',
        'Tailwind CSS': 'fa-tailwind',
        'Django': 'fa-django',
        'C': 'fa-c',
        'C++': 'fa-cplusplus',
        'Java': 'fa-java',
        'AWS': 'fa-aws',
        'React': 'fa-react',
        'Node.js': 'fa-node',
        'Bootstrap': 'fa-bootstrap',
        'PHP': 'fa-php',
        'Ruby': 'fa-ruby',
        'Go': 'fa-go',
        'Swift': 'fa-swift',
        'Kotlin': 'fa-kotlin',
        'SQL': 'fa-database',
        'TypeScript': 'fa-js-square',
        'Sass': 'fa-sass',
        'GraphQL': 'fa-graphql',
        'Perl': 'fa-perl',
        'Rust': 'fa-rust',
        'MATLAB': 'fa-matlab',
        'R': 'fa-r',
        'Lua': 'fa-lua',
        'Solidity': 'fa-solidity',
        'VHDL': 'fa-vhdl',
        'Assembly': 'fa-assembly',
        'F#': 'fa-sharp',
        'Haskell': 'fa-haskell',
        'Scala': 'fa-scala',
        'Elixir': 'fa-elixir',
        'Julia': 'fa-julia',
        'Tcl': 'fa-tcl',
        'ActionScript': 'fa-actions',
        'Clojure': 'fa-clojure',
        'Dart': 'fa-dart',
        'Groovy': 'fa-groovy',
    }

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        meta = request.POST.get('meta')
        category = request.POST.get('Project_category')
        technologies = request.POST.getlist('technologies')  
        github_link = request.POST.get('github_link')
        demo_link = request.POST.get('demo_link')
        custom_technology = request.POST.get('custom_technology')

        project = Project.objects.create(
            user=request.user,
            title=title,
            description=description,
            meta=meta,
            category=category,
            github_link=github_link,
            demo_link=demo_link
        )

        tech_objects = [Technology.objects.get_or_create(name=tech.strip())[0] for tech in technologies]
        if custom_technology:
            custom_tech, _ = Technology.objects.get_or_create(name=custom_technology)
            tech_objects.append(custom_tech)
        project.technologies.set(tech_objects)

        for image in request.FILES.getlist('images'):
            ProjectImage.objects.create(project=project, image=image)

        certificate = request.FILES.get('certificate')
        if certificate:
            project.certificate = certificate
            project.save()

        return redirect('project_detail', id=project.id)

    context = {
        'technologies_dict': technologies_dict,
    }
    return render(request, 'add_project.html', context)


@login_required
def project_detail(request, id):
    project = get_object_or_404(Project, id=id)
    return render(request, 'project_detail.html', {'project': project})


def projects(request):
    projects_list = Project.objects.all()
    for project in projects_list:
        for image in project.images.all():
            print(image.image.url)  # Check the URL being generated
    context = {
        'projects': projects_list
    }
    return render(request, 'projects.html', context)


def search(request):
    query = request.GET.get('q')
    query_list = query.split()
    results = Project.objects.none()
    for word in query_list:
        results = results | Project.objects.filter(Q(title__contains=word) | Q(description__contains=word)).order_by('-time')
    paginator = Paginator(results, 3)
    page = request.GET.get('page')
    results = paginator.get_page(page)
    if len(results) == 0:
        message = "Sorry, no results found for your search query."
    else:
        message = ""
    return render(request, 'search.html', {'results': results, 'query': query, 'message': message})

@login_required
def toggle_favorite_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if project.P_favorited.filter(id=request.user.id).exists():
        project.P_favorited.remove(request.user)
    else:
        project.P_favorited.add(request.user)
    return redirect('projects')

# ********************** Authentication Related Views ********************** #

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))


def send_otp_email(user):
    otp = generate_otp()

    try:
        user_otp, created = UserOTP.objects.get_or_create(user=user)  # Unpack the tuple
        user_otp.otp = otp  
        print(otp)
        print(user_otp.otp)
        user_otp.save() 

    except Exception as e:
        print(f"Exception occurred while saving OTP: {e}") 

    email_subject = "Your Account Activation OTP"
    email_body = f"Dear {user.username},\n\nYour OTP for account activation is: {otp}\nPlease enter this OTP on the activation page to activate your account.\n\nThank you."

    email = EmailMessage(subject=email_subject, body=email_body, to=[user.email])
    email.send()


def login_user(request):
    print("Inside the login_user function")
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "All fields are required.")
            return render(request, "registration/login.html")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:  
                return redirect('/admin/')
            else:
                return redirect('index')  
        else:
            print("User not found")
            messages.error(request, "Invalid username or password.")
            return render(request, "registration/login.html")
        
    return render(request, "registration/login.html")

def LogoutUser(request):
    logout(request)
    return redirect(login_user)

def register_user(request):
    print("Inside the register_user function")

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        full_name = request.POST.get('fname')

        print(f"Received POST data - Username: {username}, Email: {email}, Password1: {password1}, Password2: {password2}, Full Name: {full_name}")

        # Perform validation
        if not username or not email or not password1 or not password2:
            messages.error(request, "All fields are required.")
            print("Validation failed: All fields are required.")
            return render(request, "registration/register.html")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            print("Validation failed: Passwords do not match.")
            return render(request, "registration/register.html")

        try:
            validate_email(email)
            print(f"Validated email: {email}")
        except ValidationError:
            messages.error(request, "Invalid email address.")
            print("Validation failed: Invalid email address.")
            return render(request, "registration/register.html")

        User = get_user_model()

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            print(f"Validation failed: Username '{username}' is already taken.")
            return render(request, "registration/register.html")

        # Split full name into first name and last name
        if full_name:
            name_parts = full_name.split(' ', 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else 'None'
        else:
            first_name = 'None'
            last_name = 'None'

        # Create and save the user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = False
        user.save()
        print(f"User created: {user.username}, email: {user.email}, first_name: {user.first_name}, last_name: {user.last_name}, is_active: {user.is_active}")

        # Send OTP email
        send_otp_email(user)

        # Set session variables for countdown
        request.session['activation_uid'] = user.pk
        request.session['activation_expiry'] = (now() + timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:%S')
        ex = request.session.get('activation_expiry')
        print(ex)

        messages.success(request, "Please check your email for the OTP to complete the registration.")
        return redirect('activation_countdown')  # Redirect to the countdown page after registration
    return render(request, "registration/register.html")



User = get_user_model()

def activation_countdown(request):
    print("Entered activation_countdown view")  # Debugging: Indicate that the view was accessed

    activation_uid = request.session.get('activation_uid')
    activation_expiry = request.session.get('activation_expiry')

    print(f"Session activation_uid: {activation_uid}")  # Debugging: Check the value of activation_uid
    print(f"Session activation_expiry: {activation_expiry}")  # Debugging: Check the value of activation_expiry

    if not activation_uid or not activation_expiry:
        messages.error(request, "Invalid session data.")
        print("Error: Invalid session data. Redirecting to registration.")  # Debugging: Error detail
        return redirect('register')

    try:
        # Convert the naive datetime string to an aware datetime
        expiry_time = make_aware(datetime.strptime(activation_expiry, '%Y-%m-%d %H:%M:%S'))
        current_time = now()
        remaining_time = (expiry_time - current_time).total_seconds()
        print(f"Expiry time: {expiry_time}")  # Debugging: Check the expiry time
        print(f"Current time: {current_time}")  # Debugging: Check the current time
        print(f"Remaining time: {remaining_time} seconds")  # Debugging: Check the remaining time
    except Exception as e:
        messages.error(request, "Error calculating remaining time.")
        print(f"Exception occurred while calculating remaining time: {e}")  # Debugging: Exception detail
        return redirect('register')

    if request.method == "POST":
        otp = request.POST.get('otp').strip()

        try:
            user = User.objects.get(pk=activation_uid)
        except User.DoesNotExist:
            user = None
        print("user:", user)
        if user:
            try:
                # Retrieve the associated UserOTP instance
                user_otp = UserOTP.objects.get(user=user)
                print("user.otp:", user_otp.otp)

                # Check if the OTP matches
                if user_otp.otp == otp:
                    user.is_active = True
                    user.save()
                    messages.success(request, "Your account has been successfully activated!")
                    return redirect('login_user')
                else:
                    messages.error(request, "Invalid OTP. Please try again.")
            except UserOTP.DoesNotExist:
                print("UserOTP record not found for this user.")
                messages.error(request, "No OTP found for this user. Please request a new OTP.")
        else:
            print("User not found.")
            messages.error(request, "Invalid user.")

        return render(request, 'registration/verify.html', {"remaining_time": remaining_time})

    print("Rendering activation_countdown template with remaining time")  # Debugging: Before rendering the template
    return render(request, "registration/verify.html", {"remaining_time": remaining_time})
