from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = "abc"


@app.route('/registration')
def home():
    return render_template('register.html')


@app.route('/register',methods=['POST'])
def register():
    x = [x for x in request.form.values()]
    params = "name="+x[0]+"&email="+x[1]+"&contact="+x[2]+"&company="+x[3]+"&username="+x[4]+"&password="+x[5]
    check(x[1])
    return render_template('login.html')
    if('errorType' in check(x[1])):
       url = "https://iqyptn2cj6.execute-api.ap-south-1.amazonaws.com/registration?"+params
       response = requests.get(url)
       return render_template('registration.html', pred="Registration Successful, please login using your details")
    else:
       return render_template('login.html', pred="You are already a member, please login using your details")


def check(email):
    url = "https://c223spitlk.execute-api.ap-south-1.amazonaws.com/get_data?email="+email
    status = requests.request("GET",url)
    return status.json()



@app.route('/')    
@app.route('/login')
def login():
    return render_template('login.html')
    
@app.route('/loginpage',methods=['POST'])
def loginpage():
    x = [x for x in request.form.values()]
    email = x[0]
    passw = x[1]
    data = check(email)
    msg =  []
    if('errorType' in data):
        msg = [{"msg": "The username is not found, recheck the spelling or please register."}]
        return render_template('login.html', data = msg)
    else:
        if(passw==data['password']):
            return redirect(url_for('dashboard'))
        else:
            msg = [{"msg": "Login unsuccessful. You have entered the wrong password."}]
            return render_template('login.html', data = msg)
        
@app.route('/dashboard')
def dashboard():
    allItems = getAllItems()
    return render_template('dashboard.html', data = allItems)  

def getAllItems():
    url = "https://zn5ojrurg1.execute-api.ap-south-1.amazonaws.com/get_all_items"
    response = requests.request("GET",url)
    return response.json()


@app.route('/Myaccount')
def Myaccount():
    return render_template('Myaccount.html')  


@app.route('/Contactus')
def Contactus():
    return render_template('index.html')  
    
@app.route('/Inventory')
def Inventory():
    allItems = getAllItems()
    return render_template('inventory.html', data = allItems)  

@app.route('/updateInventory',methods=['POST'])
def updateInventory():
    print("updateInventory")
    x = [x for x in request.form.values()]
    print(x)
    status = updateInDDB(x)
    print(status)
    if('errorType' in status):
        flash('Item already exists in inventory!')
        return redirect(url_for('Inventory'))
    
    return redirect(url_for('dashboard'))


def updateInDDB(params):
    if(params[0] == "delete"):
        url = "https://jm89mdmo05.execute-api.ap-south-1.amazonaws.com/updateItems?operation="+ params[0] + "&itemName=" + params[1] 
    else:
        url = "https://jm89mdmo05.execute-api.ap-south-1.amazonaws.com/updateItems?operation="+ params[0] + "&itemName=" + params[1] + "&price=" + params[2] + "&quantity=" + params[3]
    status = requests.request("GET",url)
    print("\nUpdated quantity")
    return status.json()

         
@app.route('/Signout')
def Signout():
    return render_template('MODERN abstract shapes and plants (311841) _ Illustrations _ Design Bundles.png')  

@app.route('/successPage')
def successPage():
    return render_template('successPage.html')  

   

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

