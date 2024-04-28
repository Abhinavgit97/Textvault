from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
from .models import ContentTable, TagTable
from django.utils import timezone
from datetime import datetime, timedelta
from .serializers import LoginSerializer, UserSerializer,ContentSerializer,TagSerializer
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
@ensure_csrf_cookie
def index_page(request):
    return render(request, 'index.html', {})


@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(first_name,last_name,email,username,password)
        
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Username or email already exists"}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        user.save()
        return JsonResponse({"success": "User registered successfully"})
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            # print(f"Username and password {username , password}")
            user = authenticate(username=username, password=password)
            
            if user:
                login(request,user)
                refresh = RefreshToken.for_user(user)
                print("Userdata:",UserSerializer(user).data)
                request.session['user_name']=username
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                access_token_exp = datetime.now() + timedelta(seconds=3600)  #1hr
                return JsonResponse({
                    'access': access_token,
                    'refresh': refresh_token,
                    'access_exp': int(access_token_exp.timestamp()) 
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class RefreshView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            access_token_exp = datetime.now() + timedelta(seconds=3600) 

            print(f"access token : {access_token}")
            print(f"access token expiry: {access_token_exp}")
            return Response({'access': access_token,'access_exp': int(access_token_exp.timestamp())}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)
        

@login_required
def dashboard(request):
    # print(f"USER : {request.user}")
    user_firstname = User.objects.get(username=request.session['user_name']).first_name
    print(f"User name {user_firstname}")
    user_count = User.objects.count()
    doc_count = ContentTable.objects.count()
    tag_count = TagTable.objects.count()
    return render(request, 'dash.html', {"user_count":user_count,"doc_count":doc_count,"tag_count":tag_count,"user_firstname":user_firstname})



@login_required
def add_snippet(request):
    return render(request, 'add_snippet.html', {})


@csrf_exempt
@login_required
def create_snippet(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        tag_title = request.POST.get('tag')
        # print(f"Title : {title} , Content : {content} ,Tagtitle : {tag_title}")
        userdata = User.objects.get(username = request.session['user_name']) 
        tag, created = TagTable.objects.get_or_create(title=tag_title)
        snippet = ContentTable.objects.create(
            title=title,
            content=content,
            timestamp=timezone.now(),
            created_by=userdata,
            tag=tag
        )
        return JsonResponse({'message': 'Text saved successfully'}, status=201)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def list_all_snippets(request):
    return render(request, 'list_all_snippets.html', {})


@login_required
def snippet_detail(request, pk):
    snippet = get_object_or_404(ContentTable, pk=pk)
    serializer = ContentSerializer(snippet)
    return JsonResponse(serializer.data)

@login_required
def get_all_snippets(request):
    total_snippets = ContentTable.objects.count()
    snippets = ContentTable.objects.all()
    serializer = ContentSerializer(snippets, many=True)
    all_snippet_data = {
        'total_snippets': total_snippets,
        'snippets': serializer.data
    }
    return JsonResponse(all_snippet_data)

@login_required
def delete_snippets(request):
    if request.method == 'POST':
        id_list = request.POST.getlist('item_ids[]')  
        # print("IDs to delete-->",id_list)
        ContentTable.objects.filter(id__in=id_list).delete()
        updated_items = ContentTable.objects.all()
        serializer = ContentSerializer(updated_items, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def edit_snippet_page(request):
    if request.method == 'POST':
        topic_id = request.POST.get('snippet_id_inp')
        # print("TOPIC ID",topic_id)
        return render(request, 'edit_snippet.html', {'topic_id':topic_id}) 
    else:
        return render(request, 'error404.html')
    

@csrf_exempt
@login_required
def update_snippet(request, pk):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        tag_title = request.POST.get('tag')
        snippet = ContentTable.objects.get(pk=pk)
        snippet.title = title
        snippet.content = content
        tag, _ = TagTable.objects.get_or_create(title=tag_title)
        snippet.tag = tag
        snippet.save()
        return JsonResponse({'message': 'Content  updated successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def list_all_tags(request):
    return render(request, 'list_tags.html', {})

@login_required
def get_all_tags(request):
    tags = TagTable.objects.all()
    serializer = TagSerializer(tags, many=True)
    all_snippet_data = {
        'taglist': serializer.data
    }
    return JsonResponse(all_snippet_data)

@login_required
def get_content_by_tag(request, tag_title):
    try:
        content_by_tag = ContentTable.objects.filter(tag__title=tag_title)
        print(f"Tag title {tag_title}")
        serializer = ContentSerializer(content_by_tag, many=True)

        response_data = {
            'content': serializer.data
        }
        print(f"Response data {response_data}")
        
        return JsonResponse(response_data, status=200)
    except ContentTable.DoesNotExist:
        return JsonResponse({'error': 'Content not found for the given tag'}, status=404)

def handler404page(request,exception):
    return render(request, 'error_404.html')



@login_required
def do_logout(request):
    request.session['user_name'] = ""
    logout(request)
    return redirect('index_page')
