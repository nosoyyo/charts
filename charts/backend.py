import time
import uvicorn
import schedule
from uvicorn.reloaders.statreload import StatReload
from uvicorn.main import run, get_logger
from starlette.applications import Starlette
from starlette.responses import JSONResponse

from utils.tiempo import eightDigits
from utils.pipeline import MongoDBPipeline
from settings import BACKEND_PORT
from qbee import QQRoutine
from nembee import NemRoutine


app = Starlette(debug='true')


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


if __name__ == '__main__':
    reloader = StatReload(get_logger('debug'))
    reloader.run(run, {
        'app': app,
        'host': '127.0.0.1',
        'port': BACKEND_PORT,
        'log_level': 'debug',
        'debug': 'true'
    })
    uvicorn.run(app=app, host='127.0.0.1', port=BACKEND_PORT, debug='true')

    os.system('touch irun')
    schedule.every(3).hours.do(QQRoutine)
    schedule.every().day.at("00:01").do(QQRoutine)
    schedule.every(3).hours.do(NemRoutine)
    schedule.every().day.at("00:02").do(NemRoutine)
    print(schedule.jobs)
    print('schedule 安排上了')
    while True:
        schedule.run_pending()
        time.sleep(1)
