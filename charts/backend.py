import uvicorn
from uvicorn.reloaders.statreload import StatReload
from uvicorn.main import run, get_logger
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.responses import PlainTextResponse

from utils.tiempo import eightDigits
from utils.pipeline import MongoDBPipeline


app = Starlette(debug=True, template_directory='templates')


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
    for i in range(len(result)):
        doc[i+1] = result[i]

    return JSONResponse(doc)


@app.exception_handler(500)
async def server_error(request, exc):
    return PlainTextResponse('暂无数据')


if __name__ == '__main__':
    reloader = StatReload(get_logger('debug'))
    reloader.run(run, {
        'app': app,
        'host': '127.0.0.1',
        'port': 50000,
        'log_level': 'debug',
        'debug': 'true'
    })
    uvicorn.run(app, host='127.0.0.1', port=50000)
