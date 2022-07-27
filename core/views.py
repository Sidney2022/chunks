from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import CsvChunk

import pandas as pd
import zipfile
import os
from sys import argv
from pathlib import Path



read_buffer_size = 1024
chunk_size = 1024 * 100000

def _chunk_file(file, extension):
    print('files')
    current_chunk_size = 0
    current_chunk = 1
    done_reading = False
    while not done_reading:
        with open(f'files/{current_chunk}{extension}.chk', 'ab') as chunk:
            while True:
                bfr = file.read(read_buffer_size)
                if not bfr:
                    done_reading = True
                    break

                chunk.write(bfr)
                current_chunk_size += len(bfr)
                if current_chunk_size + read_buffer_size > chunk_size:
                    current_chunk += 1
                    current_chunk_size = 0
                    break


def _join():
    p = Path.cwd()

    chunks = list(p.rglob('*.chk'))
    chunks.sort()
    extension = chunks[0].suffixes[0]

    with open(f'join{extension}', 'ab') as file:
        for chunk in chunks:   
            with open(chunk, 'rb') as piece:
                while True:
                    bfr = piece.read(read_buffer_size)
                    if not bfr:
                        break

                    file.write(bfr)


def _split(upload_file):
    print('split')
    # p = Path('files')
    # file_to_split = None
    # for f in p.iterdir():
    #     if f.is_file() and f.name != '.':
    #         file_to_split = f
    #         break
    
    file_to_split = upload_file
    # if file_to_split:
    with open(file_to_split, 'rb') as file:
        _chunk_file(file, file_to_split)



@login_required(login_url='/signin')
def index(request):
    if request.method == "POST":
        chunk_size = request.POST['chunk_no']
        file = request.FILES.get('doc')
        user = request.user
        batch_no = 1
        
        if  chunk_size == '' or file == None:
            messages.info(request, 'fields cannot be blank!')
            return redirect('/')
<<<<<<< HEAD
        batch_no = 1
      
        csv = CsvChunk.objects.create(user=user, file=file)
        csv.save()    
        megabyte_size = int (chunk_size)  #50mb
        CHUNK_SIZE = megabyte_size * 1000 * 1024
        file_number = 1
        for doc in os.listdir('media/files'):
            if doc == file.name :
                with open(f'media/files/{doc}') as f:
                    chunk = f.read(CHUNK_SIZE)
                    while chunk:
                        with open('files/csv_file-' + str(file_number) +'.csv',  'w') as chunk_file:
                            chunk_file.write(chunk)
                        file_number += 1
                        chunk = f.read(CHUNK_SIZE)
                os.remove(f'media/files/{doc}')
        csv.delete()
        with zipfile.ZipFile(f'chunked_files/{user}/{file.name}.zip', 'w') as zipF:
            for nfile in os.listdir('files'):
                zipF.write(f'files/{nfile}', compress_type=zipfile.ZIP_DEFLATED)
                
        for ofile in os.listdir('files'):
            os.remove(f'files/{ofile}')
              
        messages.info(request, 'file has been received successfully')
=======
        
        
        try:
            user_folder = str(user)
            os.mkdir(f'chunked_files/{user_folder}')
        except FileExistsError:
            pass
        
        
        for chunk in pd.read_csv(file, chunksize=int(chunk_size)):
            new_file = "csv_split" + str(batch_no) + ".csv"
            chunk.to_csv(f'files/{new_file}', index=False)
            batch_no += 1
            
        with zipfile.ZipFile(f'chunked_files/{user}/{user}-{file}.zip', 'w') as zipF:
            for file in os.listdir(f'files'):
                zipF.write(f'files/{file}', compress_type=zipfile.ZIP_DEFLATED)



        for file in os.listdir('files'):
            os.remove((f'files/{file}'))        
        messages.info(request, 'file has been split successfully')
>>>>>>> 12c351b0aa82a5d230f2a7ce272663fb7cc3ca57
        return redirect('/')
        
    else:
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

