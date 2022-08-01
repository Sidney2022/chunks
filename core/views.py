
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import CsvChunk

from io import BytesIO
import pandas as pd
import zipfile
from zipfile import ZIP_DEFLATED, ZipFile

import os
from pathlib import Path



@login_required(login_url='/signin')
def index(request):
    if request.method == "POST":
        file = request.FILES.get('doc')
        ouput_name = request.POST['file_name']
        chunk_size = request.POST['chunk_no']
        user = request.user
        if chunk_size == '' or file == None:
            messages.error(request, 'fields cannot be blank!')
            return redirect('/')
        
        if  file.name.endswith('csv')  :
            if ouput_name == '':
                ouput_name = file.name

            try:
                os.mkdir('media')
            except FileExistsError:
                pass
            
            chunk_size = int(chunk_size)
            batch_no = 1
            f_name = f'{user}_{ouput_name}-.zip'
            for chunk in pd.read_csv(file, chunksize=chunk_size):
                with ZipFile(f'media/{f_name}', 'a') as zip_file:
                    file_name = f"{ouput_name}-" + str(batch_no) + ".csv"
                    zip_file.write(file_name,chunk.to_csv(file_name, index=False) ,compress_type=zipfile.ZIP_DEFLATED)
                os.remove(file_name)
                batch_no += 1
                
            csv_obj = CsvChunk.objects.create(user=user, file= f_name)
            csv_obj.save()
            file = CsvChunk.objects.get(user=user,file=f_name)
            file_id = file.file_id
            
            print(f'file id is {file_id}')
            messages.info(request, 'file hs been split successfully')
            return redirect(f'/new_chunk/{file_id}')
        
        messages.error(request, 'invalid file format')
        return redirect('/')
    
    return render(request, 'index.html')


@login_required(login_url='/signin')
def saved_chunks(request):
    user = request.user
    files = CsvChunk.objects.filter(user=user)
    
    return render(request, 'saved.html',{'files':files})


@login_required(login_url='/signin')
def new_chunk(request, pk):
    print(f'request method is {request.method}')
    user=request.user #logged in user
    file = CsvChunk.objects.filter(user=user, file_id=pk)
    if file.exists():
        file = CsvChunk.objects.get(user=user, file_id=pk) 
        return render(request, 'new.html', {'file':file})
    messages.error(request, 'file not found')
    return render(request, 'new.html')

    

@login_required(login_url='/signin')
def save(request):
    file_id = request.GET.get('file_id')
    user=request.user
    csv_object = CsvChunk.objects.get(user=user, file_id=file_id)
    print(csv_object)
    messages.info(request, 'file has been saved successfully')
    return redirect('/saved_chunks')


def file_delete(request):
    user=request.user
    file_id = request.GET.get('id')
    file = CsvChunk.objects.get(user=user, file_id=file_id)
    file.delete()
    os.remove(f'media/{file.file}')
    messages.info(request, f'your file "{file.file}" has been deleted ')
    return redirect('/saved_chunks')
    
    

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/saved_chunks')
        else:
            messages.info(request, 'invalid login credentials')
            return redirect('/signin')
    
    return render(request, 'login.html')


def signup(request):
       if request.method == "POST":
            #   first_name = request.POST['first_name']
            #   last_name = request.POST['last_name']
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
                     new_user = User.objects.create_user(username=username, email=email, password=password)
                     new_user.save()
                     user = auth.authenticate(username=username, password=password)
                     auth.login(request, user)
                     return redirect('/')              
       else:
              return render(request, 'register.html')
          

@login_required(login_url='/signin')
def logout(request):
       auth.logout(request)
       return redirect('/signin')

# /git clone https://github.com/sibtc/simple-file-upload.git 
# from https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html

#how to download files from django media folders