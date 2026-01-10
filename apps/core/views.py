# from django.shortcuts import render
# from django.shortcuts import redirect

# # Create your views here.

# def home_view(request):
#     if request.user.is_authenticated:
#         return redirect('dashboard')
#     return render(request, 'home.html')


from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.

def home_view(request):
    # Show home page for all users, authenticated or not
    return render(request, 'home.html')
