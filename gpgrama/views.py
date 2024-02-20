from django.db.models import fields
from django.db.models import query
from django.db.models.query import QuerySet
from django.http.response import HttpResponse
from django.shortcuts import render,redirect

from .filters import CandidateFilter, CandidatePipelineFilter
from .models import HiringManager, HR, Candidate, Admin, CandidateFile
from .forms import HiringManagerCreate, HrCreate, CandidateCreate, AdminCreate

from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, logout, login as auth_login,update_session_auth_hash

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import os
import pyrebase
import pprint
pp = pprint.PrettyPrinter(indent=4)

from datetime import date

firebaseConfig = {
    "apiKey": "AIzaSyD78UNg9V-ga5jRJPVI9_pyxEBY_A6q-Vo",
    "authDomain": "gpgrama-hiringplatform.firebaseapp.com",
    "databaseURL": "https://gpgrama-hiringplatform-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "gpgrama-hiringplatform",
    "storageBucket": "gpgrama-hiringplatform.appspot.com",
    "messagingSenderId": "199232017935",
    "appId": "1:199232017935:web:f3a9abb950a63cbc51357a",
    "measurementId": "G-MQZX5C2RRX",
    "serviceAccount":"static/service-provider.json"
}

firebase = pyrebase.initialize_app(firebaseConfig)
storage=firebase.storage()
#token = firebase.auth.create_custom_token("admin")

def handle_uploaded_file(f, usr_id):
    #return the url to the image
    # filename = f.name
    # backup_file = f
    # with open('temp.pdf', 'wb+') as destination:
    #     for chunk in backup_file.chunks():
    #         destination.write(chunk)

    # path = "docs/candidate/"+str(usr_id)+"/"+filename
    # #print(f)
    # storage.child(path).put("temp.pdf")
    # os.remove("temp.pdf")
    file_obj = CandidateFile()
    file_obj.name = f.name
    file_obj.pdf = f
    file_obj.user_ref = usr_id
    file_obj.owner = Candidate.objects.get(uuid=usr_id)
    file_obj.save()

    return

@login_required(login_url='login')
def get_file_list(uid):
    path = "docs/candidates/"+str(uid)
    file_list = []
    ref = storage.child(path)
    all_files = ref.list_files()
    #print(path)
    for file in all_files:
        if path in file.name:
            file_list.append(file.name)
    return file_list

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                usr_obj = HR.objects.get(email=username)
            except HR.DoesNotExist:
                try:
                    usr_obj = HiringManager.objects.get(email=username)
                except  HiringManager.DoesNotExist:
                    try:
                        usr_obj = Admin.objects.get(email=username)
                    except  Admin.DoesNotExist:
                        usr_obj = None
            
            # if HR.objects.get(name=username).exists():
            #     usr_obj = HR.objects.get(name=username)
            # elif HiringManager.objects.get(name=username).exists():
            #     usr_obj = HiringManager.objects.get(name=username)
            # else:
            #     usr_obj = Admin.objects.get(name=username)
            if usr_obj is not None:
                request.session['name'] = usr_obj.name
                request.session['type'] = usr_obj.type
                request.session['id'] = usr_obj.id
                request.session['url'] = usr_obj.image.url

            auth_login(request, user)
            return redirect('pipeline') #inserir qual a página inicial, de acordo com o cargo do utilizador
        else:
            messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'login.html', context)

@login_required(login_url='login')
def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
def homeTest(request):
    context = {}
    return render(request, 'homeTest.html', context)

@login_required(login_url='login')
def create_Hr(request):

    # hr logged
    if(request.session['type']==1):
        return redirect('/gpgrama/hr/' + str(request.session['id']))

    # hm logged
    if(request.session['type']==2):
        return redirect('/gpgrama/hm/' + str(request.session['id']))

    form = HrCreate()
    if request.method =='POST':
        uploaded_hr = HrCreate(request.POST, request.FILES)
        if uploaded_hr.is_valid():
            new_hr = uploaded_hr.save(commit=False)

            canCreate = True
            for user in User.objects.all():
                if(new_hr.name==user.username):
                    messages.info(request, 'Username already exists')
                    canCreate = False
                if(new_hr.email==user.email):
                    messages.info(request, 'Email already exists')
                    canCreate = False
            
            if(canCreate):
                user = User.objects.create_user(new_hr.email, new_hr.email, new_hr.password)
                user.save()
                new_hr.user = user
                new_id = new_hr.uuid
                new_hr.image.name = str(new_id)+".jpg"
                new_hr.save()
                return redirect('list_hr')
        else:
            messages.info(request, 'A user HR with that name/e-mail already exists')
            #return HttpResponse("""the form is wrong""")
    #with this type of form, in frontend just need to print  {% for field in form %} to get all parameters of needed
    return render(request,'hrform.html', {'form':form})

