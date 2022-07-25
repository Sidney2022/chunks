from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import CsvChunk

import pandas as pd
import zipfile
import os


@login_required(login_url='/signin')
def index(request):
    if request.method == "POST":
        chunk_size = request.POST['chunk_no']
        file = request.FILES.get('doc')
        user = request.user
        
        if  chunk_size == '' or file == None:
            messages.info(request, 'fields cannot be blank!')
            return redirect('/')
        batch_no = 1
        
        try:
            user_folder = str(user)
            os.mkdir(f'chunked_files/{user_folder}')
        except FileExistsError:
            pass
        
        for chunk in pd.read_csv(file, chunksize=int(chunk_size)):
            new_file = "csv_split" + str(batch_no) + ".csv"
            chunk.to_csv(f'/tmp/files/{new_file}', index=False)
            batch_no += 1
            
        with zipfile.ZipFile(f'/tmp/chunked_files/{user}/{user}-{file}.zip', 'w') as zipF:
            for file in os.listdir(f'files'):
                zipF.write(f'files/{file}', compress_type=zipfile.ZIP_DEFLATED)



        for file in os.listdir('files'):
            os.remove((f'files/{file}'))        
        messages.info(request, 'file has been split successfully')
        return redirect('/')
        
    else:
        print(os.getcwd())
        return render(request, 'index.html')


@login_required(login_url='/signin')
def saved_chunks(request):
    user = request.user
    files = []
    for file in os.listdir(f'chunked_files/{user}'):
        files.append(file)
        print(file)
    return render(request, 'saved.html',{'files':files})



def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'invalid login credentials')
            return redirect('/signin')
    
    return render(request, 'login.html')



def signup(request):
       if request.method == "POST":
              first_name = request.POST['first_name']
              last_name = request.POST['last_name']
              username = request.POST['username']
              email = request.POST['email']
              password = request.POST['password']
              password2 = request.POST['password2']
              if password != password2:
                     messages.info(request, 'passwords do not match')
                     return redirect('/signup')
              elif len(password) < 4:
                     messages.info(request, 'password is too short')
                     return redirect('/signup')
              elif User.objects.filter(username=username).exists():
                     messages.info(request, 'username taken')
                     return redirect('/signup')
              elif User.objects.filter(email=email).exists():
                     messages.info(request, 'email already in use. if this is your account, please login')
                     return redirect('/signup')
              else:
                     new_user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
                     new_user.save()
                     os.mkdir(f'chunked_files/{username}')
                     return redirect('/signin')              
       else:
              return render(request, 'register.html')
          

@login_required(login_url='/signin')
def logout(request):
       auth.logout(request)
       return redirect('/signin')
