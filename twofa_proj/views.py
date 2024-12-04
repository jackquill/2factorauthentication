from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login  
from django.contrib.auth.decorators import login_required
from users.models import CustomUser
from codes.forms import VerificationCodeForm
from codes.utils import send_verification_email
import re 

@login_required #only logged-in users can access this view 
def home_view(request):
    return render(request, 'main.html', {})

    # sanitize the user input to prevent any malicious characters
def sanitize_input(input_string):
    # Remove potentially harmful characters 
    sanitized_input = re.sub(r'[;&|`]', '', input_string)  # Removes characters commonly used in injection
    return sanitized_input

def login_view(request):
    login_form = AuthenticationForm() #django form for validating users, securly haskes passwords with a salt
    #print(login_form) 
    if request.method == "POST":
        entered_username = request.POST.get('username') #get entered username and password
        entered_password = request.POST.get('password')

        #sanitized inputs
        entered_username = sanitize_input(entered_username)
        entered_password = sanitize_input(entered_password)

        authenticated_user = authenticate(request, username=entered_username, password=entered_password) #check if password is correct
        #print(authenticated_user) debugging
        if authenticated_user  is not None: # if authenticated then authenticated_user becomes the users username
            request.session['pk'] = authenticated_user.pk # get users primary key
            return redirect('verify-view')
        else:
            # return with an error message if wrong crediantials
            return render(request, 'login.html', {'form': login_form, 'error': 'Invalid Username or Password'})
    # heres for if it is a GET 
    return render(request, 'login.html', {'form': login_form})



def verify_view(request):
    verification_form = VerificationCodeForm(request.POST or None) #form from codes 
    pk = request.session.get('pk') #check that they got past the first step and get there primary key
    if pk:
        authenticated_user = CustomUser.objects.get(pk=pk) # 

        code = authenticated_user.code  # Get the code generated for the user
        # code.save()
        user_and_code = f"{authenticated_user.username}: {authenticated_user.code}" # example in form jq: 60927
        
       # print(user_and_code)  # Print the code for debugging 
        send_verification_email(authenticated_user)


        if request.method == "POST": #if user sumbitted a form and it is valid
            if verification_form.is_valid():
                user_entered_number = verification_form.cleaned_data.get('number') # retrieve user entered code 
                if str(code.number) == user_entered_number:  # now compare the input with the code
                    code.save()
                    login(request, authenticated_user)  # log in the user 
                    return redirect('home-view')
                else:
                    return redirect('login-view')  

    return render(request, 'verify.html', {'form': verification_form})  