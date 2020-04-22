from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.contrib import messages
from collections import namedtuple
from .forms import MyForm 
 

def home(request):
    c_user = request.user
    context = {
        'user': c_user
    }
    return render(request, 'blog/home.html', context)


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


@login_required
def newTransaction(request):
    c_user = request.user

    if request.method == 'POST':
        detail = request.POST.get('desc')
        date = request.POST.get('date')
        from_u = request.POST.get('paidby')
        to_u = request.POST.get('topay') 
        amount = request.POST.get('amount')
        poffriend1 = request.POST.get('friend1')
        poffriend2 = request.POST.get('friend2')
            
        print(detail , date , from_u , to_u, amount,poffriend1,poffriend2)
       
        sum1 = poffriend1 + poffriend2    
        
        if (poffriend1 != None and poffriend2 != None  ):
            if (sum1 == 100):        
               splitamount = (float(amount)*float(poffriend1))/100
               netamount= float(amount) - splitamount
               finalA = netamount
            else:
               finalA = float(amount)/2       
        else:
            finalA = float(amount)/2
        detail = detail.replace("'" , "''")
        
        try:
            cursor = connection.cursor()
            res = connection.cursor()
            cursor.execute(
                f"call addexpense({from_u} ,'{detail}','{date}')")
            rid = dictfetchall(cursor)    
            rid = rid[0]["rid"]
            
            res.execute(
                f"INSERT INTO `transaction_u` VALUES ({rid},{to_u},{finalA})")
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

@login_required
def friendsView(request):
    c_user = request.user

    if request.method == 'GET':
        try:
            cursor = connection.cursor()
            result = connection.cursor()
            cursor.execute(
                f"select a.*, p.image from auth_user a inner join users_profile p on a.id = p.id where (a.id = p.user_id) and (a.id in (select u_id2 from friends where u_id1 = {c_user.id})) or (a.id in (select u_id1 from friends where u_id2= {c_user.id}))")
            ans = dictfetchall(cursor)

            print(len(ans))

            df1_data = []
            df2_data = []
            for i in range(len(ans)):
                try:
                    res = connection.cursor()
                    res.execute(
                        f"Call f_dl({c_user.id} , {ans[i].get('id')}) ;")

                    for row in res.fetchall():
                        # print(row[0])
                        # df1_data.append(row[0])
                        if row[0] is None:
                            df1_data.append('0')
                        else:
                            df1_data.append(row[0])

                    res.nextset()
                    for row in res.fetchall():
                        # print(row[0])
                        if row[0] is None:
                            df2_data.append('0')
                        else:
                            df2_data.append(row[0])

                finally:
                    res.close()

            tot = []
            for i in range(0, len(df1_data)):
                df1_data[i] = int(df1_data[i])
            print(df1_data)
            for i in range(0, len(df2_data)):
                df2_data[i] = int(df2_data[i])
            print(df2_data)

            for i in range(len(df1_data)):
                tot.append(df1_data[i]-df2_data[i])

            print(tot)

            context = {
                'frnd': ans,
                'levu': df1_data,
                'devu': df2_data,
                'total': tot,
            }

        finally:
            cursor.close()

        # messages.info(request, f'Added')

    return render(request, 'blog/friends.html', context)


def gettransdatafriend(request, f_id):
    c_user = request.user.id
    try:
        cursor = connection.cursor()
        cursor.execute(
            f"call get_tdata({c_user} , {f_id}) ")

        resultant = dictfetchall(cursor)

        # print(resultant)

    finally:
        cursor.close()

    context = {
        'c_user': c_user,
        'alldata': resultant,
    }

    return render(request, 'blog/friendshistory.html', context)