@login_required(login_url='login')
def create_HiringManager(request):

    # hr logged
    if(request.session['type']==1):
        return redirect('/gpgrama/hr/' + str(request.session['id']))

    # hm logged
    if(request.session['type']==2):
        return redirect('/gpgrama/hm/' + str(request.session['id']))

    form = HiringManagerCreate()
    if request.method =='POST':
        uploaded_hm= HiringManagerCreate(request.POST, request.FILES)
        if uploaded_hm.is_valid(): #and uploaded_user_form.is_valid():
            new_hm = uploaded_hm.save(commit=False)

            canCreate = True
            for user in User.objects.all():
                if(new_hm.name==user.username):
                    messages.info(request, 'Username already exists')
                    canCreate = False
                if(new_hm.email==user.email):
                    messages.info(request, 'Email already exists')
                    canCreate = False
            
            if(canCreate):
                user = User.objects.create_user(new_hm.email, new_hm.email, new_hm.password)
                user.save()
                new_hm.user = user
                new_id = new_hm.uuid
                new_hm.image.name = str(new_id)+".jpg"
                new_hm.save()

                return redirect('/gpgrama/hm/'+str(new_hm.id))
        else:
            messages.info(request, 'A user HM with that name/e-mail already exists')
            #return HttpResponse("""the form is wrong""")
    #with this type of form, in frontend just need to print  {% for field in form %} to get all parameters of needed
    return render(request,'hmform.html', {'form':form})


@login_required(login_url='login')
def hr(request,hr_id):

    # hm logged
    if(request.session['type']==2):
        return redirect('/gpgrama/hm/' + str(request.session['id']))

    # hr logged, but it is not his own profile
    if(request.session['type']==1):
        if(str(hr_id)!=str(request.session['id'])):
            return redirect('/gpgrama/hr/' + str(request.session['id']))


    if request.method == 'GET':
        hr_id=int(hr_id)
        try:
            hr_perfil=HR.objects.get(id=hr_id)
            hr_candidates = hr_perfil.responsibleHR.all()
        except HR.DoesNotExist:
            return HttpResponse("""Hr does not exist""")

    elif request.method == 'POST':
        if request.POST.get("hr_id"):
            hr_id=request.POST.get("hr_id")
            return redirect("/gpgrama/update_Hr/"+str(hr_id))

        elif request.POST.get("candidate_id"):
            candidate_id=request.POST.get("candidate_id")
            return redirect("/gpgrama/candidate/"+str(candidate_id))
        else:
            return HttpResponse("""Operation not valid""")
    

    return render(request,'hr_profile.html', {'hr_perfil':hr_perfil,'hr_candidates':hr_candidates})


@login_required(login_url='login')
def hm(request,hm_id):

    # hm logged, but it is not his own profile
    if(request.session['type']==2):
        if(str(hm_id)!=str(request.session['id'])):
            return redirect('/gpgrama/hm/' + str(request.session['id']))


    if request.method == 'GET':
        hm_id=int(hm_id)
        try:
            hm_perfil=HiringManager.objects.get(id=hm_id)
            candidates=Candidate.objects.filter(HiringManager=hm_perfil)
        except HiringManager.DoesNotExist:
            return HttpResponse("""HiringManager does not exist""")

    elif request.method == 'POST':
        if request.POST.get("hm_id"):
            hm_id=request.POST.get("hm_id")
            return redirect("/gpgrama/update_HiringManager/"+str(hm_id))

        elif request.POST.get("candidate_id"):
            candidate_id=request.POST.get("candidate_id")
            return redirect("/gpgrama/candidate/"+str(candidate_id))
        else:
            return HttpResponse("""Operation not valid""")

    return render(request,'hm.html', {'hm_perfil':hm_perfil,'id':str(hm_id),'candidates':candidates})

