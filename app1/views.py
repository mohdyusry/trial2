from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from .forms import ChatbotForm
from .models import Ticket
from .chatbot import recommend_action  # Ensure this import is correct

User = get_user_model()

# Chatbot View


from django.shortcuts import render, redirect
from .forms import ChatbotForm
from .chatbot import recommend_action, update_model_with_new_data

@login_required
def chatbot_view(request):
    form = ChatbotForm()
    action = None  # To hold the recommended action from the chatbot

    if request.method == 'POST':
        if 'action' in request.POST:
            # User is responding to chatbot recommendation
            resolved = request.POST.get('resolved', None)  # Get 'resolved' checkbox value
            hw_type = request.POST.get('hw_type')
            apps_sw = request.POST.get('apps_sw')
            report_type = request.POST.get('report_type')
            report_desc = request.POST.get('report_desc')
            pc_ip = request.POST.get('pc_ip')
            action = request.POST.get('action')

            if resolved:
                act_stat = 'S' if resolved == 'yes' else 'O'  # Check if resolved is checked
                # Save the Ticket model with the user's response
                Ticket.objects.create(
                    hw_type=hw_type,
                    apps_sw=apps_sw,
                    report_type=report_type,
                    report_desc=report_desc,
                    pc_ip=pc_ip,
                    act_taken=action,
                    act_stat=act_stat,
                    user_name=request.user.username,  # Save the username
                    email=request.user.email,
                    taken_by='chatbot'
                )

                # Update model with new data
                update_model_with_new_data(hw_type, apps_sw, report_type, report_desc, action)

            return redirect('chatbot_view')  # Redirect back to the initial form page or another page as needed

        else:
            # Handle initial form submission
            form = ChatbotForm(request.POST)
            if form.is_valid():
                hw_type = form.cleaned_data['hw_type']
                apps_sw = form.cleaned_data['apps_sw']
                report_type = form.cleaned_data['report_type']
                report_desc = form.cleaned_data['report_desc']
                pc_ip = form.cleaned_data['pc_ip']

                # Call the chatbot recommendation function
                action = recommend_action(hw_type, apps_sw, report_type, report_desc)

                # Render the response page with the chatbot action
                return render(request, 'chatbot_response.html', {
                    'hw_type': hw_type,
                    'apps_sw': apps_sw,
                    'report_type': report_type,
                    'report_desc': report_desc,
                    'pc_ip': pc_ip,
                    'action': action,
                    'form': form,  # Send form to retain previous input data
                })

    # Render the initial form page for GET requests or if no form submission
    return render(request, 'chatbot_form.html', {'form': form})
'''

def chatbot_view(request):
    form = ChatbotForm()
    action = None  # To hold the recommended action from the chatbot
    
    if request.method == 'POST':
        # Check if the form has been submitted with an action or response
        if 'action' in request.POST:
            # User is responding to chatbot recommendation
            resolved = request.POST.get('resolved', None)  # Get 'resolved' checkbox value
            hw_type = request.POST.get('hw_type')
            apps_sw = request.POST.get('apps_sw')
            report_type = request.POST.get('report_type')
            report_desc = request.POST.get('report_desc')
            pc_ip = request.POST.get('pc_ip')
            action = request.POST.get('action')

            print(action)
            print(hw_type)
            if resolved:
                act_stat = 'S' if resolved == 'yes' else 'O'  # Check if resolved is checked
                # Save the Ticket model with the user's response
                Ticket.objects.create(
                    hw_type=hw_type,
                    apps_sw=apps_sw,
                    report_type=report_type,
                    report_desc=report_desc,
                    pc_ip=pc_ip,
                    act_taken=action,
                    act_stat=act_stat,
                    user_name=request.user.username,  # Save the username
                    email=request.user.email,
                    taken_by='chatbot'
                )
            
            return redirect('chatbot_view')  # Redirect back to the initial form page or another page as needed

        else:
            # Handle initial form submission
            form = ChatbotForm(request.POST)
            if form.is_valid():
                hw_type = form.cleaned_data['hw_type']
                apps_sw = form.cleaned_data['apps_sw']
                report_type = form.cleaned_data['report_type']
                report_desc = form.cleaned_data['report_desc']
                pc_ip = form.cleaned_data['pc_ip']
                
                # Call the chatbot recommendation function
                action = recommend_action(hw_type, apps_sw, report_type, report_desc)
                
                # Render the response page with the chatbot action
                return render(request, 'chatbot_response.html', {
                    'hw_type': hw_type,
                    'apps_sw': apps_sw,
                    'report_type': report_type,
                    'report_desc': report_desc,
                    'pc_ip': pc_ip,
                    'action': action,
                    'form': form,  # Send form to retain previous input data
                })
    
    # Render the initial form page for GET requests or if no form submission
    return render(request, 'chatbot_form.html', {'form': form})
    '''

