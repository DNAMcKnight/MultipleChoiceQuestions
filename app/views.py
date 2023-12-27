from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User, auth
from django.shortcuts import redirect
from django.contrib import messages
from django.shortcuts import render
from .forms import FileUploadForm
from .models import UserQuestions
from .generate import generator
from .models import MCQ
import random, json
import uuid

        
@login_required(login_url='login')
def home(request):
    encoded_id = request.session.get('encoded_id', None)
    if not encoded_id:
        question = random.choice(MCQ.objects.all())
        create_id = str(uuid.uuid4())
        userQuestions = UserQuestions(encoded_id=create_id, used_question=[question.id])
        userQuestions.save()
        request.session['encoded_id'] = (create_id)
    else:
        if not UserQuestions.objects.filter(encoded_id=encoded_id).exists():
            del request.session['encoded_id']
            return redirect('home')
        questions = MCQ.objects.all()
        userQuestions = UserQuestions.objects.get(encoded_id=encoded_id)
        for i in userQuestions.used_question:
            questions = questions.exclude(id=i)
        question = random.choice(questions)
    if request.method=='POST':
        question_id = request.POST['question']
        userQuestions.used_question += [question_id]
        userQuestions.save()
        return redirect('home')
        
    options = list(question.options)
    random.shuffle(options)
    data = {
        'question': question.question,
        'option1': options[0],
        'option2': options[1],
        'option3': options[2],
        'option4': options[3],
        'answer': question.answer,
        'answered': len(userQuestions.used_question),
        'totalQ': len(MCQ.objects.all()),
        'id': question.id
        }
    return render(request, 'index.html', data)


def login(request):
    try:
        auth.logout(request)
    except Exception:
        pass

    print(request.user)
    if request.method=='POST':
        password=request.POST['password']
        username=request.POST['username']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            messages.info(request,f'Welcome {request.user}')
            return redirect('home')
        else:
            messages.info(request,'Credential Invalid')
            return redirect('login')
    else:
        return render(request, "login.html")
    
    
def signup(request):
    try:
        auth.logout(request)
    except Exception:
        pass
    if request.method=='POST':
        username=request.POST['username'].lower()
        passwords=request.POST['password'] 
        email=request.POST['emailaddress']
        if User.objects.filter(email=email).exists():
            messages.info(request,'Email Already In Use')
        elif User.objects.filter(username=username).exists():
            messages.info(request,'Username Already In Use')
        else:    
            user=User.objects.create_user(username=username,email=email,password=passwords)
            user.save();
            messages.info(request,'Sign Up Successfull')

        return redirect('Signup')
    return render(request, "signup.html")

def logout(response):
    auth.logout(response)
    return redirect('home')

@login_required(login_url='login')
def generate(request):
    if not request.user.is_superuser:
        return redirect('home')
    try:
        generator('/Video-Audio/development/PythonSideProjects/TTC/text.txt')
        return redirect('home')
    except ValueError:
        return redirect('home')

@login_required(login_url='login')
def export(request):
    if not request.user.is_superuser:
        return redirect('home')
    questions = MCQ.objects.all()
    data = []
    for question in questions:
        questionSet = {}
        questionSet['question']=(question.question)
        questionSet['options']=question.options
        questionSet['answer']= question.answer
        data.append(questionSet)
    #     for option in question.options:
    #         if option == question.answer:
    #             data.append(f"Ans: {option}")
    #         else:
    #             data.append(option)
    print(len(data))
    return JsonResponse(data, safe=False)

@login_required(login_url='login')
def importData(request):
    if not request.user.is_superuser:
        return redirect('home')
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                uploaded_file = form.cleaned_data['file'].read().decode('utf-8')
                data = json.loads(uploaded_file)
                for entry in data:
                    question = entry['question']
                    options = entry['options']
                    answer = entry['answer']
                    print(question, options, answer)
                    mcq = MCQ(question=question, options=options, answer=answer, bangla=False)
                    mcq.save()
                return redirect ('home')
            except Exception:
                form = FileUploadForm()
                messages.error(request, "Error, not a valid import file")
                return render(request, 'import.html', {'form': form})
    else:
        form = FileUploadForm()
    return render(request, 'import.html', {'form': form})
    
    # file_path = "/Video-Audio/development/PythonSideProjects/TTC/export.json"
    
    # return HttpResponse("success")
            
def reset(request):
    encoded_id = request.session.get('encoded_id', None)
    if not UserQuestions.objects.filter(encoded_id=encoded_id).exists():
        del request.session['encoded_id']
        return redirect('home')
    data = UserQuestions.objects.get(encoded_id=encoded_id)
    data.delete()
    return redirect('home')