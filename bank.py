import sqlite3
from flask import Flask,request,render_template,redirect
app=Flask(__name__)

def createtable():
    conn=sqlite3.connect("bank.db")
    cursor=conn.cursor()
    cursor.execute("""create table if not exists account(
                    id integer primary key autoincrement,
                    pin text,
                    balance integer
                    ) """)
    conn.commit()
    conn.close()
createtable()
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/create",methods=["POST"])
def createpin():
    pin=request.form["pin"]
    balance=request.form["balance"]
    conn=sqlite3.connect("bank.db")
    cursor=conn.cursor()
    cursor.execute("insert into account(pin,balance) values(?,?)",(pin,balance))
    conn.commit()
    conn.close()
    return "Pin created successfully"
   

@app.route("/checkbalance",methods=["POST"])
def checkbalance():
    pin=request.form["pin"]
    conn=sqlite3.connect("bank.db")
    cursor=conn.cursor()
    cursor.execute("select balance from account where pin=?",(pin,))
    data=cursor.fetchone()
    conn.close()
    if data:
        return f"your balance is{data[0]}"
    else:
        return "Incorrect pin"
        
@app.route("/withdraw",methods=["POST"])
def withdraw():
    pin=request.form["pin"]
    amount=int(request.form["amount"])
    conn=sqlite3.connect("bank.db")
    cursor=conn.cursor()
    cursor.execute("select balance from account where pin=?",(pin,))
    data=cursor.fetchone()
    if data[0]>=amount:
         newbalance=data[0]-amount
         cursor.execute("update account set balance=? where pin=?",(newbalance,pin))
         conn.commit()
         return f"Your available balance is{newbalance}"
    else:
         return "Invalid Pin"

@app.route("/deposite",methods=["POST"])
def deposite():
    pin=request.form["pin"]
    amount=int(request.form["amount"])
    conn=sqlite3.connect("bank.db")
    cursor=conn.cursor()
    cursor.execute("select balance from account where pin=?",(pin,))
    data=cursor.fetchone()
    if data:
         newbalance=data[0]+amount
         cursor.execute("update account set balance=? where pin=?",(newbalance,pin))
         conn.commit()
         return f"Amount credited:{newbalance}"
    else:
         return "Invalid Pin"
    

@app.route("/logout")
def logout():
    return render_template("index.html")
if __name__ == "__main__":
    app.run(debug=True)


       




    
        