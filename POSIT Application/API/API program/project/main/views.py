# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.utils.encoding import smart_str
from wsgiref.util import FileWrapper
from shutil import make_archive
import mimetypes
from rename import Renamefiles
from sentistrenght import Sentistrenght
from wordfrequency import Wordfrequency
from posit import Runposit
import shutil
from time import gmtime, strftime
# import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import uuid
import zipfile # this is to work on content of zipped file
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='/admin')
def index(request):
    uploaded = True
    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'posit')):
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'posit'))
    file_name_list =  os.listdir( os.path.join(settings.MEDIA_ROOT, 'posit'))
    if (len(file_name_list) == 0 ):
        uploaded = False
    return render(request, "main/index.html", {"home": '', 'uploaded_file_url': file_name_list, 'uploaded': uploaded})


def api_doc(request):
    return render(request, "main/api_doc.html" , {})


@csrf_exempt
def api_posit(request):
    json_response = dict()
    input_files = dict()
    if request.method == 'POST' and request.FILES['files']:
        date_time_foldername = strftime("%Y%m%d%H%M%S", gmtime()) + "-" + str(uuid.uuid4())[:4]
        json_response["result_name"] = date_time_foldername
        directory = os.path.join(settings.MEDIA_ROOT, date_time_foldername)
        if not os.path.exists(directory):
            os.makedirs(directory)
            # copy folder content to the directory
            if request.method == 'POST' and request.FILES['files']:
                file_name_list = []
                files = request.FILES.getlist('files')
                fs = FileSystemStorage(location = directory)
                for f in files:
                    filename = fs.save(f.name, f)
                    # uploaded_file_url = fs.url(filename)
                    file_name_list.append(filename)
                input_files["files"] = file_name_list
        else:
            return HttpResponse("directory Already Exist")
        return_txt = run_posit_function(directory)
        if return_txt != "done":
            return render(request, "main/index.html", {"home" : return_txt })
        zip_and_download(date_time_foldername + "-output")

        input_files["Total_input"] = len(input_files["files"])
        json_response["input"] = input_files
        json_response["result_url"] =  request.META['HTTP_HOST'] + "/result/" + date_time_foldername
        json_response["date_time"] =  strftime("%Y-%m-%d %H-%M-%S", gmtime())
        json_response["ip_address"] = get_client_ip(request)
        return JsonResponse(json_response)
    else:
        json_response["error"] = {"message":"Not A POST Request or No File Attached", "code": 504 }
        return JsonResponse(json_response)



@csrf_exempt
def api_posit_zipped(request):
    json_response = dict()
    input_files = dict()
    if request.method != 'POST':
        return JsonResponse({"error": {"message":"Not A POST Request or No File Attached", "code": 504}})

    if 'input_file' not in request.FILES:
        return JsonResponse({"error": {"message":"No input_file key specified", "code": 400}})

    if not(zipfile.is_zipfile(request.FILES['input_file'])):
        return JsonResponse({"error": {"message":"Invalid input file format, file must be zip format", "code": 406}})

    if request.method == 'POST' and request.FILES['input_file']:
        date_time_foldername = strftime("%Y%m%d%H%M%S", gmtime()) + "-" + str(uuid.uuid4())[:4]
        json_response["result_name"] = date_time_foldername
        directory = os.path.join(settings.MEDIA_ROOT, date_time_foldername)
        if not os.path.exists(directory):
            os.makedirs(directory)
            # copy folder content to the directory
            if request.method == 'POST' and request.FILES['input_file']:
                zfiles = zipfile.ZipFile(request.FILES['input_file'])
                zfiles.extractall(directory)
                input_files["files"] = zfiles.namelist()
                zfiles.close()
        else:
            return JsonResponse({"error": {"message":"Directory Already Exist", "code": 429}})
        return_txt = run_posit_function(directory)
        if return_txt != "done":
            return render(request, "main/index.html", {"home" : return_txt })
        zip_and_download(date_time_foldername + "-output")

        input_files["Total_input"] = len(input_files["files"])
        json_response["input"] = input_files
        json_response["result_url"] =  request.META['HTTP_HOST'] + "/result/" + date_time_foldername
        json_response["date_time"] =  strftime("%Y-%m-%d %H-%M-%S", gmtime())
        json_response["ip_address"] = get_client_ip(request)
        return JsonResponse(json_response)
    else:
        json_response["error"] = {"message":"Not A POST Request or No File Attached", "code": 504 }
        return JsonResponse(json_response)

@csrf_exempt
def api_result(request, filename):
    try:
        zipped_output = os.path.join(settings.MEDIA_ROOT, filename + "-output.zip")
        file_wrapper = FileWrapper(file(zipped_output,'rb'))
    except:
        return JsonResponse({"error": {"message":"The specified result could not be found.", "code": 404}})
    file_mimetype = mimetypes.guess_type(zipped_output)
    response = HttpResponse(file_wrapper, content_type=file_mimetype )
    response['X-Sendfile'] = zipped_output
    response['Content-Length'] = os.stat(zipped_output).st_size
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(zipped_output)
    return response

def delete_all_uploads(request):
    run_delete_all()
    return render(request, "main/index.html", {"home": 'All files deleted successfully' })


def get_file(request):
    if request.method == 'POST' and request.FILES['myfile']:
        file_name_list = []
        files = request.FILES.getlist('myfile')
        if not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'posit')):
            os.makedirs(os.path.join(settings.MEDIA_ROOT, 'posit'))
        fs = FileSystemStorage(location= os.path.join(settings.MEDIA_ROOT, 'posit'))
        for f in files:
            filename = fs.save(f.name, f)
            uploaded_file_url = fs.url(filename)
            file_name_list.append(uploaded_file_url)
        return redirect('/')
    return render(request, "main/index.html",{"home": "Not uploaded"})

