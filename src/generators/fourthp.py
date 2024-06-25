import mysql.connector
from bs4 import BeautifulSoup
from pyecharts import options as opts
from pyecharts.charts import Bar, BMap, PictorialBar, Timeline
from pyecharts.faker import Faker
from pyecharts.globals import SymbolType

connection = mysql.connector.connect(
    host="192.168.43.100", user="root", password="123456", database="NBA_database"
)


cursor = connection.cursor()

cursor.execute("SHOW TABLES")
tables = cursor.fetchall()
table_content = {}
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
    s = str(i)
    ss = s[:4]
    if maxn < int(ss):
        maxn = int(ss)
    if minn > int(ss):
        minn = int(ss)
    sss = int(ss)

    if sss not in ans1:
        ans1[sss] = {"球队": [], "胜率": [], "均得分": [], "均失分": [], "胜场": []}
    if table_content[i][0][1] == "Oklahoma City Thunder":
        ans1[sss]["球队"].append("雷霆")
    else:
        ans1[sss]["球队"].append(table_content[i][0][1])
    ans1[sss]["胜率"].append(table_content[i][0][4])
    ans1[sss]["均得分"].append(table_content[i][0][8])
    ans1[sss]["均失分"].append(table_content[i][0][9])
    ans1[sss]["胜场"].append(table_content[i][0][2])


def redirect_to_year(year):
    result = {}
    for i in ans1:
        if i == year:
            result = ans1[i]

    tempt = []
    for i in result:
        for j in result[i]:
            tempt.append(j)

    output = []
    index = -1
    for i in range(len(tempt)):
        if i % 6 == 0:
            output.append([])
            index += 1
        output[index].append(tempt[i])

    win_ratio = []
    for i in output[1]:
        win_ratio.append(i * 100)

    # print([output, win_ratio])

    return [output, win_ratio]


def bar_base(year: int) -> Bar:
    c = (
        PictorialBar()
        .add_xaxis(redirect_to_year(year)[0][0])
        .add_yaxis(
            "胜率",
            # win_ratio,
            redirect_to_year(year)[1],
            label_opts=opts.LabelOpts(is_show=False),
            symbol_size=10,
            symbol_repeat="fixed",
            symbol_offset=[0, 0],
            is_symbol_clip=True,
        )
        .add_yaxis(
            "均得分",
            # output[2],
            redirect_to_year(year)[0][2],
            label_opts=opts.LabelOpts(is_show=False),
            symbol_size=10,
            symbol_repeat="fixed",
            symbol_offset=[0, 15],
            is_symbol_clip=True,
        )
        .add_yaxis(
            "均失分",
            # output[3],
            redirect_to_year(year)[0][3],
            label_opts=opts.LabelOpts(is_show=False),
            symbol_size=10,
            symbol_repeat="fixed",
            symbol_offset=[0, 30],
            is_symbol_clip=True,
        )
        .add_yaxis(
            "胜场",
            # output[4],
            redirect_to_year(year)[0][4],
            label_opts=opts.LabelOpts(is_show=False),
            symbol_size=10,
            symbol_repeat="fixed",
            symbol_offset=[0, 45],
            is_symbol_clip=True,
        )
        .reversal_axis()
        .set_global_opts(
            title_opts=opts.TitleOpts(title="PictorialBar-各球队数据"),
            xaxis_opts=opts.AxisOpts(is_show=False),
            yaxis_opts=opts.AxisOpts(
                axistick_opts=opts.AxisTickOpts(is_show=False),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(opacity=0)
                ),
            ),
        )
        # .render("pictorialbar_multi_custom_symbols.html")
    )
    return c


def main():
    timeline = Timeline()
    for i in range(2015, 2023):
        timeline.add(bar_base(year=i), "{}年".format(i))
    timeline.add_schema(is_auto_play=True, play_interval=2000)
    timeline.render("pictorialbar_multi_custom_symbols.html")

    with open("pictorialbar_multi_custom_symbols.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")

    modify = soup.find("div", class_="chart-container")
    modify["style"] = "width:1600px; height:900px;"

    with open("pictorialbar_multi_custom_symbols.html", "w", encoding="utf-8") as f:
        f.write(str(soup))


if __name__ == "__main__":
    main()
