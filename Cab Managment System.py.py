import sqlite3
conn=sqlite3.connect("cabsbooking.db")
c=conn.cursor()
global dealerid
global adminid
global userid
def dealerreg():
    cab_dealername=input("Enter The Name:")
    cab_dealerusername=input("Enter theṇ username:")
    cab_dealerpassword=input("Enter The Password:")
    cab_dealeremail=input("Enter The email:")
    cab_dealerphone=input("Enter The Phone Number:")
    t1=(cab_dealername,cab_dealerusername,cab_dealerpassword,cab_dealeremail,cab_dealerphone)
    t1=tuple(t1)

    ins=f"INSERT INTO cab_dealers (cab_dealername,cab_dealerusername,cab_dealerpassword,cab_dealeremail,cab_dealerphone) VALUES {t1}"
    c.execute(ins)
    conn.commit()
    init()
def userreg():
    user_name=input("Enter the name:")
    user_username=input("Enter your user name:")
    user_password=input("Enter the pasword")
    user_email=input("Enter the email:")
    user_phone=input("Enter your phone number")
    t2=(user_name,user_username,user_password,user_email,user_phone)
    data=c.execute(f"SELECT * FROM users WHERE user_email='{user_email}'")
    if len(data.fetchall())==0:
        ins=f"INSERT INTO users (user_name,user_username,user_password,user_email,user_phone) VALUES {t2}"
        c.execute(ins)
        conn.commit()
        print("User registered successfully")
    else:
        print("User already exists,goodbye")
    init()
try:
    c.execute("""
        CREATE TABLE admin
        (admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
        admin_username VARCHAR(20) NOT NULL,
        admin_password VARCHAR(20) NOT NULL)""")
    c.execute("""CREATE TABLE cab_dealers
    (cab_dealerid INTEGER PRIMARY KEY AUTOINCREMENT,
     cab_dealername VARCHAR(20) NOT NULL,
     cab_dealerusername VARCHAR(20) NOT NULL,
     cab_dealerpassword VARCHAR(20) NOT NULL,
     cab_dealeremail VARCHAR(20) NOT NULL,
     cab_dealerphone VARCHAR(20) NOT NULL)
     """)
    c.execute("""CREATE TABLE cabs
        (cab_id INTEGER PRIMARY KEY AUTOINCREMENT,
        cab_name VARCHAR(20) NOT NULL,
        cab_type VARCHAR(20) NOT NULL,
        cab_model VARCHAR(20) NOT NULL,
        cab_dealerid INT(11) NOT NULL,
        cab_from VARCHAR(20) NOT NULL,
        cab_to VARCHAR(20) NOT NULL,
        cab_number VARCHAR(20) NOT NULL)""")
    c.execute("""CREATE TABLE users
        (user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name VARCHAR(20) NOT NULL,
        user_username VARCHAR(20) NOT NULL,
        user_password VARCHAR(20) NOT NULL,
        user_email VARCHAR(20) NOT NULL,
        user_phone INT(10) NOT NULL)""")
    print("Table created")
except:
    print("Some Error")

def dealer_login():
    try:
        global dealerid
        cab_dealerusername=input("Enter the username:")
        cab_dealerpassword=input("Enter The Password:")
        data=c.execute("SELECT * FROM cab_dealers WHERE cab_dealerusername='"+cab_dealerusername+"' and cab_dealerpassword='"+cab_dealerpassword+"'")
        d=data.fetchall()
        print(d)
        dealerid=d[0][0]
        t=len(str(dealerid))
        if  t>0:
            print("Login Succesfully")
            indealer()
        else:
            print("Invalid Username and password")
            dealer_login()
    except Exception as e:
         print(e)
         print("Some Error Occured,try once again")
         dealer_login()
