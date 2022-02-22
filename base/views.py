from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Message, Topic, Room
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

def loginPage(request):
  page = 'login'
  if request.user.is_authenticated:
    return redirect('/')
  if request.method == 'POST':
    username = request.POST['username'].lower()
    password = request.POST['password']
    try:
      user = User.objects.filter(username=username)      
    except:
      messages.error(request, 'User does not exist')

    user = authenticate(request, username=username, password=password)
    if user:
      login(request, user)
      return redirect('/')
    else:
      messages.error(request, 'Username or Password is incorect')
  context = {'page':page}
  return render(request, 'base/login_register.html', context)

def logoutPage(request):
  logout(request)
  return redirect('/')

def registerUser(request):
  page = 'register'
  form = UserCreationForm()
  
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.username = user.username.lower()
      user.save()
      login(request, user)
      return redirect('/')
    else:
      messages.error(request, 'An error occured')
  context = {'page':page, 'form':form}
  return render(request, 'base/login_register.html', context)

def home(request):
  q = request.GET.get('q') if request.GET.get('q') != None else ''
  rooms = Room.objects.filter(
    Q(topic__name__contains=q) |
    Q(name__contains=q) |
    Q(description__contains=q)
    )
  room_count = rooms.count()
  topics = Topic.objects.all()
  context = {'rooms':rooms, 'topics':topics, 'q':q, 'room_count':room_count}
  return render(request, 'base/home.html', context)
  
# @login_required(login_url='login')
def room(request, pk):
  room = Room.objects.get(id=pk)
  topics = Topic.objects.all()
  room_messages = room.message_set.all().order_by('-created')
  if request.method == 'POST':
    message = Message.objects.create(
      user=request.user,
      room=room,
      body=request.POST['body']
    )
    return redirect('room', pk=room.id)
  context = {'room':room, 'topics':topics, 'room_messages':room_messages}
  return render(request, 'base/room.html', context)

@login_required(login_url='login')
def createRoom(request):
  if request.method  == 'POST':
    form = RoomForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('/')
  form = RoomForm()
  context = {'form':form}
  return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
  room = Room.objects.get(id=pk)
  form = RoomForm(instance=room)
  
  if request.user != room.host:
    return HttpResponse(f'You are not user of "{room.name}"')
  if request.method == 'POST':
    form = RoomForm(request.POST, instance=room)
    if form.save():
      form.save()
      return redirect('/')
  context = {'room':room, 'form':form}
  return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
  room = Room.objects.get(id=pk)
  if request.user != room.host:
    return HttpResponse(f'You are not user of "{room.name}"')

  if request.method == 'POST':
    room.delete()
    return redirect('/')
  context = {'room':room}
  return render(request, 'base/delete_room.html', context)
