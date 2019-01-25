import json
import requests

from settings import BACKEND_PORT
from statemgmt import StateManager
from utils.tiempo import buildClass, delta, ft


class PropsFactory():

    nem_charts = {
        'nem_rise': '云音乐飙升榜',
        'nem_new': '云音乐新歌榜',
        'nem_original': '网易原创歌曲榜',
        'nem_hot': '云音乐热歌榜',
    }

    qq_charts = {
        'qq_new': 'QQ音乐巅峰榜·新歌',
        'qq_hot': 'QQ音乐巅峰榜·热歌',
        'qq_trends': 'QQ音乐巅峰榜·流行指数',
        'qq_original': 'QQ音乐巅峰榜·腾讯音乐人原创榜',
    }

    def __init__(self, chart: str, day: str):
        self.chart, self.day = chart, day
        url = f'http://127.0.0.1:{BACKEND_PORT}/toplist?chart={chart}&day={day}'
        content = requests.get(url).content
        if content:
            self.j = json.loads(content)

        self.buildProps()

    def buildProps(self):
        self.props = {}
        self.props['songlist'] = self.j
        self.props['delta'] = delta
        self.props['ft'] = ft
        self.props['buildClass'] = buildClass
        self.props['statemgr'] = StateManager

        if self.chart.startswith('nem_'):
            self.props['chart_title'] = self.nem_charts[self.chart]
        elif self.chart.startswith('qq_'):
            self.props['chart_title'] = self.qq_charts[self.chart]
