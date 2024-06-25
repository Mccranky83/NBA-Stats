from pyecharts import options as opts
from pyecharts.charts import Radar
from pyecharts.charts import Page, Radar
import pyecharts.options as opts
from pyecharts.charts import Timeline, Bar, Pie, Grid
from pyecharts.globals import ThemeType
from pyecharts.components import Image
import pandas as pd
import mysql.connector
from mysql.connector import Error
from pyecharts.commons.utils import JsCode
from bs4 import BeautifulSoup
import requests
from pyecharts.charts import Grid
from pyecharts.charts import Page

connection = mysql.connector.connect(
    host="192.168.43.100",
    user="root",
    password="123456",
    database="NBA_database"
)


cursor = connection.cursor()

cursor.execute("SHOW TABLES")
tables = cursor.fetchall()
#print(tables[0])
table_content={}
for (table_name,) in tables:
    cursor.execute(f"SELECT * FROM `{table_name}`")
    rows = cursor.fetchall()
    table_content[table_name] = rows

cursor.close()
connection.close()

maxn = 0
minn = 9999
ans1 = {}

for i in table_content:
    #print(table_content[i][0][4])
    s = str(i)
    ss = s[:4]
    #print(s[:4])
    if maxn < int(ss):
        maxn = int(ss)
    if minn > int(ss):
        minn = int(ss)
    sss = int(ss)

    if sss not in ans1:
        ans1[sss] = {"球队": [],
                    "胜率": [],
                    "均得分": [],
                    "均失分": [],
                    "胜场": []
                    }
    if table_content[i][0][1] == "Oklahoma City Thunder":
        ans1[sss]["球队"].append("雷霆")
    else:
        ans1[sss]["球队"].append(table_content[i][0][1])
    ans1[sss]["胜率"].append(table_content[i][0][4])
    ans1[sss]["均得分"].append(table_content[i][0][8])
    ans1[sss]["均失分"].append(table_content[i][0][9])
    ans1[sss]["胜场"].append(table_content[i][0][2])

    
v1 = [[100,98.4,48,0.585]]
v2 = [[5000, 14000, 28000, 31000, 42000, 21000]]


def bar_base(year:int)->Bar:
    scores = [[0]*4 for _ in range(6)]
    for i in range(6):
        scores [i] =[[ans1[year]["均得分"][i],ans1[year]["均失分"][i],ans1[year]["胜场"][i],ans1[year]["胜率"][i]]]
    # scores [2] =ans1[year]["均失分"]
    # scores [0] =ans1[year]["胜场"]
    # scores [3] =ans1[year]["胜率"]
    #print (scores)
    Teams = ans1[year]["球队"]
    colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'brown', 'gray', 'black']  # 颜色列表
    print(ans1[year]["球队"][0])
    c = (
            Radar()
            
            .add_schema(
                schema=[
                    opts.RadarIndicatorItem(name="胜场", max_=150),
                    opts.RadarIndicatorItem(name="均得分", max_=150),
                    opts.RadarIndicatorItem(name="均失分", max_=150),
                    opts.RadarIndicatorItem(name="胜率", max_=1),

                ]
            )
            .add(
                series_name=ans1[year]["球队"][0],
                data=scores[0],
                linestyle_opts=opts.LineStyleOpts(color="#CD0000"),
            )
            .add(
                series_name=ans1[year]["球队"][1],
                data=scores[1],
                linestyle_opts=opts.LineStyleOpts(color="#00CD00"),
            )
            .add(
                series_name=ans1[year]["球队"][2],
                data=scores[2],
                linestyle_opts=opts.LineStyleOpts(color="#0000CD"),
            )
            .add(
                series_name=ans1[year]["球队"][3],
                data=scores[3],
                linestyle_opts=opts.LineStyleOpts(color="#CDCD00"),
            )
            .add(
                series_name=ans1[year]["球队"][4],
                data=scores[4],
                linestyle_opts=opts.LineStyleOpts(color="#CD00CD"),
            )
            .add(
                series_name=ans1[year]["球队"][5],
                data=scores[5],
                linestyle_opts=opts.LineStyleOpts(color="#00CDCD"),
            )

            
            
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
                legend_opts=opts.LegendOpts(selected_mode="multiple"),
                title_opts=opts.TitleOpts(title="球队能力统计"),
            )
            
        )
    
    # for i in range(len(scores[0])):
    #     print(f"{Teams} {year}")
    #     for j in range(len(scores)):
    #         s = [0]*4
    #         s[i] = scores[j][i]
    #         print(s)


    # for team,a in Teams,len(Teams):
    #     for i in range(0,4):
    #         s = [0]*4
    #         s[i] = scores[i][a]
    #     print(s)
    #     c.add(f'{team} {year}',s)  # 使用scores列表中的每四个值作为一个系列
        #c.add(f'{team} {year}',scores)#areastyle_opts=opts.AreaStyleOpts(opacity=, color=colors[i % len(colors)]))  # 使用颜色列表中的颜色
    # c.render(str(year) + "_radar.html")
    return c

def main():
    # page = Page(layout=Page.SimplePageLayout)
    # for year in range(minn, maxn+1):
    #     radar_chart = bar_base(year)
    #     page.add(radar_chart)
    # page.render("all_years_radar.html")
    timeline = Timeline()
    for i in range(2015, 2023):
        timeline.add(bar_base(year = i), "{}年".format(i))
    # timeline.add(bar_base(year = 2016), "{}年".format(2015))
    # timeline.add(bar_base(year = 2016), "{}年".format(2016))
    timeline.add_schema(is_auto_play=True, play_interval=2000)
    timeline.render("all_years_radar.html")

    with open("all_years_radar.html", "r", encoding="utf-8") as f:
        html_content=f.read()

    soup = BeautifulSoup(html_content, "html.parser")

    modify = soup.find("div", class_="chart-container")
    print(modify)
    modify["style"] = "width:1600px; height:900px;"

    with open("all_years_radar.html", "w", encoding="utf-8") as f:
        f.write(str(soup))

if __name__ == "__main__":
    main()


