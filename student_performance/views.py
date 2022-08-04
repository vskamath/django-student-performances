
from django.shortcuts import redirect
from student_performance.models import Student, Performance
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication  import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Max
from django.contrib.auth import logout

# API endpoint to view the Student Performance
@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def student_performance(request):
    ## Students will login using their Roll Number as Username
    user_id = request.user.username
    if user_id=='admin':
        return redirect('http://127.0.0.1:8000/admin/')

    ## Obtain the Student Object corresponding to the Roll Number
    try:
        student = Student.objects.get(roll_number=int(user_id))
    except Student.DoesNotExist:
        return Response({'message':'Roll Number is not available in our system. Please contact Admin'})
    except Student.MultipleObjectsReturned:
        return Response({'message':'Multiple entries for Roll Number is present in our system. Please contact Admin'})
    
    ## Obtain the Performance Object corresponding to the Roll Number
    try:
        performance = Performance.objects.get(student_id = student.roll_number)
    except Performance.DoesNotExist:
        return Response({'message':'Performance for this Roll Number is not available in our system. Please contact Admin'})

    ## Obtain the highest scorers ( Individual as well as Overall)
    english_highest = Performance.objects.aggregate(Max('english_marks'))
    science_highest = Performance.objects.aggregate(Max('science_marks'))
    CS_highest      = Performance.objects.aggregate(Max('CS_marks'))
    maths_highest   = Performance.objects.aggregate(Max('maths_marks'))
    overall_highest = Performance.objects.aggregate(Max('total_marks'))

    ## Build response data
    data = {
        'roll_number':student.roll_number,
        'student_name':student.name,
        'student_data':{ 
            'english_marks' : getattr(performance, 'english_marks' ),
            'CS_marks'      : getattr(performance, 'CS_marks' ),
            'maths_marks'   : getattr(performance, 'maths_marks' ),
            'science_marks' : getattr(performance, 'science_marks' ),
            'total_marks'   : getattr(performance, 'total_marks' ),
        },
        'english_highest':english_highest['english_marks__max'],
        'CS_highest':CS_highest['CS_marks__max'],
        'maths_highest':maths_highest['maths_marks__max'],
        'science_highest':science_highest['science_marks__max'],
        'highest_total':overall_highest['total_marks__max'],
    }
    return Response(data)

# Homepage of the Backend
@api_view(['GET'])
def hompage(request):
    user_id = request.user.username
    if user_id=='admin':
        return redirect('http://127.0.0.1:8000/admin/')
    try:
        student = Student.objects.get(roll_number=int(user_id))
        return Response({'message':f'Hi {student.name}. Kindly visit http://127.0.0.1:8000/view/ to view your performace'})
    except:
        return Response({'message':'Welcome to the Student-Performance Backend API. Kindly visit http://127.0.0.1:8000/view/ to view your performace.'})

# Endpoint for the User to logout (Redirection to Homepage)
@api_view(['GET'])
def user_logout(request):
    logout(request)
    return redirect('http://127.0.0.1:8000/')