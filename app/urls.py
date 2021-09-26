
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm,PasswordChangeForm,PasswordresetForm,PasswordSetForm

urlpatterns = [

    path('',views.PostListView.as_view(),name = 'home'),

    path('profile/<int:pk>/',views.ProfileDetailView.as_view(),name='profile-detail'),
    path('profile_update/<int:pk>/',views.ProfileUpdateView.as_view(),name='profile_update'),


    #path('profile/',views.ProfileView.as_view(),name='profile'),
    path('studymaterial/',views.StudyMaterialListView.as_view() ,name='SM'),
    path('about/',views.about,name='about'),

    #POST DETAILS ,DELETE,EDIT
    path('post_detail/<int:pk>',views.PostDetailView.as_view(),name  = 'post-detail'),
    path('post_create/',views.PostMakeView.as_view(),name  = 'post-create'),
    path('post_delete/<int:pk>/',views.PostDeleteView.as_view(),name='post-delete'),
    path('comment_delete/<int:pk>/',views.CommentDeleteView.as_view(),name='comment-delete'),




    path('registration/',views.ProfileRegistrationView.as_view(),name = 'registration'),
    path('accounts/login/', auth_view.LoginView.as_view(
        template_name='app/login.html',
        authentication_form=LoginForm,
    ), 
    name='login'),
    path('logout/',auth_view.LogoutView.as_view(next_page='login'),name='logout'),
    path('password_change/',auth_view.PasswordChangeView.as_view(
        template_name='app/password_change.html',
        form_class=PasswordChangeForm,
        success_url = '/passwordchangedone/'
    ),name='password_change'),

    path('passwordchangedone/',auth_view.PasswordChangeDoneView.as_view(
         template_name='app/passwordchangedone.html',
        
    ),name='password_change_done'),

    path('password_reset/',auth_view.PasswordResetView.as_view(
        template_name = 'app/passwordreset.html',
        form_class = PasswordresetForm,
     
    ),name='password_reset'),


    path('password_reset/done/',auth_view.PasswordResetDoneView.as_view(
        template_name = 'app/passwordresetdone.html'   
    ),name='password_reset_done'),

    path('password_reset-confrim/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(
        template_name = 'app/passwordresetconfirm.html',
        form_class = PasswordSetForm,
     
    ),name='password_reset_confirm'),
    
    path('password_reset_complete/',auth_view.PasswordResetCompleteView.as_view(
        template_name='app/passwordresetcomplete.html',
    ),name='password_reset_complete'),
]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
