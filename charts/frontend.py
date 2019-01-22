import uvicorn
from uvicorn.main import run, get_logger
from uvicorn.reloaders.statreload import StatReload
from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

from utils.tiempo import eightDigits, ft
from datahandler import DataHandler
from settings import FRONTEND_PORT


app = Starlette(debug=True, template_directory='templates')
app.mount('/assets', StaticFiles(directory='assets'), name='assets')


@app.route('/chart/{name}')
async def charts(request):
    try:
        chart = request.path_params['name']     # e.g. 'rise'
    except KeyError:
        chart = 'nem_rise'

    try:
        day = request.query_params['day']       # eg. 20181209
    except KeyError:
        day = eightDigits()

    # some backend rendering
    props = DataHandler(chart, day).props

    template = app.get_template('index.html')
    content = template.render(request=request,
                              props=props,
                              )
    return HTMLResponse(content)


if __name__ == '__main__':
    reloader = StatReload(get_logger('debug'))
    reloader.run(run, {
        'app': app,
        'host': '0.0.0.0',
        'port': FRONTEND_PORT,
        'log_level': 'debug',
        'debug': 'true'
    })

    uvicorn.run(app, host='0.0.0.0', port=FRONTEND_PORT, debug='true')