def run_rename_request(request):
    return_txt = run_rename()
    if return_txt != "done":
        return render(request, "main/index.html",{"home": "Something Went Wrong"})
    response =  zip_and_download("posit")
    return response

def run_posit(request):
    return_txt = run_posit_function("posit")
    if return_txt != "done":
        return render(request, "main/index.html",{"home": return_txt})
    response = zip_and_download("posit-output")
    # delete all files and folders
    run_delete_all()
    # return redirect('/intermiediatepage/posit')
    return response

def run_posit_intermiediatepage(request, filename):
    download_link = "/download/"+ filename
    return render(request, "main/index.html",{"download_link": download_link})

def download_result(request, filename):
    try:
        zipped_output = os.path.join(settings.MEDIA_ROOT, filename + "-output.zip")
        file_wrapper = FileWrapper(file(zipped_output,'rb'))
    except:
        return JsonResponse({"error": {"message":"The specified result could not be found.", "code": 404}})
    file_mimetype = mimetypes.guess_type(zipped_output)
    response = HttpResponse(file_wrapper, content_type=file_mimetype )
    response['X-Sendfile'] = zipped_output
    response['Content-Length'] = os.stat(zipped_output).st_size
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(zipped_output)
    run_delete_all()
    return response

def run_wordfrequency_request(request):
    return_txt = run_wordfrequency()
    if return_txt != "done":
        return render(request, "main/index.html",{"home": "Something Went Wrong"})
    response =  download("frequency_positive.txt")
    return response


def run_sentistrength_request(request):
    return_txt = run_sentistrenght()
    if return_txt != "done":
        return render(request, "main/index.html",{"home": "Something Went Wrong"})
    response =  zip_and_download("output")
    return response


####################################################################################
############ Genertics Functions Here ##############################################
####################################################################################



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def run_delete_all():
    # delete all inputs
    folder_location = os.path.join(settings.MEDIA_ROOT, 'posit')
    file_name_list =  os.listdir(folder_location )
    for f in file_name_list:
        file_path = os.path.join(folder_location, f)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)
    folder_location_2 = os.path.join(settings.MEDIA_ROOT, 'output')
    file_name_list_2 =  os.listdir(folder_location_2 )
    for f2 in file_name_list_2:
        file_path2 = os.path.join(folder_location_2, f2)
        try:
            if os.path.isfile(file_path2):
                os.remove(file_path2)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)
    folder_location_3 = os.path.join(settings.MEDIA_ROOT, 'posit-output')
    file_name_list_3 =  os.listdir(folder_location_3 )
    for f3 in file_name_list_3:
        file_path3 = os.path.join(folder_location_3, f3)
        try:
            if os.path.isfile(file_path3):
                os.remove(file_path3)
            elif os.path.isdir(file_path3):
                shutil.rmtree(file_path3)
        except Exception as e:
            print(e)

    zipped_output = os.path.join(settings.MEDIA_ROOT, 'output.zip')
    zipped_input = os.path.join(settings.MEDIA_ROOT, 'posit.zip')
    zipped_iccrcoutput = os.path.join(settings.MEDIA_ROOT, 'posit-output')
    if os.path.isfile(zipped_output):
        os.remove(zipped_output)
    if os.path.isfile(zipped_input):
        os.remove(zipped_input)
    if os.path.isfile(zipped_iccrcoutput):
        os.remove(zipped_iccrcoutput)



def run_rename():
    file_path = settings.MEDIA_ROOT
    input = os.path.join(file_path, 'posit')
    Renamefiles.run(input)
    return "done"


def run_sentistrenght():
    file_path = settings.MEDIA_ROOT
    input = os.path.join(file_path, 'posit')
    output = os.path.join(file_path, 'output/')
    Sentistrenght.run_analysis(input, output)
    return "done"

def run_wordfrequency():
    file_path = settings.MEDIA_ROOT
    input = os.path.join(file_path, 'posit')
    output = os.path.join(file_path, 'output')
    output_file = os.path.join(output, 'frequency_positive.txt' ) # the output in this case is a text file and not a directory
    Wordfrequency.run(input, output_file)
    return "done"

def run_posit_function(folder_name):
    file_path = settings.MEDIA_ROOT
    input = os.path.join(file_path, folder_name)
    Runposit.run_posit(input)
    return "done"

# download function, pass path of file to download
def download(file_name):
    output_folder = os.path.join(settings.MEDIA_ROOT, "output")
    file_path = os.path.join(output_folder, file_name)
    file_wrapper = FileWrapper(file(file_path,'rb'))
    file_mimetype = mimetypes.guess_type(file_path)
    response = HttpResponse(file_wrapper, content_type=file_mimetype )
    response['X-Sendfile'] = file_path
    response['Content-Length'] = os.stat(file_path).st_size
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
    return response

# function to zip the whole output folder
def zip_and_download(folder_name):
    """
    A python function to zip files in directory and send it as downloadable response to the browser.
    Args:
      @request: Django request object
      @file_name: Name of the directory to be zipped
    Returns:
      A downloadable Http response
    """
    folder_path = os.path.join(settings.MEDIA_ROOT, folder_name)

    path_to_zip = make_archive(folder_path, "zip", folder_path)
    response = HttpResponse(FileWrapper(file(path_to_zip, 'rb')), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename='+folder_name.replace(" ","_")+'.zip'
    return response
