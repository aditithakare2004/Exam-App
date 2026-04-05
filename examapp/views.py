from django.shortcuts import render
from django.http import HttpResponse
from examapp.models import Questions, UserData, Result
from django.contrib.auth import logout

# Create your views here.
def Home (request):
    return render(request ,'home.html')

def Give_Me_Questioncurd_Page(request):
    return render(request,'question/questioncurd.html')

def Give_Me_AddQuestion_Page(request):
    return render(request,'question/addquestion.html')

def Give_Me_ViewQuestion_Page(request):
    return render(request,'question/viewquestion.html')

def Give_Me_UpdateQuestion_Page(request):
    return render(request,'question/updatequestion.html')

def Give_Me_DeleteQuestion_Page(request):
    return render(request,'question/deletequestion.html')

def Give_Me_ShowAllQuestion_Page(request):
    qdata = Questions.objects.all()
    return render(request,'question/showallquestion.html',{'qdata':qdata})


def AddQuestions(request):
    if request.method == "POST":
        qno = request.POST.get('qno')
        qtext = request.POST.get('qtext')
        op1 = request.POST.get('op1')
        op2 = request.POST.get('op2')
        op3 = request.POST.get('op3')
        op4 = request.POST.get('op4')
        subject = request.POST.get('subject')
        answer = request.POST.get('answer')

        # ✅ validation
        if not qno:
            return render(request, 'question/addquestion.html', {'message': 'qno is required'})

        Questions.objects.create(
            qno=qno,
            qtext=qtext,
            op1=op1,
            op2=op2,
            op3=op3,
            op4=op4,
            subject=subject,
            ans=answer
        )

        return render(request, 'question/addquestion.html', {'message': 'Question added Successfully'})

    return render(request, 'question/addquestion.html')

def View_Question(request):
    qno = request.GET['qno']
    qdata = Questions.objects.get(qno=qno)
    return render (request,'question/viewquestion.html' ,{'qdata' : qdata})

def View_Question_Update(request):
    qno = request.GET['qno']
    qdata = Questions.objects.get(qno=qno)
    return render (request,'question/updatequestion.html' ,{'qdata' : qdata})

def UpdateQuestion(request):
    qno = request.GET['qno']
    qdata = Questions.objects.filter(qno=qno)
    qdata.update(
        qtext = request.GET['qtext'],
        op1 =request.GET['op1'],
        op2 =request.GET['op2'],
        op4 =request.GET['op4'],
        subject = request.GET['subject'],
        ans = request.GET['answer']
    )
    return render (request,'question/updatequestion.html' ,{'message' : 'Question updated Successfully'})

def View_Question_Delete(request):
    qno = request.GET['qno']
    qdata = Questions.objects.get(qno=qno)
    return render (request,'question/deletequestion.html' ,{'qdata' : qdata})

def DeleteQuestion(request):
    qno = request.GET['qno']
    subject = request.GET['subject']

    Questions.objects.filter(qno=qno, subject=subject).delete()
    return render (request,'question/deletequestion.html' ,{'message' : 'Question deleted Successfully'})


########################################################################################################################

# For Students 

def GiveMeRagisterPage(request):
    return render(request,'student/ragister.html')


def Ragister(request):
    uname = request.GET['username']
    passwd = request.GET['password']
    mobno = request.GET['mobno']

    UserData.objects.create(username = uname, password =passwd , mobno = mobno)
    return render(request,'student/login.html',{'message': 'user ragistered successfully'})

def GiveMeLoginPage(request):
    return render(request,'student/login.html')


def Login(request):
    uname = request.GET['username']
    passwd = request.GET['password']
    udata = UserData.objects.get(username = uname)

    if (udata.password == passwd):
        request.session['username'] = uname
        request.session['answer'] = {}
        request.session['score'] = 0
        request.session['qno'] = 0 
        return render(request,'question/subject.html')
    else :
        return render(request,'student/login.html',{'message':'invalid password'})
    
def GiveMeUserCurdPage(request):
    return render(request,'student/usercurd.html')


