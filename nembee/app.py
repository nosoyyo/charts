import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.responses import PlainTextResponse

from utils.tiempo import eightDigits
from utils.pipeline import MongoDBPipeline


app = Starlette(debug=True, template_directory='templates')
# app.mount('/static', StaticFiles(directory='statics'), name='static')


@app.route('/')
async def homepage(request):
    template = app.get_template('index.html')
    content = template.render(request=request)
    return HTMLResponse(content)


@app.route('/toplist')
async def toplist(request):
    try:
        day = request.query_params['day']
    except KeyError:
        day = eightDigits()

    try:
        chart = request.query_params['chart']
    except KeyError:
        chart = 'rise'

    m = MongoDBPipeline()
    query = f'{day}.{chart}'
    result = m.ls(query)
    for item in result:
        item.pop('_id')

    doc = {}
    for i in range(100):
        doc[i] = result[i]

    return JSONResponse(doc)


@app.exception_handler(500)
async def server_error(request, exc):
    return PlainTextResponse('暂无数据')


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