@login_required(login_url='login')
def update_Hr(request,hr_id):

    # hm logged
    if(request.session['type']==2):
        return redirect('/gpgrama/update_HiringManager/' + str(request.session['id']))
        
    # hr logged, but it is not his own profile
    if(request.session['type']==1):
        if(str(hr_id)!=str(request.session['id'])):
            return redirect('/gpgrama/update_Hr/' + str(request.session['id']))

    hr_id=int(hr_id)
    try:
        Hr=HR.objects.get(id=hr_id)
    except HR.DoesNotExist:
         return HttpResponse("""Hr does not exist""")

    if request.method =='POST':
        if(request.POST.get("delete_hr")): 
            try:
                hr_perfil=HR.objects.get(id=hr_id)
            except HR.DoesNotExist:
                return HttpResponse("""HR does not exist""")

            hr_perfil.user.delete()
            hr_perfil.delete()


            return redirect("/gpgrama/list_hr")

        if(request.POST.get("update_hr")): 
            updated_hr=HrCreate(request.POST, request.FILES, instance=Hr)

            if updated_hr.is_valid():
                user = User.objects.get(username=updated_hr.instance.email)
                user.set_password(updated_hr.instance.password)
                user.save()
                update_session_auth_hash(request,user)
                if "images/hr" in updated_hr.instance.image.name:
                    updated_hr.save()
                else:
                    teste=updated_hr.save(commit=False)
                    new_id = teste.uuid
                    teste.image.name = str(new_id)+".jpg"
                    teste.user.username = teste.name
                    teste.user.email = teste.email
                    teste.user.set_password(teste.password)
                    #teste.user.save()
                    teste.save()
                return redirect("/gpgrama/hr/"+str(hr_id))

    hr_form=HrCreate(instance=Hr)
    #with this type of form, in frontend just need to print  {% for field in form %} to get all parameters of needed
    return render(request,'hredit.html', {'form':hr_form,'hr_perfil':Hr})

@login_required(login_url='login')
def update_HiringManager(request,hm_id):

    # hm logged, but it is not his own profile
    if(request.session['type']==2):
        if(str(hm_id)!=str(request.session['id'])):
            return redirect('/gpgrama/update_HiringManager/' + str(request.session['id']))
    

    hm_id=int(hm_id)
    try:
        hm=HiringManager.objects.get(id=hm_id)
    except HiringManager.DoesNotExist:
         return HttpResponse("""HiringManager does not exist""")

    if request.method =='POST':
        if(request.POST.get("delete_hm")):
            try:
                hm_perfil=HiringManager.objects.get(id=hm_id)
            except HiringManager.DoesNotExist:
                return HttpResponse("""HiringManager does not exist""")

            hm_perfil.user.delete()
            hm_perfil.delete()


            return redirect("/gpgrama/list_hm")

        if(request.POST.get("update_hm")): 
            updated_hm=HiringManagerCreate(request.POST, request.FILES, instance=hm)
            if updated_hm.is_valid():
                user = User.objects.get(username=updated_hm.instance.email)
                user.set_password(updated_hm.instance.password)
                user.save()
                update_session_auth_hash(request,user)
                if "images/hm" in updated_hm.instance.image.name:
                    updated_hm.save()
                else:
                    teste = updated_hm.save(commit=False)
                    new_id = teste.uuid
                    teste.image.name = str(new_id)+".jpg"
                    teste.user.username = teste.name
                    teste.user.email = teste.email
                    teste.user.set_password(teste.password)
                    #teste.user.save()
                    teste.save()
                return redirect("/gpgrama/hm/"+str(hm_id))

    hm_form=HiringManagerCreate(instance=hm)
    #with this type of form, in frontend just need to print  {% for field in form %} to get all parameters of needed
    return render(request,'hmedit.html', {'form':hm_form,'hm_perfil':hm})


@login_required(login_url='login')
def delete_HiringManager(request,hm_id):

    # hr logged
    if(request.session['type']==1):
        return redirect('/gpgrama/hr/' + str(request.session['id']))

    # hm logged
    if(request.session['type']==2):
        return redirect('/gpgrama/hm/' + str(request.session['id']))

    hm_id=int(hm_id)
    try:
        hm_perfil=HiringManager.objects.get(id=hm_id)
    except HiringManager.DoesNotExist:
         return HttpResponse("""HiringManager does not exist""")

    hm_perfil.delete()
    return redirect('list_hm')


@login_required(login_url='login')
def delete_Hr(request,hr_id):

     # hr logged
    if(request.session['type']==1):
        return redirect('/gpgrama/hr/' + str(request.session['id']))

    # hm logged
    if(request.session['type']==2):
        return redirect('/gpgrama/hm/' + str(request.session['id']))

    hr_id=int(hr_id)
    try:
        hr_perfil=HR.objects.get(id=hr_id)
    except HR.DoesNotExist:
         return HttpResponse("""Hr does not exist""")

    hr_perfil.delete()
    return redirect('list_hr')


@login_required(login_url='login')
def admin_profile(request):

    # hr logged
    if(request.session['type']==1):
        return redirect('/gpgrama/hr/' + str(request.session['id']))

    # hm logged
    if(request.session['type']==2):
        return redirect('/gpgrama/hm/' + str(request.session['id']))
    
    try:
        admin = Admin.objects.first()
    except Admin.DoesNotExist:
         return HttpResponse("""Admin not found""")

    if request.method =='POST':
        return redirect('updateAdmin')
    

    
    return render(request,'admin_profile.html', {'admin':admin})

