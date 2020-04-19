from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.contrib import messages
from collections import namedtuple


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
                f"INSERT INTO `transactions`(`user_id`, `t_name`, `t_posted`) VALUES ('{from_u}','{detail}','{date}')")
            res.execute(
                f"INSERT INTO `transaction_u`(`u_id`, `amount`) VALUES ({to_u},{finalA})")
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
                f"select a.*, p.image from auth_user a , users_profile p where (a.id = p.user_id) and (a.id in (select u_id2 from friends where u_id1 = {c_user.id})) or (a.id in (select u_id1 from friends where u_id2={c_user.id}))")
            ans = dictfetchall(cursor)

            print(len(ans))

            # result.execute(
            #     f"Call get_tdata({c_user.id}, {ans[m].get('id')});")

            # resfrnd = dictfetchall(result)

            # print(resfrnd)
            # restransfrnd = dict()
            df1_data = []
            df2_data = []
            for i in range(len(ans)):
                try:
                    res = connection.cursor()
                    res.execute(
                        f"Call f_dl({c_user.id} , {ans[i].get('id')}) ;")

                    for row in res.fetchall():
                        # print(row[0])
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

            # print(idk)
                # for j in range(3):
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

  


def activityView(request):
    return render(request, 'blog/activity.html')


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


# select transactions.* , transaction_u.u_id , transaction_u.amount from transactions inner join transaction_u on transactions.t_id= transaction_u.t_id where (transactions.user_id='5' or transaction_u.u_id = '5') ORDER BY transactions.t_posted DESC
    #  AYA thi jovanu
    # column_names = [col[0] for col in res.description]

    # for row in res.fetchall():
    #     df1_data.append({name: row[k] for k, name in enumerate(column_names)})

    # res.nextset()
    # column_names = [col[0] for col in res.description] # Get column names from MySQL

    # for row in res.fetchall():
    #     df2_data.append({name: row[j] for j, name in enumerate(column_names)})



# @login_required
# def newTransaction(request):
#     c_user = request.user

#     if request.method == 'POST':
#         detail = request.POST.get('desc')
#         date = request.POST.get('date')
#         from_u = request.POST.get('paidby')
#         to_u = request.POST.get('topay')
#         amount = request.POST.get('amount')

#         print(detail, date, from_u, to_u, amount)
#         finalA = float(amount)/2
#         detail = detail.replace("'", "''")
#         print(detail, date, from_u, to_u, amount)
#         try:
#             cursor = connection.cursor()
#             res = connection.cursor()
#             cursor.execute(
#                 f"INSERT INTO `transactions`(`user_id`, `t_name`, `t_posted`) VALUES ('{from_u}','{detail}','{date}')")
#             res.execute(
#                 f"INSERT INTO `transaction_u`(`u_id`, `amount`) VALUES ({to_u},{finalA})"
#             )
#         finally:
#             cursor.close()
#             res.close()

#         messages.info(request, f'Added')
#     else:
#         try:
#             cursor = connection.cursor()
#             cursor.execute(
#                 f"select *from auth_user where (id in (select u_id2 from friends where u_id1 ={c_user.id})) or (id in (select u_id1 from friends where u_id2={c_user.id}))")
#             # f"SELECT * FROM auth_user where id in (SELECT u_id2 from friends where u_id1 = {c_user.id} or u_id2 = {c_user.id})")
#             ans = dictfetchall(cursor)
#         finally:
#             cursor.close()
#         context = {
#             'user': c_user,
#             'frnd': ans,
#         }
#         return render(request, 'blog/newtransaction.html', context)
#     return render(request, 'blog/home.html')
