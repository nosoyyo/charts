import json
import requests
import uvicorn
from uvicorn.main import run, get_logger
from uvicorn.reloaders.statreload import StatReload
from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

from utils.tiempo import eightDigits, ft


app = Starlette(debug=True, template_directory='templates')
app.mount('/assets', StaticFiles(directory='assets'), name='assets')


@app.route('/chart/{name}')
async def charts(request):
    try:
        chart = request.path_params['name']     # e.g. 'rise'
    except KeyError:
        chart = 'rise'

    try:
        day = request.query_params['day']       # eg. 20181209
    except KeyError:
        day = eightDigits()

    url = f'http://127.0.0.1:50000/toplist?chart={chart}&day={day}'
    content = requests.get(url).content
    if content:
        j = json.loads()

    # some backend rendering
    artists = [i[1]['artists'][0]['name'] for i in j.items()]
    biggest = 0
    most_artist = []
    for a in artists:
        if artists.count(a) > biggest:
            most_artist = []
            most_artist.append(a)
            biggest = artists.count(a)
        elif artists.count(a) == biggest:
            most_artist.append(a)
    # TODO bad thing happens when no one most
    most_artist = list(set(most_artist))
    ma_result = {}
    for ma in most_artist:
        songs = []
        for i in j.items():
            if i[1]['artists'][0]['name'] == ma:
                songs.append(i[1]['name'])
            ma_result[ma] = songs

    template = app.get_template('index.html')
    content = template.render(request=request,
                              j=j,
                              title=chart,
                              day=day,
                              ft=ft,
                              most_artist=most_artist,
                              ma_result=ma_result,
                              )
    return HTMLResponse(content)


if __name__ == '__main__':
    reloader = StatReload(get_logger('debug'))
    reloader.run(run, {
        'app': app,
        'host': '0.0.0.0',
        'port': 40404,
        'log_level': 'debug',
        'debug': 'true'
    })

    uvicorn.run(app, host='0.0.0.0', port=40404)