@login_required(login_url='login')
def update_admin(request):
    
    # hr logged
    if(request.session['type']==1):
        return redirect('/gpgrama/update_Hr/' + str(request.session['id']))

    # hm logged
    if(request.session['type']==2):
        return redirect('/gpgrama/update_HiringManager/' + str(request.session['id']))

    try:
        admin = Admin.objects.first()
    except Admin.DoesNotExist:
         return HttpResponse("""Admin not found""")

    if request.method =='POST':
        updated_admin=AdminCreate(request.POST,  request.FILES, instance=admin)
        if updated_admin.is_valid():
            user = User.objects.get(username=updated_admin.instance.email)
            user.set_password(updated_admin.instance.password)
            user.save()
            update_session_auth_hash(request,user)
            if "images/admin" in updated_admin.instance.image.name:
                updated_admin.save()
                return redirect('/gpgrama/admin_profile')

            else:
                teste = updated_admin.save(commit=False)
                new_id = teste.uuid
                teste.image.name = str(new_id)+".jpg"
                teste.user.set_password(teste.password)
                #teste.user.save()   
                teste.save()
            return redirect('adminProfile')
        
    admin_form=AdminCreate(instance=admin)
    #with this type of form, in frontend just need to print  {% for field in form %} to get all parameters of needed
    return render(request,'admin_form.html', {'form':admin_form,'admin':admin})



@login_required(login_url='login')
def create_candidate(request):
    # hr logged
    if(request.session['type']==1):
        return redirect('/gpgrama/hr/' + str(request.session['id']))

    # hm logged
    if(request.session['type']==2):
        return redirect('/gpgrama/hm/' + str(request.session['id']))

    form = CandidateCreate()
    contact_person_list = list(HiringManager.objects.all()) + list(HR.objects.all())

    if request.method == 'POST':
        uploaded_candidate=CandidateCreate(request.POST,  request.FILES)

        contact_person_type = str(request.POST['contact_person_type'])
        contact_person_id = int(request.POST['contact_person_id'])

        if contact_person_type == 'HiringManager':
            uploaded_candidate.instance.responsibleHM = HiringManager.objects.get(pk=contact_person_id)
            uploaded_candidate.instance.responsibleHR = None

        elif contact_person_type == 'HR':
            uploaded_candidate.instance.responsibleHR = HR.objects.get(pk=contact_person_id)
            uploaded_candidate.instance.responsibleHM = None

        if uploaded_candidate.is_valid():
            teste = uploaded_candidate.save(commit=False)
            if str(request.POST['comments']) != '':
                date_string = date.today().strftime("%d/%m/%Y")
                teste.comments = str(request.session['name']) + ' - ' + date_string + ' || ' + '"' + str(request.POST['comments']) + '"'
            teste.last_update_name = str(request.session['name'])
            new_id = teste.uuid
            teste.last_update_name = str(request.session['name'])
            teste.image.name = str(new_id)+".jpg"
            teste.save()
            for file in request.FILES.getlist('myfiles'):
                handle_uploaded_file(file, new_id)

            return redirect('/gpgrama/candidate/'+str(teste.id))
        else:
            return render(request, 'candidateform.html', {'form':uploaded_candidate, 'contact_person_list':contact_person_list})
    #with this type of form, in frontend just need to print  {% for field in form %} to get all parameters of needed
    return render(request, 'candidateform.html', {'form':form, 'contact_person_list':contact_person_list})

from django.utils.html import escape
@login_required(login_url='login')
def list_candidates(request):

    candidate_filtered_hm = ""
    # hm logged but only can see the candidates he is responsible for
    if(request.session['type']==2):
        candidate_filtered_hm = Candidate.objects.filter(HiringManager=request.session['id'])
    
    filtered_candidates=""
    search_query=""
    if request.method =='POST':
        if request.POST.get("checkbox"):
            return redirect('pipeline')
        elif request.POST.get("create"):
            return redirect('createcandidate')
        elif request.POST.get("btn-search"):
            search_query = request.POST.get("query_search")
            search_query = search_query.strip()
            if(request.session['type']==2):
                filtered_candidates = candidate_filtered_hm.filter(name__icontains=search_query)
            else:
                filtered_candidates = Candidate.objects.filter(name__icontains=search_query)
        elif request.POST.get("candidate_id"):
            candidate_id=request.POST.get("candidate_id")
            return redirect("/gpgrama/candidate/"+str(candidate_id))


    contact_person_list = list(HiringManager.objects.all()) + list(HR.objects.all())
    candidate_list = Candidate.objects.all()


    if(filtered_candidates!=""):
        list_filter = CandidateFilter(request.GET, queryset=filtered_candidates)
    
    else:
        if(candidate_filtered_hm!=""):    
            list_filter = CandidateFilter(request.GET, queryset=candidate_filtered_hm)
        else:
            list_filter = CandidateFilter(request.GET, queryset=candidate_list)

    candidate_list = list_filter.qs
    print(candidate_list)
    return render(request,'candidates.html',{'candidate_list':candidate_list, 'list_filter':list_filter, 'contact_person_list':contact_person_list, 'search_query': search_query})

