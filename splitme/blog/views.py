from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.contrib import messages

def home(request):
    c_user = request.user
    context = {
        'user' : c_user
    }
    return render(request, 'blog/home.html' , context)

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

@login_required
def newTransaction(request):
    c_user = request.user

    if request.method == 'POST':
        detail = request.POST.get('desc')
        date = request.POST.get('date')
        from_u = request.POST.get('paidby')
        to_u = request.POST.get('topay')
        amount = request.POST.get('amount')
        
        print(detail , date , from_u , to_u, amount)
        finalA = float(amount)/2
        detail = detail.replace("'" , "''")
        print(detail , date , from_u , to_u, amount)
        try:
            cursor = connection.cursor()
            res = connection.cursor()
            cursor.execute(
                f"INSERT INTO `transactions`(`user_id`, `t_name`, `t_posted`) VALUES ('{from_u}','{detail}','{date}')")
            res.execute(
                f"INSERT INTO `transaction_u`(`u_id`, `amount`) VALUES ({to_u},{finalA})"
            )
        finally:
            cursor.close()
            res.close()

        messages.info(request, f'Added')
    else:
        try:
            cursor = connection.cursor()
            cursor.execute(
                f"select *from auth_user where (id in (select u_id2 from friends where u_id1 ={c_user.id})) or (id in (select u_id1 from friends where u_id2={c_user.id}))")
                # f"SELECT * FROM auth_user where id in (SELECT u_id2 from friends where u_id1 = {c_user.id} or u_id2 = {c_user.id})")
            ans = dictfetchall(cursor)
        finally:
            cursor.close()
        context = {
            'user' : c_user,
            'frnd' : ans,
        }    
        return render(request, 'blog/newtransaction.html' ,context)
    return render(request, 'blog/home.html')


def activityView(request):


    return render(request , 'blog/activity.html')



def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

    
# select transactions.* , transaction_u.u_id , transaction_u.amount from transactions inner join transaction_u on transactions.t_id= transaction_u.t_id where (transactions.user_id='5' or transaction_u.u_id = '5') ORDER BY transactions.t_posted DESC
