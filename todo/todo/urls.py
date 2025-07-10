from django.contrib import admin
from django.urls import path
from app.views import home_view, signup_view, login_view, todo_view, delete_todo_view, edit_todo_view, logout_view 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view),
    path('signup/', signup_view, name="signup"),
    path('login/', login_view, name="login"),
    path('todopage', todo_view, name="todopage"),
    path('delete_todo/<int:srno>', delete_todo_view, name='delete_todo'),
    path('edit_todo/<int:srno>', edit_todo_view, name='edit_todo'),
    path('logout/', logout_view, name="logout"),
]
