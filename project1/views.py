
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Ruangan
from .models import PemesananRuangan
from .forms import RuanganForm
from .forms import PemesananRuanganForm
from django.contrib import messages



def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Check if the user is an admin and redirect accordingly
            if user.is_staff:
                return redirect('admin_home')  # Redirect to admin_home for admin users
            # Check if the user is in the 'approven' group
            elif Group.objects.get(name='approval') in user.groups.all():
                return redirect('approval_home')  # Redirect to 'approval_view' for 'approven' group members
            else:
                return redirect('home')  # Redirect to 'home' for other non-admin users
    return render(request, 'auth/login.html')

@login_required
def index_view(request):
    ruangan_list = Ruangan.objects.filter(Status_Ruangan=False)
    context = {'ruangan_list': ruangan_list}

    if request.user.is_authenticated:
        username = request.user.username
        context['username'] = username

    # Create an empty form instance and pass it to the context
    context['form'] = PemesananRuanganForm()

    return render(request, 'index.html', context)

@login_required
def pesan_ruangan(request):
    print("Reached pesan_ruangan view")
    if request.method == 'POST':
        form = PemesananRuanganForm(request.POST)
        if form.is_valid():
            # Set the username to the logged-in user
            form.instance.username = request.user
            form.save()
            # Redirect to the 'home' view after successful form submission
            print("Form is valid. Redirecting to list_pemesanan")
            return redirect('list_pemesanan')

    # If the form is not valid or the request method is not POST, stay on the same page
    print("Form is not valid. Redirecting to home")
    return redirect('home')

@login_required
def home_admin_view(request):
    ruangan_list = Ruangan.objects.all
    context = {'ruangan_list': ruangan_list}
    
    if request.user.is_authenticated:
        username = request.user.username
        context['username'] = username  # Menambahkan 'username' ke konteks
    
    return render(request, 'admin/home.html', context)    

@login_required
def tambah_ruangan(request):
    if request.method == 'POST':
        form = RuanganForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_home')  # Ganti dengan URL yang sesuai
    else:
        form = RuanganForm()
    return render(request, 'admin/addRuangan.html', {'form': form})

@login_required
def list_pemesanan(request):
    if request.method == 'POST':
        form = PemesananRuanganForm(request.POST)
        if form.is_valid():
            pesanan = form.save(commit=False)
            pesanan.username = request.user
            pesanan.save()
            return redirect('home')  # Ganti dengan rute yang sesuai
    else:
        form = PemesananRuanganForm()
    
    # Mengambil semua data pemesanan
    pesanan_list = PemesananRuangan.objects.filter(username=request.user).order_by('-id')  # Reverse order by 'id'
    
    return render(request, 'user/Pemesanan.html', {'form': form, 'pesanan_list': pesanan_list, 'username': request.user.username})

@login_required
def History(request):
    if request.method == 'POST':
        form = PemesananRuanganForm(request.POST)
        if form.is_valid():
            pesanan = form.save(commit=False)
            pesanan.username = request.user
            pesanan.save()
            return redirect('admin_home')  # Ganti dengan rute yang sesuai
    else:
        form = PemesananRuanganForm()
    
    # Mengambil semua data pemesanan
    pesanan_list = PemesananRuangan.objects.all()  # Remove the filter here
    
    return render(request, 'admin/history.html', {'form': form, 'pesanan_list': pesanan_list, 'username': request.user.username})

@login_required
def update_Status_Ruangan(request, ruangan_id):
    ruangan = get_object_or_404(Ruangan, pk=ruangan_id)
    ruangan.Status_Ruangan = not ruangan.Status_Ruangan  # Toggle the hidden state
    ruangan.save()
    return HttpResponseRedirect(reverse('admin_home'))

@login_required
def edit_ruangan(request, ruangan_id):
    ruangan = get_object_or_404(Ruangan, id=ruangan_id)

    if request.method == 'POST':
        form = RuanganForm(request.POST, request.FILES, instance=ruangan)
        if form.is_valid():
            form.save()
            return redirect('admin_home')  # Redirect to your list view after editing
    else:
        form = RuanganForm(instance=ruangan)

    return render(request, 'admin/edit_ruangan.html', {'form': form, 'ruangan': ruangan})
@login_required
def delete_ruangan(request, ruangan_id):
    ruangan = get_object_or_404(Ruangan, pk=ruangan_id)
    ruangan.delete()
    return redirect('admin_home')

@login_required
def update_alasan(request, pesanan_id):
    pesanan = get_object_or_404(PemesananRuangan, pk=pesanan_id)

    if request.method == 'POST':
        pesanan.alasan = request.POST.get('alasan')
        pesanan.save()
        messages.success(request, 'Alasan updated successfully')
        return redirect('list_pemesanan')

    return render(request, 'user/Pemesanan.html', {'pesanan': pesanan})


@login_required
def user_calendar_view(request):
    events = PemesananRuangan.objects.all()
    return render(request, 'user/user_calendar.html', {'events': events})

@login_required
def admin_calendar_view(request):
    events = PemesananRuangan.objects.all()
    return render(request, 'admin/admin_calendar.html', {'events': events})

@login_required
def approval_calendar_view(request):
    if request.user.username == 'approval':
        events = PemesananRuangan.objects.all()
        return render(request, 'Approval/Approval_calendar.html', {'events': events})

@login_required
def approval_view(request):
    print("Current user:", request.user.username)  # Check the console or log
    if request.user.username == 'approval':
        ruangans = Ruangan.objects.filter(Status_Ruangan=False)
        return render(request, 'Approval/Approval_home.html', {'ruangans': ruangans})

@login_required
def approval_list(request):
    if request.user.username == 'approval':
        if request.method == "POST":
            pesanan_id = request.POST.get("pesanan_id")
            new_status = request.POST.get("new_status")

            # Check if the form was submitted to update status
            if pesanan_id and new_status:
                pesanan = PemesananRuangan.objects.get(id=pesanan_id)
                pesanan.status = new_status
                pesanan.save()

        pesanan_list = PemesananRuangan.objects.all()
        return render(request, 'Approval/Approval_List.html', {'pesanan_list': pesanan_list})