# Signup View


# Login View


# Logout View
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout

# Dashboard View

    
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')  # Redirect to login page upon successful sign-up
    template_name = 'signup.html'  # Make sure this template exists and includes the form fields

    def form_valid(self, form):
        # Save the form data to create a user but don't commit to the database yet
        user = form.save(commit=False)
        # Assign the user's role
        user.is_admin = form.cleaned_data.get('is_admin')
        user.is_technician = form.cleaned_data.get('is_technician')
        user.is_user = form.cleaned_data.get('is_user')
        # Save the user to the database
        user.save()
        return super().form_valid(form)

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Use email for authentication
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                # Redirect based on user role
                if user.is_admin:
                    return redirect('admin_dashboard')  # Ensure these URL names exist in your urls.py
                elif user.is_technician:
                    return redirect('technician_dashboard')
                elif user.is_user:
                    return redirect('user_dashboard')
                else:
                    return redirect('login')  # Fallback in case no role is defined
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def admin_dashboard(request):
    if request.user.is_admin:
        tickets=Ticket.objects.all()
        return render(request, 'admin_dashboard.html',{"tickets":tickets})
    return redirect('login')





# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Ticket

@login_required
def technician_dashboard(request):
    if request.user.is_technician:
        return render(request, 'technician_dashboard.html')
    return redirect('login')

# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Ticket

@login_required
def open_tickets(request):
    if request.user.is_technician:
        tickets = Ticket.objects.filter(act_stat='O')
        return render(request, 'open_tickets.html', {'tickets': tickets})
    return redirect('login')

@login_required
def update_ticket(request, ticket_id):
    if request.user.is_technician and request.method == 'POST':
        ticket = get_object_or_404(Ticket, id=ticket_id)
        action_taken = request.POST.get('action_taken', '').strip()
        if action_taken:
            ticket.act_taken = action_taken
            ticket.act_stat = 'S'
            ticket.taken_by = request.user.username  # Set the technician's username
        else:
            ticket.act_taken = 'Chatbot'
            ticket.act_stat = 'S'
            ticket.taken_by = 'chatbot'
        ticket.save()
        return redirect('open_tickets')
    return redirect('login')

@login_required
def closed_tickets(request):
    if request.user.is_technician:
        # Filter tickets closed by the logged-in technician
        tickets = Ticket.objects.filter(act_stat='S', taken_by=request.user.username)
        return render(request, 'closed_tickets.html', {'tickets': tickets})
    return redirect('login')

# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Ticket

@login_required
def user_dashboard(request):
    if request.user.is_user:
        return render(request, 'user_dashboard.html')
    return redirect('login')

@login_required
def user_tickets(request):
    if request.user.is_user:
        # Filter tickets raised by the logged-in user
        tickets = Ticket.objects.filter(user_name=request.user.username ,email=request.user.email)
        return render(request, 'user_tickets.html', {'tickets': tickets})
    return redirect('login')
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

'''@login_required
def dashboard_view(request):
    if request.user.is_admin:
        return redirect('admin_dashboard')
    #elif request.user.is_technician:
       # return redirect('technician_dashboard')
    elif request.user.is_user:
        return redirect('user_dashboard')
    else:
        return redirect('login')  # Or some default page
'''