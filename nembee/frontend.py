import json
import uvicorn
import requests
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


@app.route('/chart/{name}')
async def homepage(request):
    try:
        chart = request.path_params['name']     # e.g. 'rise'
    except KeyError:
        chart = 'rise'

    try:
        day = request.query_params['day']       # eg. 20181209
    except KeyError:
        day = eightDigits()

    url = f'http://127.0.0.1:50000/toplist?chart={chart}&day={day}'
    print(f'fetching data from {url}')
    j = json.loads(requests.get(url).content)
    template = app.get_template('index.html')
    content = template.render(request=request, j=j, title=chart, today=day)
    return HTMLResponse(content)



@app.exception_handler(500)
async def server_error(request, exc):
    return PlainTextResponse('暂无数据')


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=40404)