def indealer():
        global dealerid
        print("1-Add Cab\n 2-View Cab\n 3-Delete Cab\n 4-Update Cab\n 5-Logout")
        dc=int(input("Enter the dealer option\n"))   
        if dc==1:
            add_cab()
        elif dc==2:
            displaycab()
        elif dc==3:
            delcab()
        elif dc==4:
            updatecab()
        elif dc==5:
            del dealerid
            init()
def add_cab():
    global dealerid
    cab_name=input("Enter the cab name:")
    cab_type=input("Enter the cab type:")
    cab_model=input("Enter the cab model:")
    cab_dealerid=dealerid
    print(dealerid)
    cab_from=input("From where does this cab start its journey?")
    cab_to=input("Where will it go?")
    cab_number=input("Enter the cab number")
    ins="INSERT INTO cabs(cab_name,cab_type,cab_model,cab_dealerid,cab_from,cab_to,cab_number)VALUES('"+cab_name+"','"+cab_type+"','"+cab_model+"','"+str(cab_dealerid)+"','"+cab_from+"','"+cab_to+"','"+cab_number+"')"
    c.execute(ins)
    conn.commit()
    print("Cab Created")
    indealer()
def delcab():
    global dealerid
    cabid=input("Enter you cab id please")
    del1="DELETE FROM cabs WHERE cab_id='"+cabid+"' and cab_dealerid='"+str(dealerid)+"' "
    c.execute(del1)
    conn.commit()
    print("Data deleted")
    displaycab()

def delcabbyadmin():
    cabid=input("Enter the cab id please")
    del1="DELETE FROM cabs WHERE cab_id='"+cabid+"'"
    c.execute(del1)
    conn.commit()
    print("Cab deleted")
    inadmin()
def updatecab():
    global dealerid
    cab_id=int(input("Enter your cab id:"))
    cab_name=input("Enter your cab name:")
    cab_type=input("Enter your cab type")
    cab_model=input("Enter your cab model:")
    cab_dealerid=dealerid
    cab_from=input("From where does this cab start its journey?")
    cab_to=input("Where will it go?")
    cab_number=input("Enter the cab number")
    upd="Update cabs set cab_name='"+cab_name+"',cab_type='"+cab_type+"'cab_model='"+cab_model+"',cab_from='"+cab_from+"',cab_to='"+cab_to+"',cab_number='"+cab_number+"' where cab_id='"+str(cab_id)+"'"
    c.execute(upd)
    conn.commit()
    print('Cabs data updated')
    indealer()


def displaycab():
    global dealerid
    data="SELECT c.cab_id,c.cab_name,c.cab_type,c.cab_model,d.cab_dealername,c.cab_from,c.cab_to,c.cab_number from cabs as c inner join cab_dealers as d on c.cab_dealerid=d.cab_dealerid WHERE c.cab_dealerid='"+str(dealerid)+"'"
    cabdata=c.execute(data)
    finalcabdata=c.fetchall()
    print("{0:15}{1:15}{2:15}{3:15}{4:20}{5:15}{6:15}{7:15}".format("Cab Id","Cab Name","Cab Type","Cab Model","Cab Dealer Name","Cab From","Cab To","cab Number"))
    for d in finalcabdata:
        print("{0:<15}{1:<15}{2:<15}{3:<15}{4:<20}{5:<15}{6:<15}{7:<15}".format(d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7]))
    indealer()



def displaycabuser(cab_from='',cab_to=''):
    global dealerid
    if cab_from!="" and cab_to!='':
        data="SELECT c.cab_id,c.cab_name,c.cab_type,c.cab_model,d.cab_dealername,c.cab_from,c.cab_to,c.cab_number from cabs as c inner join cab_dealers as d on c.cab_dealerid=d.cab_dealerid WHERE cab_from='"+cab_from+"' and cab_to='"+cab_to+"'"
    else:
        data="SELECT c.cab_id,c.cab_name,c.cab_type,c.cab_model,d.cab_dealername,c.cab_from,c.cab_to,c.cab_number from cabs as c inner join cab_dealers as d on c.cab_dealerid=d.cab_dealerid"
    cabdata=c.execute(data)
    finalcabdata=c.fetchall()
    print("{0:15}{1:15}{2:15}{3:15}{4:20}{5:15}{6:15}{7:15}".format("Cab Id","Cab Name","Cab Type","Cab Model","Cab Dealer Name","Cab From","Cab To","cab Number"))
    for d in finalcabdata:
        print("{0:<15}{1:<15}{2:<15}{3:<15}{4:<20}{5:<15}{6:<15}{7:<15}".format(d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7]))
    inuser()