@login_required(login_url='login')
def filter_candidate(request):
    candidates = Candidate.objects.all()
    filtered_candidates = CandidateFilter(request.GET, queryset=candidates)
    return filtered_candidates


@login_required(login_url='login')
def filter_pipeline_candidate(request):
    candidates = Candidate.objects.all()
    filtered_candidates = CandidatePipelineFilter(request.GET, queryset=candidates)
    return render(request, 'gpgrama/candidate_filter.html', {'filter': filtered_candidates})

@login_required(login_url='login')
def candidate(request,candidate_id):

    candidate_id=int(candidate_id)

     # hm logged but only can see the ones is responsible for
    if(request.session['type']==2):
        candidate_perfil=Candidate.objects.get(id=candidate_id)
        if(candidate_perfil.HiringManager.id != request.session['id']):
            return redirect('/gpgrama/listCandidates/')
    
    
    if(request.method=='POST'):
        return redirect('/gpgrama/updatecandidate/' + str(candidate_id))

    try:
        candidate_perfil=Candidate.objects.get(id=candidate_id)
        file_list = candidate_perfil.fileOwner.all()
        print(file_list)
    except Candidate.DoesNotExist:
         return HttpResponse("""Candidate does not exist""")
    
    candidate_status = ""
    if (candidate_perfil.status == 0):
        candidate_status = "Lead"
    elif (candidate_perfil.status == 1):
        candidate_status = "Active"
    elif (candidate_perfil.status == 2):
        candidate_status = "On-hold"
    elif (candidate_perfil.status == 3):
        candidate_status = "Not interested"

    pipeline_status = ""
    if(candidate_perfil.pipeline_status==0):
        pipeline_status = "For future revision"
    elif(candidate_perfil.pipeline_status==1):
        pipeline_status = "On-hold"
    elif(candidate_perfil.pipeline_status==2):
        pipeline_status = "Dropped"
    elif(candidate_perfil.pipeline_status==3):
        pipeline_status = "In process - Phone Interview"
    elif(candidate_perfil.pipeline_status==4):
        pipeline_status = "In process - Interviewing"
    elif(candidate_perfil.pipeline_status==5):
        pipeline_status = "In process - Proposal Sent"
    elif(candidate_perfil.pipeline_status==6):
        pipeline_status = "Contracted"
    elif(candidate_perfil.pipeline_status==7):
        pipeline_status = "Proposal Rejected"

    exp_level=""
    if(candidate_perfil.years_exp==1):
        exp_level = "Entry-level"

    elif(candidate_perfil.years_exp==2):
        exp_level = "Junior"

    elif(candidate_perfil.years_exp==3):
        exp_level = "Mid"
    
    elif(candidate_perfil.years_exp==4):
        exp_level = "Senior"


    comments_person = []
    comments = []
    if (candidate_perfil.comments!=""):
        get_comments = candidate_perfil.comments.split(" && ")
        for comment in get_comments:
            get_comments_person = comment.split (" || ")
            comments_person.append(get_comments_person[0])
            comments.append(get_comments_person[1])
        
        zipped_comments = zip(comments_person,comments)
    
    else:
        zipped_comments = []
    
    print("data: " , candidate_perfil.lastupdate.strftime('%d-%m-%Y'))
    last_update = ""
    if(candidate_perfil.lastupdate!=""):
        last_update = str(candidate_perfil.lastupdate.strftime('%d-%m-%Y'))
        
    return render(request,'candidate.html', {'candidate_perfil':candidate_perfil, 'pipeline_status': pipeline_status, 'candidate_status': candidate_status, 'comments': zipped_comments,'file_list':file_list, 'last_update': last_update, 'exp_level': exp_level})


