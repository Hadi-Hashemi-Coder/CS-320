# project: p4
# submitter: mhashemineja
# partner: none
# hours: 15
import pandas as pd
from flask import Flask, request, Response, jsonify
import re
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from io import BytesIO


app = Flask(__name__)
#Data comes from a company called Statsbomb that supplies soccer data to clubs, betting companies, and media. I hope I get a job there.
#Open source Github page for their talent recruitment: https://github.com/statsbomb/open-data
#main.csv is competition data. It is parsed in a seperate file and copied over to here.
df = pd.read_csv("main.csv")

n = 0
visits = [0,0]
@app.route('/')
def home():
    global n
    global visits
    n += 1
    if n <= 10:
        if (n % 2) == 0:
            with open("index.html") as f:
                html = f.read()
                html = html.replace("donate.html","donate.html?from=A")
            return html
        else:
            with open("index.html") as f:
                html = f.read()
                html = html.replace("Donate here","Please consider donating")
                html = html.replace("donate.html","donate.html?from=B")
            return html
    else:
        if visits[0] >= visits[1]:
            print("Choose A")
            print(visits)
            with open("index.html") as f:
                html = f.read()
            return html
        else:
            print("Choose B")
            print(visits)
            with open("index.html") as f:
                html = f.read()
                html = html.replace("Donate here","Please consider donating")
            return html

@app.route('/browse.html')
def browse():
    return """
    <h1>Competition Data</h1>
    {}
    """.format(pd.DataFrame.to_html(df))

@app.route('/email', methods=["POST"])
def email():
    email = str(request.data, "utf-8")
    if re.match(r"[\d\w]*@[\d\w]*\..*", email): # 1
        with open("emails.txt", "a") as f: # open file in append mode
            f.write(email + "\n") # 2
            n = number_of_n() + 1
        return jsonify(f"thanks, you're subscriber number {n}!")
    return jsonify("Your email is not valid, please try again. If you don't, the owner of this website will be unhappy.") # 3

@app.route('/donate.html?from=A')
def donate_A():
    global visits
    visits[0] += 1
    with open("donate.html") as f:
        html = f.read()
    return html

@app.route('/donate.html?from=B')
def donate_B():
    global visits
    visits[1] += 1
    with open("donate.html") as f:
        html = f.read()
    return html

@app.route('/donate.html')
def donate():
    with open("donate.html") as f:
        html = f.read()
    return html

@app.route('/robots.txt')
def robo():
    return Response("\n".join(["User-Agent: hungrycaterpillar", "Disallow: /browse", "User-Agent: busyspider", "Disallow: /"]),
                    headers={"Content-Type":"text/plain"})

@app.route("/country.svg")
def country():
    fig, ax = plt.subplots()
    ax.hist(df['country_name'])
    ax.set_xlabel("Country")
    ax.set_ylabel("Competitions in Country")
    fake_file = BytesIO()
    ax.get_figure().savefig(fake_file, format="svg", bbox_inches="tight")
    plt.close()
    return Response(fake_file.getvalue(),
                    headers={"Content-Type": "image/svg+xml"})

@app.route("/country.svg?country_international")
def country_international():
    fig, ax = plt.subplots()
    ax.hist(df["country_name"][df["competition_international"]])
    ax.set_xlabel("International datasets")
    ax.set_ylabel("Number of International Competitions")
    fake_file_3 = BytesIO()
    ax.get_figure().savefig(fake_file_3, format="svg", bbox_inches="tight")
    plt.close()
    return Response(fake_file_3.getvalue(),
                    headers={"Content-Type": "image/svg+xml"})

@app.route("/gender.svg")
def gender():
    fig, ax = plt.subplots()
    ax.hist(df['competition_gender'])
    ax.set_xlabel("international")
    ax.set_ylabel("number of datasets")
    fake_file_2 = BytesIO()
    ax.get_figure().savefig(fake_file_2, format = "svg", bbox_inches="tight")
    plt.close()
    return Response(fake_file_2.getvalue(),
                    headers={"Content-Type": "image/svg+xml"})

def number_of_n():
    n = 0
    with open("emails.txt", "r") as f:
        for _ in f:
            n += 1
        return n

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, threaded=False) # don't change this line!

# NOTE: app.run never returns (it runs for ever, unless you kill the process)
# Thus, don't define any functions after the app.run call, because it will
# never get that far.
