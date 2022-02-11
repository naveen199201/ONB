import imp
from .models import Student, User, Post
from .serializers import StudentSerializer, UserSerializer, PostSerializer, AdminSerializer
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly,AllowAny  # <-- Here
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


class AddPostView(APIView):
    permission_classes  = (IsAuthenticated,)

    def post(self, request):
        if hasattr(request, 'user'):
            user = request.user
            post_object = request.data
            if user.is_staff:
                Post.objects.create(**post_object)  
                content = {'status':200, 'message':'Succesfully posted the notice'}
            else:
                content = {'success':False,'message':'Invalid Permissions'}
        else:
            content = {'success':False, 'message':'Invalid Request'}
        return Response(content) 

class SinglePostView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CoAdminsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = User.objects.filter(role__in=['2'])
    serializer_class = UserSerializer

class UpdateCoAdmin(UpdateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def put(self, request, *args, **kwargs):
        instance = super().partial_update(request, *args, **kwargs)
        return Response({'success':True,'message':'Succesfully added as admin'})


class StudentDetail(RetrieveAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class CreateUserView(CreateAPIView):
    permission_classes = [AllowAny] # Or anon users can't register

    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            'status': 200,
            'message': 'Successfully created the user',
            'data': response.data
        })

class AddAdmin(CreateAPIView):
    permission_classes = [AllowAny] # Or anon users can't register

    serializer_class = AdminSerializer
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            'status': 200,
            'message': 'Successfully created the admin',
            'data': response.data
        })


class Login(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'message':'User login successfull',
            'status':200,
            'data':{
                'token': token.key,
                'user_id': user.pk,
                'is_staff':user.is_staff,
                'email': user.email,
                'role':user.role
            }
        })

class PostsViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role!='0':
            return Post.objects.all().order_by('-id')
        student = Student.objects.get(user=user)
        if student.batch=='1':
            posts = Post.objects.filter(target_year=1).order_by('-id')
        else:
            posts = Post.objects.filter(target_year=student.batch, target_audience=student.specialization).order_by('-id')
        return posts