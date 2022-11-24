import sqlite3

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/index')
def home():
    #return render_template("index.html")
    return index()

# @app.route('/user/<name>')
# def hello_user(name):
#     return render_template('index.html',name = name)

@app.route('/score')
def score():
    # score = []  # 评分
    # num = []    # 每个评分所统计出的电影数量
    # score2 = []  # 评分
    # num2 = []  # 每个评分所统计出的电影数量
    # res={}
    # con = sqlite3.connect("movie.db")
    # cur = con.cursor()
    # sql = "select score,count(score) from movie250 group by score"
    # data = cur.execute(sql)
    # for item in data:
    #     score.append(str(item[0]))
    #     num.append(item[1])
    # for k, v in zip(score, num):
    #     res.update({k: v, },)
    #
    # sql2="select year_release,count(year_release) from movie250 group by year_release"
    # data2 = cur.execute(sql2)
    # for item2 in data2:
    #     score2.append(str(item2[0]))
    #     num2.append(item2[1])
    #
    # #print(num2)
    # cur.close()
    # con.close()
    # return render_template("score.html",score=score,num=num,res=res,num2=num2,score2=score2)
    # return render_template("testshanxing.html",score=score,num=num,res=res,num2=num2,score2=score2)
    return render_template("socre.html")


if __name__ == '__main__':
    """初始化,debug=True"""
    # app.run(host='127.0.0.1', port= 5000, debug=True)
    app.run()