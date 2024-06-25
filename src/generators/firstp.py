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
    print(sss)
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

    

# 柱状图
def bar_base(year:int)->Bar:
    c = (
        Bar()
            
            .add_xaxis(xaxis_data = ans1[year]["球队"])
            .add_yaxis(series_name = "胜场",
                       y_axis = ans1[year]["胜场"],
                       label_opts=opts.LabelOpts(is_show=True),
                       
                       
                       )
            .add_yaxis(series_name = "均得分",
                       y_axis = ans1[year]["均得分"],
                       label_opts=opts.LabelOpts(is_show=True),
                       
                       )
            .add_yaxis(series_name = "均失分",
                       y_axis = ans1[year]["均失分"],
                       label_opts=opts.LabelOpts(is_show=True),
                       
                       )

            
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="{}NBA六大地区第一球队数据对比图".format(year),subtitle="数据来自NBA-STAT"
                ),
                
                tooltip_opts=opts.TooltipOpts(
                    is_show=True, trigger="axis", axis_pointer_type="shadow"
                ),
                xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=25)),
                toolbox_opts=opts.ToolboxOpts(),
                legend_opts=opts.LegendOpts(is_show=False,),
                #legend_opts=opts.LegendOpts(is_show=False, type_="scroll", pos_left="left", orient="vertical"),
                yaxis_opts=opts.AxisOpts(
                    min_=0,
                    max_=250,),
                    
                graphic_opts=[
                    opts.GraphicImage(
                        graphic_item=opts.GraphicItem(
                            id_="background",
                            right=0,
                            top=0,
                            width=200,
                            height=200,
                            bounding="raw",
                            z=0,
                        ),
                    graphic_imagestyle_opts=opts.GraphicImageStyleOpts(
                        # image="https://ts1.cn.mm.bing.net/th/id/R-C.66d7b796377883a92aad65b283ef1f84?rik=sQ%2fKoYAcr%2bOwsw&riu=http%3a%2f%2fwww.quazero.com%2fuploads%2fallimg%2f140305%2f1-140305131415.jpg&ehk=Hxl%2fQ9pbEiuuybrGWTEPJOhvrFK9C3vyCcWicooXfNE%3d&risl=&pid=ImgRaw&r=0https://s1.ax1x.com/2020/08/09/aT5jH.png",
                        # image="https://www.sportspress.cn/webimages/2001/1-200121150959.jpg",
                        # image="https://gd-hbimg.huaban.com/24709244f79998ca773a4276d67b33d60745a93155334-8dJzAT_fw658https://pic4.zhimg.com/v2-8c43ceaaf5c5a7aec35b5846729b8d8c_r.jpg?source=1940ef5c",
                        #image="NN.jpg",
                        # image="https://img.tukuppt.com/ad_preview/00/06/34/5c98ed2eaa200.jpg!/fw/980",
                        width=2000,
                        height=1000,
                        opacity=0.8,
                    )
                ),
                ]
                #legend_opts=opts.LegendOpts(is_show=False, type_="scroll", pos_left="left", orient="vertical")
                #legend_opts=opts.LegendOpts(is_show=False),
            )
    )
    d = pie(y = year)
    return c.overlap(d)


def pie(y:int)->Pie:
    c = (
        Pie()
            .add(
                series_name="胜率比较",
                data_pair=[(ans1[y]["球队"][0], ans1[y]["胜率"][0]),
                           (ans1[y]["球队"][1], ans1[y]["胜率"][1]),
                           (ans1[y]["球队"][2], ans1[y]["胜率"][2]),
                           (ans1[y]["球队"][3], ans1[y]["胜率"][3]),
                           (ans1[y]["球队"][4], ans1[y]["胜率"][4]),
                           (ans1[y]["球队"][5], ans1[y]["胜率"][5])
                           ],

                radius=["10%", "30%"],
                rosetype="radius",
                center=["77%", "30%"])
                # .set_series_opts(tooltip_opts=opts.TooltipOpts(is_show=False, trigger="item"))
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    return c



timeline = Timeline()

for i in range(minn, maxn + 1):
    timeline.add(bar_base(year = i), "{}年".format(i), )
timeline.add_schema(is_auto_play=True, play_interval=2000)

timeline.render("NBA.html")


with open("NBA.html", "r", encoding="utf-8") as f:
    html_content=f.read()

soup = BeautifulSoup(html_content, "html.parser")

modify = soup.find("div", class_="chart-container")
print(modify)
modify["style"] = "width:1600px; height:900px;"

with open("NBA.html", "w", encoding="utf-8") as f:
    f.write(str(soup))