def GiveMeShowAllPage(request):
    udata = UserData.objects.all()
    return render(request,'student/showall.html',{'udata':udata})
 

def AddUser(request):
    uname = request.GET['username']
    passwd = request.GET['password']
    mobno = request.GET['mobno']

    UserData.objects.create(username = uname, password = passwd , mobno = mobno)
    return render(request,'student/usercurd.html',{'message': 'user ragistered successfully'})

def ShowUser(request):
    try : 
        uname = request.GET['username']
        udata = UserData.objects.get(username = uname)
        return render(request,'student/usercurd.html',{'udata':udata})
    except :
         return render(request,'student/usercurd.html',{'message': 'user not Found'})

def UpdateUser(request):
    uname = request.GET['username']
    udata = UserData.objects.filter(username = uname)
    udata.update(password = request.GET['password'], mobno = request.GET['mobno'])
    return render(request,'student/usercurd.html',{'message': 'user updated successfully'})

def DeleteUser(request):
    uname = request.GET['username']
    UserData.objects.filter(username = uname).delete()
    return render(request,'student/usercurd.html',{'message': 'user deleted successfully'})

def DeleteUserForShowAllPage(request):
    uname = request.GET['username']
    UserData.objects.filter(username = uname).delete()
    udata = UserData.objects.all()
    return render(request,'student/showall.html',{'udata':udata})


def StartTest(request):
    subject = request.GET['subject']
    request.session['subject'] = subject

    questions = Questions.objects.filter(subject=subject).values()
    allquestions = list(questions)

    request.session['allquestions'] = allquestions

    return render(request, 'starttest.html', {'question':allquestions[0]})

def NextQuestion(request):
    allquestions = request.session['allquestions']
    questionindex = request.session['qno']
    
    if 'op' in request.GET:
        allanswer = request.session['answer']
        allanswer[request.GET['qno']] = [request.GET['qno'], request.GET['qtext'], request.GET['op'], request.GET['answer']]

        # allanswer = {}
        # allanswer = {1:[1, 100/4, 25, 25], 1:[2, 10+10, 15, 20]}

    try:
        if questionindex < len(allquestions):
            request.session['qno'] += 1
            question = allquestions[request.session['qno']]
            return render(request, 'starttest.html', {'question':question})
        
    except:
        return render(request, 'starttest.html', {'msg':'Go to previous question'})

def PreviousQuestion(request):
    allquestions = request.session['allquestions']
    questionindex = request.session['qno']
    
    if 'op' in request.GET:
        allanswer = request.session['answer']
        allanswer[request.GET['qno']] = [request.GET['qno'], request.GET['qtext'], request.GET['op'], request.GET['answer']]

        # allanswer = {}
        # allanswer = {1:[1, 100/4, 25, 25], 1:[2, 10+10, 15, 20]}

    try:
        if questionindex > 0:
            request.session['qno'] -= 1
            question = allquestions[request.session['qno']]
            return render(request, 'starttest.html', {'question':question})
        else:
            return render(request, 'starttest.html', {'msg':'Go to next question'})
        
    except:
        return render(request, 'starttest.html', {'msg':'Go to next question'})

def EndTest(request):

    if 'op' in request.GET:
        allanswer = request.session['answer']
        allanswer[request.GET['qno']] = [request.GET['qno'], request.GET['qtext'], request.GET['op'], request.GET['answer']]

    response = request.session['answer'].values()

    for res in response:
        if res[2]==res[3]:
            request.session['score'] += 1

    finalscore = request.session['score']

    uname = request.session['username']

    userdb = UserData.objects.get(username=uname)

    Result.objects.create(
        username = userdb,
        subject = request.session['subject'],
        score = finalscore
    )

    return render(request, 'result/scorecard.html', {'response':response, 'finalscore':finalscore})

def ShowAllResults(request):
    resultdb = Result.objects.all()
    return render(request, 'result/showallresults.html', {'resultdb':resultdb})

def LogOutUser(request):
    logout(request)
    return render(request, 'student/login.html')
    

 ##########################################################################################################
