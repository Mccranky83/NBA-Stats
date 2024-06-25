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
    #print(sss)
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


from pyecharts.charts import Scatter3D
from pyecharts import options as opts
import random

# # 创建新的Scatter3D对象
# scatter3d = Scatter3D(init_opts=opts.InitOpts(width="600px", height="600px"))

# # 对于ans1中的每一年，获取"胜率"，"均得分"和"胜场"的数据，并添加到Scatter3D对象中
# data = []
# for year, data_dict in ans1.items():
#     for team, win_rate, avg_score, win_games in zip(data_dict["球队"], data_dict["胜率"], data_dict["均得分"], data_dict["胜场"]):
#         data.append([win_rate, avg_score, win_games, team])

# scatter3d.add("", data,
#     grid3d_opts=opts.Grid3DOpts(width=300, height=300, depth=300),
#     xaxis3d_opts=opts.Axis3DOpts(type_="value", name="胜率"),
#     yaxis3d_opts=opts.Axis3DOpts(type_="value", name="均得分"),
#     zaxis3d_opts=opts.Axis3DOpts(type_="value", name="胜场"),

# )

# # 设置Scatter3D对象的标题
# scatter3d.set_global_opts(title_opts=opts.TitleOpts("3D散点图"))

# # 渲染Scatter3D对象
# scatter3d.render("scatter3d.html")

# 创建新的Scatter3D对象
scatter3d = Scatter3D(init_opts=opts.InitOpts(width="800px", height="800px"))

# 创建一个颜色列表
colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(100)]

# 对于ans1中的每一年，获取"胜率"，"均得分"和"胜场"的数据，并添加到Scatter3D对象中
color_index = 0
for year, data_dict in ans1.items():
    team_data = {}
    for team, win_rate, avg_score, win_games in zip(data_dict["球队"], data_dict["胜率"], data_dict["均得分"], data_dict["胜场"]):
        if team not in team_data:
            team_data[team] = []
        team_data[team].append([win_rate, avg_score, win_games])

    for team, data in team_data.items():
        scatter3d.add(team, data,
            itemstyle_opts=opts.ItemStyleOpts(color=colors[color_index]),
            grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
            xaxis3d_opts=opts.Axis3DOpts(type_="value", name="胜率",min_=0.5, max_=1, split_number=10),
            yaxis3d_opts=opts.Axis3DOpts(type_="value", name="均得分", min_=70, max_=140, split_number=5),
            zaxis3d_opts=opts.Axis3DOpts(type_="value", name="胜场", min_=20, max_=80, split_number=5),
        )
        color_index += 1

# 设置Scatter3D对象的标题
scatter3d.set_global_opts(
    title_opts=opts.TitleOpts("3D散点图")
    )

# 渲染Scatter3D对象
scatter3d.render("scatter3d.html")