def displaycabsbyadmin(cab_from='',cab_to=''):
    global dealerid
    if cab_from!="" and cab_to!='':
        data="SELECT c.cab_id,c.cab_name,c.cab_type,c.cab_model,d.cab_dealername,c.cab_from,c.cab_to,c.cab_number from cabs as c inner join cab_dealers as d on c.cab_dealerid=d.cab_dealerid WHERE cab_from='"+cab_from+"' and cab_to='"+cab_to+"'"
    else:
        data="SELECT c.cab_id,c.cab_name,c.cab_type,c.cab_model,d.cab_dealername,c.cab_from,c.cab_to,c.cab_number from cabs as c inner join cab_dealers as d on c.cab_dealerid=d.cab_dealerid"
    cabdata=c.execute(data)
    finalcabdata=c.fetchall()
    print("{0:15}{1:15}{2:15}{3:15}{4:20}{5:15}{6:15}{7:15}".format("Cab Id","Cab Name","Cab Type","Cab Model","Cab Dealer Name","Cab From","Cab To","cab Number"))
    for d in finalcabdata:
        print("{0:<15}{1:<15}{2:<15}{3:<15}{4:<20}{5:<15}{6:<15}{7:<15}".format(d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7]))
    d=int(input("Emter 1 to go back\nEnter 2 to delete a cab\n"))
    if d==1:
        inadmin()
    elif d==2:
        delcabbyadmin()
        inadmin()
def changepass():
    try:
        global userid
        old=input("PLease enter the old password:")
        data=c.execute("SELECT * FROM users WHERE user_password='"+old+"' and user_id='"+str(userid)+"'" )
        d=data.fetchall()
        t=len(d)
        if t==1:
            newpass=input("Enter the new password:")
            cpass=input("Enter the confirmed password:")
            if(newpass==cpass):
                upd="update users set user_password='"+newpass+"' WHERE user_id ='"+str(userid)+"'"
                c.execute(upd)
                conn.commit()
                print("Password updated....")
                inuser()
            else:
                print("New password and confirm password are not matching!...")
                inuser()
        else:
            print("Invalid old password")
            inuser()
    except Exception as e:
        print(e)


def userupdate():
    global userid
    user_email=input("Enter the new Email:")
    user_phone=input("Enter the new phone:")
    upd="Update users set user_email='"+user_email+"',user_phone='"+user_email+"' WHERE user_id='"+str(userid)+"'" 
    c.execute(upd)
    conn.commit()
    print("Information Updated")
    inuser()

def inuser():
    global userid
    print("1 View all cabs\n 2 Search cabs\n 3 Update Profile\n 4 Change Password\n 5 Logout")
    userc=int(input("Enter your choice"))
    if userc==1:
        displaycabuser()
    elif userc==2:
        cab_from=input("Enter your picking point")
        cab_to=input("Enter your drop point")
        displaycabuser(cab_from,cab_to)
    elif userc==3:
        userupdate()
    elif userc==4:
        changepass()
    elif userc==5:
        del userid
        init()



def userlogin():
    global userid
    user_username=input("Enter user name:")
    user_password=input("Enter user password:")
    data=c.execute("SELECT * FROM users WHERE user_username='"+user_username+"' and user_password='"+user_password+"'")
    d=data.fetchall()
    userid=d[0][0]
    t=len(str(userid))
    if(t==1):
        print("Login Sucesfully")
        inuser()
    else:
        print("Invalid username and password")
        userlogin()