@login_required(login_url='login')
def update_candidate(request,candidate_id):
    candidate_id=int(candidate_id)

     # hm logged but only can see the ones is responsible for
    if(request.session['type']==2):
        candidate_perfil=Candidate.objects.get(id=candidate_id)
        if(candidate_perfil.HiringManager.id != request.session['id']):
            return redirect('/gpgrama/listCandidates/')

    contact_person_list = list(HiringManager.objects.all()) + list(HR.objects.all())

    try:
        candidate=Candidate.objects.get(id=candidate_id)
        file_list = candidate.fileOwner.all()
    except Candidate.DoesNotExist:
         return HttpResponse("""Candidate does not exist""")

    candidate_status = ""
    if (candidate.status == 0):
        candidate_status = "Lead"
    elif (candidate.status == 1):
        candidate_status = "Active"
    elif (candidate.status == 2):
        candidate_status = "On-hold"
    elif (candidate.status == 3):
        candidate_status = "Not interested"

    pipeline_status = ""
    if(candidate.pipeline_status==0):
        pipeline_status = "For future revision"
    elif(candidate.pipeline_status==1):
        pipeline_status = "On-hold"
    elif(candidate.pipeline_status==2):
        pipeline_status = "Dropped"
    elif(candidate.pipeline_status==3):
        pipeline_status = "In process - Phone Interview"
    elif(candidate.pipeline_status==4):
        pipeline_status = "In process - Interviewing"
    elif(candidate.pipeline_status==5):
        pipeline_status = "In process - Proposal Sent"
    elif(candidate.pipeline_status==6):
        pipeline_status = "Contracted"
    elif(candidate.pipeline_status==7):
        pipeline_status = "Proposal Rejected"

    comments_person = []
    comments = []
    if (candidate.comments!=""):
        get_comments = candidate.comments.split(" && ")
        for comment in get_comments:
            get_comments_person = comment.split (" || ")
            comments_person.append(get_comments_person[0])
            comments.append(get_comments_person[1])
        
        zipped_comments = zip(comments_person,comments)
    else:
        zipped_comments = []

    candidate_form=CandidateCreate(instance=candidate)

    if request.method =='POST':
        updated_candidate=CandidateCreate(request.POST, request.FILES, instance=candidate)
        if(request.POST.get("delete_candidate")):  
            try:
                candidate_perfil=Candidate.objects.get(id=candidate_id)
            except Candidate.DoesNotExist:
                return HttpResponse("""HiringManager does not exist""")
            # candidate_perfil.user.delete()
            candidate_perfil.delete()
            return redirect("list_candidates")

        if(request.POST.get("new_comment")):      
            try:
                candidate_perfil=Candidate.objects.get(id=candidate_id)
            except Candidate.DoesNotExist:
                return HttpResponse("""HiringManager does not exist""")      
        
        contact_person_type = str(request.POST['contact_person_type'])
        contact_person_id = int(request.POST['contact_person_id'])

        if contact_person_type == 'HiringManager':
            updated_candidate.instance.responsibleHM = HiringManager.objects.get(pk=contact_person_id)
            updated_candidate.instance.responsibleHR = None

        elif contact_person_type == 'HR':
            updated_candidate.instance.responsibleHR = HR.objects.get(pk=contact_person_id)
            updated_candidate.instance.responsibleHM = None

        if updated_candidate.is_valid():
            teste = updated_candidate.save(commit=False)
            new_id = teste.uuid
            if "images/candidate" not in updated_candidate.instance.image.name:
                teste.image.name = str(new_id)+".jpg"
            if str(request.POST['comment-popup']) != ' Add comment... ' and str(request.POST['comment-popup']) != '' :
                if teste.comments == '':
                    date_string = date.today().strftime("%d/%m/%Y")
                    teste.comments = str(request.session['name']) + ' - ' + date_string + ' || ' + '"' + str(request.POST['comment-popup']) + '"'
                else:
                    date_string = date.today().strftime("%d/%m/%Y")
                    teste.comments += ' && ' + str(request.session['name']) + ' - ' + date_string + ' || ' + '"' + str(request.POST['comment-popup']) + '"'
            teste.save()
            for file in request.FILES.getlist('myfiles'):
                handle_uploaded_file(file, new_id)
            return redirect("/gpgrama/candidate/"+str(candidate_id))

    #with this type of form, in frontend just need to print  {% for field in form %} to get all parameters of needed
    return render(request,'editCandidateform.html', {'form':candidate_form, 'contact_person_list':contact_person_list, 'pipeline_status': pipeline_status, 'candidate_status': candidate_status, 'comments': zipped_comments, 'file_list':file_list,'candidate':candidate})

@login_required(login_url='login')
def delete_candidate(request,candidate_id):
    # hr logged
    if(request.session['type']==1):
        return redirect('/gpgrama/hr/' + str(request.session['id']))

    # hm logged
    if(request.session['type']==2):
        return redirect('/gpgrama/hm/' + str(request.session['id']))

    candidate_id=int(candidate_id)
    try:
        candidate_perfil=Candidate.objects.get(id=candidate_id)
    except Candidate.DoesNotExist:
         return HttpResponse("""Candidate does not exist""")
    candidate_perfil.delete()

    return redirect('list_candidates')