def updatefriend(request, t_id):
    c_user = request.user.id
    if request.method == 'POST':
        detail = request.POST.get('desc')
        date = request.POST.get('date')
        from_u = request.POST.get('paidby')
        to_u = request.POST.get('topay') 
        amount = request.POST.get('amount')
        poffriend1 = request.POST.get('friend1')
        poffriend2 = request.POST.get('friend2')
            
        print(detail , date , from_u , to_u, amount,poffriend1,poffriend2)
       
        sum1 = poffriend1 + poffriend2    
        
        if (poffriend1 != None and poffriend2 != None  ):
            if (sum1 == 100):        
               splitamount = (float(amount)*float(poffriend1))/100
               netamount= float(amount) - splitamount
               finalA = netamount
            else:
               finalA = float(amount)/2       
        else:
            finalA = float(amount)/2
        detail = detail.replace("'" , "''")
        
        # try:
        #     cursor = connection.cursor()
        #     res = connection.cursor()
        #     cursor.execute(
        #         f"INSERT INTO `transactions`(`user_id`, `t_name`, `t_posted`) VALUES ('{from_u}','{detail}','{date}')")
        #     res.execute(
        #         f"INSERT INTO `transaction_u`(`u_id`, `amount`) VALUES ({to_u},{finalA})")
        # finally:
        #     cursor.close()
        #     res.close()

        messages.info(request, f'Added')
    else:
        try:
            res = connection.cursor()
            cursor = connection.cursor()
            # cursor.execute(
            #     f"select t.user_id , t.t_name , t.t_posted , tu.u_id , tu.amount from transactions t inner join transaction_u tu on t.t_id = tu.t_id where tu.t_id = {t_id}")

            # resul = dictfetchall(cursor)

            res.execute(
                f"select *from auth_user where (id in (select u_id2 from friends where u_id1 ={c_user})) or (id in (select u_id1 from friends where u_id2={c_user}))")

            resu = dictfetchall(res)

            print(resu)

        finally:
            cursor.close()
            res.close()

        context = {
            'alldata': resu,
        }
        return render(request, 'blog/newtransaction.html', context)
    return render(request, 'blog/home.html')    

  
def deleteexpense(request , t_id):
    try:
        res = connection.cursor()
        res.execute(
           f"delete from transactions where transactions.t_id = {t_id};" )

    finally:
        res.close()
        
        messages.info(request, f'Expense deleted')
    return render(request, 'blog/home.html')

def activityView(request):
    c_user = request.user
    if request.method == 'GET':
        try:
            cursor = connection.cursor()
            cursor.execute(
                f"select activity.message,activity.at_time from activity where activity.userid={c_user.id} order by activity.a_id desc")
            ans = dictfetchall(cursor)
            print(ans)
        finally:
            cursor.close()    
        
        context={
            'active': ans,
        }
           
    return render(request, 'blog/activity.html',context)


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


def addnewgroup(request):
    c_user = request.user
    form = MyForm()
    if request.method=='POST':
        form = MyForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #now in the object cd, you have the form as a dictionary.
            name = cd.get('name')
            bio = cd.get('bio')
            
            print

            name = str(name)
            bio = str(bio)

            try:
                cursor = connection.cursor()
                cursor.execute(
                    f"INSERT INTO groups VALUES (Null,'{name}','{bio}',{c_user.id});"
                )
            finally:
                cursor.close()    
        return redirect('friends')
    else:
        return render(request, 'blog/newgroup.html' , {'form' : form})  

def addfriendsingroup(request,g_id):
    c_user = request.user
    some_var =[]
    if request.method == 'POST':
        some_var = request.POST.getlist('checks[]')
        
        for i in range(0, len(some_var)): 
            some_var[i] = int(some_var[i]) 

        print(some_var)
        try:
            cursor = connection.cursor()
            for i in range(len(some_var)):
                cursor.execute(
                    f"INSERT INTO `group_data`(`g_id`, `id`) VALUES ({g_id},{some_var[i]})"
                )
        finally:
                cursor.close()    
        return redirect('friends')
        # return render(request, 'blog/newgroup.html')
    else:
        try:
            cursor = connection.cursor()
            res = connection.cursor()            
            cursor.execute(
                f"call getgroupfriend({c_user.id} , {g_id})")
            ans = dictfetchall(cursor)

            res.execute(
                f"select * from auth_user a where id in (select g.id from group_data g where g.g_id = {g_id} and not g.id = {c_user.id})")
            result = dictfetchall(res)
            print(result)
        finally:
            cursor.close()
        context = {
            'user' : c_user,
            'frnd' : ans,
            'g_id' : g_id,
            'alldata' : result
        }    
        return render(request, 'blog/newgroupcreated.html' ,context)
    return render(request, 'blog/home.html')