def adminlogin():
    global adminid
    admin_username=input("Enter admin username:")
    admin_password=input("Enter admin password:")
    data=c.execute("SELECT * FROM admin WHERE admin_username='"+admin_username+"' and admin_password='"+admin_password+"'")
    d=data.fetchall()
    adminid=d[0][0]
    t=len(str(adminid))
    if(t==1):
        print("Login Sucesfully")
        inadmin()
    else:
        print("Invalid username and password")
        adminlogin()



def adminchangepass():
    try:
        global adminid
        old=input("PLease enter the old password:")
        data=c.execute("SELECT * FROM admin WHERE admin_password='"+old+"' and admin_id='"+str(adminid)+"'" )
        d=data.fetchall()
        t=len(d)
        if t==1:
            newpass=input("Enter the new password:")
            cpass=input("Enter the confirmed password:")
            if(newpass==cpass):
                upd="update admin set admin_password='"+newpass+"' WHERE admin_id ='"+str(adminid)+"'"
                c.execute(upd)
                conn.commit()
                print("Password updated....")
                inadmin()
            else:
                print("New password and confirm password are not matching!...")
                inadmin()
        else:
            print("Invalid old password")
            inadmin()
    except Exception as e:
        print(e)

def inadmin():
    global adminid
    print("\n1-View All Users\n 2-View All Dealers \n 3-View Cabs \n 4-Change Password \n 5-Logout")
    adminc=int(input("Enter your choice:"))
    if adminc==1:
        displayuser()
    elif adminc==2:
        displaydealer()
    elif adminc==3:
        displaycabsbyadmin()
    elif adminc==4:
        adminchangepass()
    elif adminc==5:
        del adminid
        init()

def displayuser():
    global userid
    try:
        print("{0:^15}{1:^15}{2:^30}{3:^20}".format("User Id","User Name","User Email","User Phone"))
        data="SELECT * From users"
        alldata=c.execute(data)
        fetch=alldata.fetchall()
        for d in fetch:
            print("{0:^15}{1:^15}{2:^30}{3:^20}".format(d[0],d[1],d[3],d[4]))
        adminc=int(input("Enter 1 to go back\nEnter 2 to go delete users"))
        if adminc==1:
            inadmin()
        elif adminc==2:
            userid=int(input("Send us the userid"))
            deldata="Delete from users where user_id='"+str(userid)+"'"
            c.execute(deldata)
            conn.commit()
            print("User deleted...")
            inadmin()
    except Exception as e:
        print(e)

def displaydealer():
    global dealerid
    try:
        print("{0:^15}{1:^15}{2:^30}{3:^20}".format("Dealer Id","Dealer Name","Dealer Email","Dealer Phone"))
        data="SELECT * From cab_dealers"
        alldata=c.execute(data)
        fetch=alldata.fetchall()
        for d in fetch:
            print("{0:^15}{1:^15}{2:^30}{3:^20}".format(d[0],d[1],d[3],d[4]))
        adminc=int(input("Enter 1 to go back\nEnter 2 to go delete users"))
        if adminc==1:
            inadmin()
        elif adminc==2:
            dealerid=int(input("Send us the Dealer id"))
            deldata="Delete from cab_dealers where dealer_id_id='"+str(dealerid)+"'"
            c.execute(deldata)
            conn.commit()
            print("User deleted...")
            inadmin()
    except Exception as e:
        print(e)


def init():
    print('1 Dealer Registration \n 2 Dealer Login \n 3 User Registration \n 4 User Login \n 5 Admin Login \n 6 Exit')
    userc=int(input("Enter The Choice\n"))
    if userc==1:
        dealerreg()
    elif userc==2:
        dealer_login()
    elif userc==3:
        userreg()
    elif userc==4:
        userlogin()
    elif userc==5:
        adminlogin()
    else:
        exit()
init()