@login_required(login_url='login')
def navbar(request):
    return render(request,'navbar.html')

@login_required(login_url='login')
def base(request):
    return render(request,'base.html')


@login_required(login_url='login')
def list_hr(request):
    
    # hr logged
    if(request.session['type']==1):
        return redirect('/gpgrama/list_hm')

    # hm logged
    if(request.session['type']==2):
        return redirect('/gpgrama/hm/' + str(request.session['id']))


    if(request.method=='POST'):
        if(request.POST.get("bottom")):
            hr_id=request.POST.get("bottom")
            return redirect('/gpgrama/hr/' + str(hr_id))

        if(request.POST.get("create_hr")):
            return redirect('/gpgrama/create_Hr/')

        if request.POST.get("btn-search"):
            search_query = request.POST.get("query_search")
            search_query = search_query.strip()
            filtered_hrs = HR.objects.filter(name__icontains=search_query)
            return render(request, 'list_hr.html', {'hr_list': filtered_hrs, 'search_query':search_query})
            
    hr_list = HR.objects.all()
    return render(request, 'list_hr.html', {'hr_list': hr_list})


@login_required(login_url='login')
def list_hm(request):
    # hm logged
    if(request.session['type']==2):
        return redirect('/gpgrama/hm/' + str(request.session['id']))
    
    if(request.method=='POST'):
        if(request.POST.get("bottom")):
            hm_id=request.POST.get("bottom")
            return redirect('/gpgrama/hm/' + str(hm_id))

        if(request.POST.get("create_hm")):
            return redirect('/gpgrama/create_HiringManager/')

        if request.POST.get("btn-search"):
            search_query = request.POST.get("query_search")
            search_query = search_query.strip()
            filtered_hms = HiringManager.objects.filter(name__icontains=search_query)
            return render(request, 'list_hm.html', {'hm_list': filtered_hms, 'search_query':search_query})

    hm_list = HiringManager.objects.all()
    return render(request, 'list_hm.html', {'hm_list': hm_list})