def removefriends(request,u_id):
    try:
        res = connection.cursor()
        res.execute(
           f"delete from group_data where id = {u_id};")

    finally:
        res.close()
        
        messages.info(request, f'User removed from group.!!')

    return redirect('friends')  


def showgroups(request):
    c_user = request.user

    if request.method == 'GET':
        try:
            cursor = connection.cursor()
            result = connection.cursor()
            cursor.execute(
                f"call getgroups({c_user.id})")
            ans = dictfetchall(cursor)

            print(ans)

            context ={
                'grup':ans,
            }

        finally:
            cursor.close()

        # messages.info(request, f'Added')

    return render(request, 'blog/groups.html', context)

def newgroupTransaction(request,g_id):
    c_user = request.user

    if request.method == 'POST':
        detail = request.POST.get('desc')
        date = request.POST.get('date')
        from_u = request.POST.get('paidby')
        amount = request.POST.get('amount')
        some_var = request.POST.getlist('checks[]')
        poffriend1 = request.POST.get('friend1')
        poffriend2 = request.POST.get('friend2')
            
        sum1 = poffriend1 + poffriend2    
        
        if (poffriend1 != None and poffriend2 != None  ):
            if (sum1 == 100):        
               splitamount = (float(amount)*float(poffriend1))/100
               netamount= float(amount) - splitamount
               finalA = netamount
            else:
               finalA = float(amount)/(len(some_var)+1)    
        else:
            finalA = float(amount)/(len(some_var)+1)

        print(detail , date , from_u , amount, finalA)    
        
        for i in range(0, len(some_var)): 
            some_var[i] = int(some_var[i]) 

        print(some_var)

        detail = detail.replace("'" , "''")
        
        try:
            cursor = connection.cursor()
            res = connection.cursor()
            cur = connection.cursor()
            cursor.execute(
                f"call addgroupexpense({from_u} ,'{detail}','{date}',{g_id})")
            rid = dictfetchall(cursor)    
            rid = rid[0]["rid"]
            print(rid)
                # f"INSERT INTO `transactions`(`user_id`, `t_name`, `t_posted`) VALUES ('{from_u}','{detail}','{date}')")
            for i in some_var:
                res.execute(
                    f"INSERT INTO `transaction_u` VALUES ({rid} ,{i},{finalA})")
              
        finally:
            cursor.close()
            res.close()

        messages.info(request, f'Added')
    else:
        try:
            cursor = connection.cursor()
            cursor.execute(
                f"select a.* from auth_user a inner JOIN group_data g on a.id = g.id where g.g_id ={g_id}")
            ans = dictfetchall(cursor)
        finally:
            cursor.close()
        context = {
            'g_id' : g_id,
            'user' : c_user,
            'frnd' : ans,
        }    
        return render(request, 'blog/newgtransaction.html' ,context)
    return redirect('friends')

def gettransdatagroup(request , g_id):
    c_user = request.user.id
    try:
        cursor = connection.cursor()
        cursor.execute(
            f"call getgroupexpense({g_id});")

        resultant = dictfetchall(cursor)

        # print(resultant)

    finally:
        cursor.close()

    context = {
        'c_user': c_user,
        'alldata': resultant,
    }

    return render(request, 'blog/seetransaction.html', context)