from django.contrib.auth import forms
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import *
from .forms import PostForm, ProfileRegistrationForm,ProfileForm,CommentForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
import sys
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



#def base(request):
#   user_profile = Profile.objects.filter(user = request.user)
#    return render(request,'app/base.html',{'profile':user_profile})


def is_users(post_user, logged_user):
    return post_user == logged_user

class ProfileDetailView(LoginRequiredMixin,View):

    def get(self,request,pk):
        us =User.objects.get(id=pk)
        profile = Profile.objects.get(user = us)
        if profile :
            context = {"profile":profile}
            return render(request ,'app/profile.html',context)
        else:
            return redirect('profile_update')



class ProfileUpdateView(LoginRequiredMixin,View):
 
    def get(self,request,pk):
        obj = Profile.objects.get(pk=pk)
        form = ProfileForm(instance=obj)
        obj = Profile.objects.get(pk=pk)
        return render(request,'app/profileupdate.html', {"form": form, "acitve": "btn-primary","obj":obj}) 

    def post(self, request,pk):
        obj = Profile.objects.get(pk=pk)
        form =ProfileForm(request.POST,request.FILES,instance=obj)

        if form.is_valid():
            user = request.user
            college_name = form.cleaned_data["college_name"]
            Branch_Year = form.cleaned_data["Branch_Year"]
            location = form.cleaned_data["location"]
            image = form.cleaned_data["image"]
            skill = form.cleaned_data["skill"]
            profession = form.cleaned_data["profession"]
            reg = Profile(
                id=pk,
                user=user,
                college_name=college_name,
                Branch_Year=Branch_Year,
                location = location,
                image=image,
                skill = skill,
                profession =profession, 
            )
            reg.save()
            messages.success(request, "Congratulation !! Profile Updated Successfully")
            context = {"form": form, "active": "btn-primary"}
            return redirect("home")
   


#class HomeView(LoginRequiredMixin,View):
 #   def get(self,request):
  #      college = College.objects.filter(name="BTKIT")
       # post=Post.objects.filter(type='Information')
   #     profile = Profile.objects.filter(user = request.user)
   #     context = {"college":college,"profile":profile}
  #      return render(request,"app/home.html",context,)
    
class CommentDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Comment
    template_name = "app/commentdelete.html"
    success_url = "/"
    
    def test_func(self):
        return is_users(self.get_object().author, self.request.user)



class PostListView(LoginRequiredMixin,ListView):

    model = Post
    template_name = 'app/home.html'
    context_object_name = 'post'
    paginate_by = 5
    ordering = ['-date_posted']

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        post = self.get_queryset()
        page = self.request.GET.get('page')
        paginator = Paginator(post, self.paginate_by)
        try:
            post = paginator.page(page)
        except PageNotAnInteger:
            post = paginator.page(1)
        except EmptyPage:
            post = paginator.page(paginator.num_pages)
        context['post'] = post
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'app/postdetail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        comments_connected = Comment.objects.filter(post=self.get_object()).order_by('-date_posted')

        data['comments'] = comments_connected
    
        data['form'] = CommentForm(instance=self.request.user)
        return data

    def post(self, request, *args, **kwargs):
        form =CommentForm(request.POST)
        if form.is_valid():
          new_comment = Comment(comment=request.POST.get('comment'),
                              author=self.request.user,
                              post=self.get_object())
          new_comment.save()

        return self.get(self, request, *args, **kwargs)



class StudyMaterialListView(LoginRequiredMixin,ListView):

    model = Post
    template_name = 'app/studymaterial.html'
    context_object_name = 'sm'
    queryset = Post.objects.filter(type = 'StudyMaterial')
    paginate_by = 5
    ordering = ['-date_posted']

    def get_context_data(self, **kwargs):
        context = super(StudyMaterialListView, self).get_context_data(**kwargs)
        sm = self.get_queryset()
        page = self.request.GET.get('page')
        paginator = Paginator(sm, self.paginate_by)
        try:
            sm = paginator.page(page)
        except PageNotAnInteger:
            sm = paginator.page(1)
        except EmptyPage:
            sm = paginator.page(paginator.num_pages)
        context['post'] = sm
        return context


def about(request):
    return render(request,"app/about.html")


def download_pdf(request,url):
    return render(request,"")


class ProfileRegistrationView(View):
    def get(self, request):
        form = ProfileRegistrationForm()
        return render(request, "app/profileregistration.html", {"form": form})

    def post(self, request):
        form = ProfileRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, "Registration Completed ! Please go to Login Page")
            form.save()
        return redirect('home')





class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    template_name = "app/postdelete.html"
    success_url = "/"
    def test_func(self):
        return is_users(self.get_object().author, self.request.user)


class PostMakeView(LoginRequiredMixin,View):

    def get(self,request):
        form=PostForm()
        return render(request,'app/postcreate.html', {"form": form, "acitve": "btn-primary"})


    def post(self, request):
        form =PostForm(request.POST,request.FILES)
        if form.is_valid():
            user = request.user
            type = form.cleaned_data["type"]
            title = form.cleaned_data["title"]
            subtitle =  form.cleaned_data["subtitle"]
            content = form.cleaned_data["content"]
            image = form.cleaned_data["image"]
            pdf = form.cleaned_data["pdf"]
            reg = Post(
                author=user,
                type=type,
                title=title,
                content = content,
                subtitle =subtitle,
                image=image,
                pdf = pdf 

            )
            reg.save()
            messages.success(request, "Congratulation !! Post Created Successfully")
            context = {"form": form, "active": "btn-primary"}
            return redirect('home')



   