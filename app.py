from flask import Flask,render_template,request,redirect,url_for
import random
import os
app=Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        with open("user.txt","r") as f:
            alluser=f.read().split("\n")
            for user in range(len(alluser)):
                if alluser[user]!="":
                    username=alluser[user].split("????")[0]
                    password=alluser[user].split("????")[1]
                    if(username==request.form["username"] and password==request.form["password"]):
                        with open("id.txt","r") as ids:
                            userid=ids.read().split("\n")[user]
                        return redirect("/userhome/"+userid)
            return redirect(url_for("login"))
    else:
        return render_template("login.html")


@app.route("/adduser",methods=["GET","POST"])
def adduser():
    if request.method=="POST":
        with open("user.txt","a") as f:
            f.write(request.form["username"]+"????"+request.form["password"]+"\n")
        strs="0123456789QWERTYUIOPLKJHGFDSAZXCVBNM"
        flag=0
        with open("id.txt","r") as ids:
            oldids=ids.read().split("\n")
        with open("id.txt","a") as ids:
            while(flag==0):
                flag=1
                newid=""
                for i in range(15):
                    newid=newid+strs[random.randint(0,len(strs)-1)]
                for oldid in oldids:
                    if newid==oldid:
                        flag=0
                        break
            ids.write(newid+"\n")
        return "adduser is ok"
    else:
        return render_template("adduser.html")

@app.route("/userhome/<userid>")
def userhome(userid):
    with open("id.txt","r") as ids:
        theids=ids.read().split("\n")
        for i in range(len(theids)):
            if(theids[i]==userid):
                with open("user.txt","r") as users:
                    username=users.read().split("\n")[i].split("????")[0]
                return render_template("userhome.html",username=username,userid=userid)

@app.route("/diarys/<userid>")
def diarys(userid):
    try:
        diarysnum=0
        while(1):
            diarysnum=diarysnum+1
            with open(userid+"&&&"+str(diarysnum)+".txt","r"):
                pass
    except:
        diarysnum=diarysnum-1
    return render_template("diarys.html",userid=userid,diarysnum=diarysnum)

@app.route("/readdiary/<userid>/<diaryid>")
def readdiarys(userid,diaryid):
    with open(userid+"&&&"+diaryid+".txt","r") as diary:
        return diary.read()

@app.route("/deldiary/<userid>",methods=["GET","POST"])
def deldiarys(userid):
    if(request.method=="POST"):
        try:
            diarysnum=0
            while(1):
                diarysnum=diarysnum+1
                with open(userid+"&&&"+str(diarysnum)+".txt","r"):
                    pass
        except:
            diarysnum=diarysnum-1
        os.remove(userid+"&&&"+request.form["diaryid"]+".txt")
        for i in range(int(request.form["diaryid"]),diarysnum):
            os.rename(userid+"&&&"+str(i+1)+".txt",userid+"&&&"+str(i)+".txt")
        return redirect("/diarys/"+userid)
    else:
        return render_template("deldiary.html",userid=userid)

@app.route("/newdiary/<userid>",methods=["GET","POST"])
def newdiary(userid):
    if request.method=="POST":
        try:
            diarysnum=0
            while(1):
                diarysnum=diarysnum+1
                with open(userid+"&&&"+str(diarysnum)+".txt","r"):
                    pass
        except:
            diarysnum=diarysnum-1
        with open(userid+"&&&"+str(diarysnum+1)+".txt","w") as new:
            new.write(request.form["text"])
        return redirect("/diarys/"+userid)
    else:
        return render_template("newdiary.html",userid=userid)

if __name__=="__main__":
    app.run(host="0.0.0.0",port=80)