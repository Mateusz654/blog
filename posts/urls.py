from django.urls import path
from .views import login_user, register_user,logout_user, show_posts, delete_post, edit_post, add_post,choose_post,add_comment,delete_comment,edit_comment,user_profile,comeback,toggle_like


urlpatterns =[
    path('', login_user, name='login'),
    path('register/', register_user, name='register'),
    path('logout/', logout_user, name='logout'),
    path('posts/', show_posts, name='post-list'),
    path('delete_post/<int:post_id>/', delete_post, name='delete-post'),
    path('edit_post/<int:post_id>/', edit_post, name='edit-post'),
    path('add_post/', add_post, name='add-post'),
    path('choose_post/<int:post_id>/', choose_post, name='choose-post'),
    path('add_comment/<int:post_id>/', add_comment, name='add-comment'),
    path('delete_comment/<int:comment_id>/<int:post_id>/', delete_comment, name='delete-comment'),
    path('edit_comment/<int:comment_id>/<int:post_id>/', edit_comment, name='edit-comment'),
    path('profil/', user_profile, name='user-profile'),
    path('comeback/', comeback, name='comeback'),
     path('toggle_like/<int:comment_id>/', toggle_like, name='toggle-like'),
]
