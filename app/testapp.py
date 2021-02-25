from sanic import Blueprint
from sanic.response import json
from sanic_openapi import doc, swagger_blueprint
from db.connect import SqlConnection
testapp = Blueprint('testapp')

cnx = SqlConnection(-6)  # ISTSQL Server SMDB dbo

filter_qtags = [(1, 'QIL'), (2, 'SES2'), (3, 'QYAS'),
                (4, 'QCINS'), (5, 'HR'), (6, 'QMED1'), (7, 'SES1X1')]
def get_idd_valueslist():
    values_list = dict()
    for gtuple in filter_qtags:
        x, y = gtuple
        ch = f"convert(int,iddvalues)" if y == "QYAS" else f"iddvalues"
        script = (
            f"select {ch} {y} from idd_values_list t1 (nolock) where Qtag='{y}' order by {ch} asc")
        temp = cnx.getData(script).to_dict('records')
        values_list[y] = temp
    # print(values_list)
    return values_list
    # Proje bazlı data seçmelerinde verilen filtreleri json olarak basıyor.
    dict_df = cnx.getData(
        f"Select * from smdb..idd_project_filter where projectId='{projid}'").to_dict('records')
    # print(dict_df)
    return dict_df

def get_basic_chart():
    return cnx.getData("""select 
                        count(case when QIL is not null then 1 end) count_QIL,
                        count(case when Ses2 is not null then 1 end) count_SES2,
                        count(case when QYAS is not null then 1 end) count_QYAS,
                        count(case when QCINS is not null then 1 end) count_QCINS,
                        count(case when HR is not null then 1 end) count_HR,
                        count(case when QMED1 is not null then 1 end) count_QMED1,
                        count(case when MD is not null then 1 end) count_MD
                        --count(case when MESLEK is not null then 1 end) count_MESLEK
                        --select *
                        from Idd_Table where DataDurum=1 """)

@testapp.route('/basic_count_chart')
@doc.summary("Test route")
async def basiccountchart(request):
    basic_count_chart = get_basic_chart().iloc[0].tolist()
    return json(basic_count_chart)


@testapp.route('/idd_values_list')
@doc.summary("Test route")
async def valuelist(request):
    values_list = get_idd_valueslist()
    return json(values_list)


@testapp.route("/hello", methods=['GET'])
@doc.summary("Test route")
@doc.tag("test")
@doc.description('This is a test route with detail description.')
async def test(request):
    return json({"hello": "world"})


@testapp.route("/emre", methods=['GET'])
@doc.summary("Test route")
@doc.tag("testx")
@doc.description('This is a test route with detail description.')
async def test1(request):
    return json({"name": "emre"})