@login_required(login_url='login')
def pipeline(request):
    filtered_candidates = []
    if request.method =='POST':
        if request.POST.get("checkbox"):
            return redirect('list_candidates')
        if request.POST.get("create"):
            return redirect('createcandidate')
        if request.FILES:
            
            for filename, file in request.FILES.items():
                #print(filename)#has the id of the candidate to upload the file
                #print(file)#file to save in firebase
                try:
                    candidate=Candidate.objects.get(id=filename)
                    new_id = candidate.uuid
                except Candidate.DoesNotExist:
                    return HttpResponse("""Candidate does not exist""")
                handle_uploaded_file(file, new_id)
            return redirect('pipeline')


        if request.POST.get("submit_comment"):
            comment=request.POST.get("comment")
            candidate_id= request.POST.get("submit_comment")
            try:
                candidate=Candidate.objects.get(id=candidate_id)
            except Candidate.DoesNotExist:
                return HttpResponse("""Candidate does not exist""")

            if len(candidate.pipeline_comments)>0:
                #separate comments with point
                candidate.pipeline_comments+=". "+comment
            else:
                candidate.pipeline_comments=comment

            candidate.save()
            return redirect('pipeline')

        if request.POST.get("submit_status"):
            status_pipeline=request.POST.get("status_pipeline")
            candidate_id= request.POST.get("submit_status")

            try:
                candidate=Candidate.objects.get(id=candidate_id)
            except Candidate.DoesNotExist:
                return HttpResponse("""Candidate does not exist""")

            candidate.pipeline_status=status_pipeline

            candidate.save()
            return redirect('pipeline')
   
        if request.POST.get("add_filters") or request.POST.get("btn-search"):

            search_query = request.POST.get("query_search")
            search_query = search_query.strip()

            comments = request.POST.get("comments")
            comments = comments.strip()
            status_filter=request.POST.get("status_filter")
            if (int(status_filter)==0):
                if (comments==""):
                    list = Candidate.objects.filter(status=1)
                    if(request.session['type']==2):
                        list = list.filter(HiringManager=request.session['id'])

                    if (search_query==""):
                        list_all_files=[]
                        for candidate in list:
                            file_list = candidate.fileOwner.all()
                            list_all_files.append(file_list)

                        list_of_list = zip(list,list_all_files)
                        return render(request,'pipeline.html',{'list_of_list':list_of_list,'size_list':len(list)})
                    
                    else:
                        filtered_candidates = list.filter(name__icontains=search_query)
                        list_all_files=[]
                        for candidate in filtered_candidates:
                            file_list = candidate.fileOwner.all()
                            list_all_files.append(file_list)

                        list_of_list = zip(filtered_candidates,list_all_files)
                        return render(request, 'pipeline.html', {'list_of_list':list_of_list, 'search_query': search_query,'size_list':len(filtered_candidates)})

                else:
                    filtered_candidates = Candidate.objects.filter(pipeline_comments__icontains=comments)
                    filtered_candidates = filtered_candidates.filter(status=1)
    
                    if(request.session['type']==2):
                        filtered_candidates = filtered_candidates.filter(HiringManager=request.session['id'])

                    if (search_query==""):
                        list_all_files=[]
                        for candidate in filtered_candidates:
                            file_list = candidate.fileOwner.all()
                            list_all_files.append(file_list)

                        list_of_list = zip(filtered_candidates,list_all_files)
                        return render(request, 'pipeline.html', {'list_of_list':list_of_list, 'comments_filtered': comments,'size_list':len(filtered_candidates)})
                    else:
                        filtered_candidates = filtered_candidates.filter(name__icontains=search_query)
                        list_all_files=[]
                        for candidate in filtered_candidates:
                            file_list = candidate.fileOwner.all()
                            list_all_files.append(file_list)

                        list_of_list = zip(filtered_candidates,list_all_files)
                        return render(request, 'pipeline.html', {'list_of_list':list_of_list, 'search_query': search_query, 'comments_filtered': comments,'size_list':len(filtered_candidates)})


            else:
                status_filter1 = int(status_filter)
                status_filter1 = status_filter1 - 1
                filtered_candidates =  Candidate.objects.filter(pipeline_status=status_filter1)
                if (comments==""):
                    filtered_candidates = filtered_candidates.filter(status=1)
                    if(request.session['type']==2):
                        filtered_candidates = filtered_candidates.filter(HiringManager=request.session['id'])

                    if (search_query==""):
                        list_all_files=[]
                        for candidate in filtered_candidates:
                            file_list = candidate.fileOwner.all()
                            list_all_files.append(file_list)

                        list_of_list = zip(filtered_candidates,list_all_files)
                        return render(request,'pipeline.html',{'list_of_list':list_of_list, 'status_filtered': status_filter,'size_list':len(filtered_candidates)})

                    else:
                        filtered_candidates = filtered_candidates.filter(name__icontains=search_query)
                        list_all_files=[]
                        for candidate in filtered_candidates:
                            file_list = candidate.fileOwner.all()
                            list_all_files.append(file_list)

                        list_of_list = zip(filtered_candidates,list_all_files)
                        return render(request, 'pipeline.html', {'list_of_list':list_of_list, 'status_filtered': status_filter, 'search_query': search_query,'size_list':len(filtered_candidates)})

                else:
                    filtered_candidates = Candidate.objects.filter(pipeline_comments__icontains=comments)
                    filtered_candidates = filtered_candidates.filter(status=1)

                    if(request.session['type']==2):
                        filtered_candidates = filtered_candidates.filter(HiringManager=request.session['id'])

                    if (search_query==""):
                        list_all_files=[]
                        for candidate in filtered_candidates:
                            file_list = candidate.fileOwner.all()
                            list_all_files.append(file_list)

                        list_of_list = zip(filtered_candidates,list_all_files)
                        return render(request, 'pipeline.html', {'list_of_list':list_of_list, 'status_filtered': status_filter, 'comments_filtered': comments,'size_list':len(filtered_candidates)})
                    else:
                        filtered_candidates = filtered_candidates.filter(name__icontains=search_query)
                        list_all_files=[]
                        for candidate in filtered_candidates:
                            file_list = candidate.fileOwner.all()
                            list_all_files.append(file_list)

                        list_of_list = zip(filtered_candidates,list_all_files)
                        return render(request, 'pipeline.html', {'list_of_list':list_of_list, 'status_filtered': status_filter, 'search_query': search_query, 'comments_filtered': comments,'size_list':len(filtered_candidates)})

    candidate_list = Candidate.objects.filter(status=1)

    # Check, if the user is Hiring Manager
    # hm logged but only can see the candidates he is responsible for
    if(request.session['type']==2):
        candidate_list = candidate_list.filter(HiringManager=request.session['id'])
    

    list_all_files=[]
    for candidate in candidate_list:
        file_list = candidate.fileOwner.all()
        list_all_files.append(file_list)

    list_of_list = zip(candidate_list,list_all_files)
    return render(request,'pipeline.html',{'list_of_list':list_of_list,'size_list':len(candidate_list)})


@login_required(login_url='login')
def manage_permissions(request):
    # hr logged
    if(request.session['type']==1):
        return redirect('/gpgrama/hr/' + str(request.session['id']))

    # hm logged
    if(request.session['type']==2):
        return redirect('/gpgrama/hm/' + str(request.session['id']))

    return render(request,'manage_permissions.html')
