from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
import requests
import pandas as pd
import numpy as np
from datetime import date
from datetime import timedelta

app = Flask(__name__)



# MONGO DB Connection
client = MongoClient("mongodb+srv://Shubham:Shubham123@cluster0.k8b4o.mongodb.net/Final_Project?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client.get_database('Final_Project')
records = db.Rates

# Dates for 2021 (Ref : https://www.w3resource.com/pandas/date_range.php)
y1 = '2021'
M1 = 12 # Month count
begin2021 = pd.date_range(y1, periods=M1, freq='MS').strftime("%Y-%m-%d")
end2021 = pd.date_range(y1, periods=M1, freq='M').strftime("%Y-%m-%d")
begin2021 = begin2021.tolist()
end2021 = end2021.tolist()

# Dates for 2022
y2 = '2022'
M2 = 3 # Month count
begin2022 = pd.date_range(y2, periods=4, freq='MS').strftime("%Y-%m-%d")
end2022 = pd.date_range(y2, periods=M2, freq='M').strftime("%Y-%m-%d")
begin2022 = begin2022.tolist()
end2022 = end2022.tolist()

today = date.today()
# Yesterday date
yesterday = today - timedelta(days = 1)
yes_str = yesterday.strftime("%Y-%m-%d")
yes_lst = list(yes_str.split(" "))

#Combining both lists
start_date = begin2021 + begin2022
end_date = end2021 + end2022 + yes_lst

lineChart_RUB = []
lineChart_USD = []
lineChart_CAD = []
lineChart_GBP = []
lineChart_INR = []
usd = []
rub = []
cad = []
inr = []
eur = []
gbp = []
aed = []
cny = []

symbols = 'USD,RUB,CAD,INR,EUR,GBP,AED,CNY'

res = {start_date[i]: end_date[i] for i in range(len(start_date))}  
#print(str(res))



for start, end in res.items():

    url = "https://api.exchangerate.host/fluctuation?start_date=" + start + "&end_date=" +  end + "&symbols=" + symbols + '&base=USD' + "&format=json"
    #print(url)
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        #print(data)
        
        #time.sleep(5)
        records.insert_one(data) #inserting data into MongoDB

        #Line Charts
        lineChart_RUB.append(data["rates"]["RUB"]["change"])
        lineChart_USD.append(data["rates"]["USD"]["change"])
        lineChart_CAD.append(data["rates"]["CAD"]["change"])
        lineChart_GBP.append(data["rates"]["GBP"]["change"])
        lineChart_INR.append(data["rates"]["INR"]["change"])

        #Bar Charts
        usd.append(data["rates"]["USD"]["start_rate"])
        cad.append(data["rates"]["CAD"]["start_rate"])
        inr.append(data["rates"]["INR"]["start_rate"])
        rub.append(data["rates"]["RUB"]["start_rate"])
        gbp.append(data["rates"]["GBP"]["start_rate"])
        eur.append(data["rates"]["EUR"]["start_rate"])
        aed.append(data["rates"]["AED"]["start_rate"])
        cny.append(data["rates"]["CNY"]["start_rate"])
    else:
        exit()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/lineChart1")
def lineChart1():
    months = ["Jan'21","Feb'21","Mar'21","Apr'21","May'21","Jun'21","Jul'21","Aug'21","Sep'21","Oct'21","Nov'21","Dec'21","Jan'22","Feb'22","Mar'22","Apr'22"]
    values = lineChart_RUB
    return render_template('lineChart1.html',labels = months, values = values)

@app.route("/lineChart2")
def lineChart2():
    months = ["Jan'21","Feb'21","Mar'21","Apr'21","May'21","Jun'21","Jul'21","Aug'21","Sep'21","Oct'21","Nov'21","Dec'21","Jan'22","Feb'22","Mar'22","Apr'22"]
    values = lineChart_CAD
    return render_template('lineChart2.html',labels = months, values = values)

@app.route("/lineChart3")
def lineChart3():
    months = ["Jan'21","Feb'21","Mar'21","Apr'21","May'21","Jun'21","Jul'21","Aug'21","Sep'21","Oct'21","Nov'21","Dec'21","Jan'22","Feb'22","Mar'22","Apr'22"]
    values = lineChart_INR
    return render_template('lineChart3.html',labels = months, values = values)

@app.route("/lineChart Multiple")
def lineChart_M():
    months = ["Jan'21","Feb'21","Mar'21","Apr'21","May'21","Jun'21","Jul'21","Aug'21","Sep'21","Oct'21","Nov'21","Dec'21","Jan'22","Feb'22","Mar'22","Apr'22"]
    values1 = lineChart_RUB
    values2 = lineChart_CAD
    values3 = lineChart_INR

    return render_template('lineChart Multiple.html',labels = months, values1 = values1, values2 = values2, values3 = values3)

Bar_Values = [np.average(usd), np.average(cad), np.average(aed), np.average(gbp),np.average(cny),np.average(eur)]
@app.route("/BarChart")
def BarChart():
    labels = ["USD", "CAD", "AED", "GBP", "CNY", "EUR"]
    values = Bar_Values
    return render_template('BarChart.html', labels=labels, values=values)


if __name__ == "__main__":
    app.debug = False
    app.run()
