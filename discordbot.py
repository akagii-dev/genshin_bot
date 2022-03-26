import datetime
from email import message
from http import client
from tracemalloc import stop
from unittest import async_case
from dateutil.relativedelta import relativedelta
import discord

TOKEN = 'hogehoge'

# 日付の定義
eventday1 = datetime.datetime(2022, 4, 1, 5, 0, 0)
eventday2 = datetime.datetime(2022, 4, 16, 5, 0, 0)
today = datetime.datetime(2022, 4, 1, 7, 0, 0)
stopday = datetime.datetime(2050, 12, 31, 23, 59, 59)

# 空のリストを作成
outputdays1 = []
outputdays2 = []

# 起動時に実行


@client.event
async def on_ready():
    # ターミナルにログインしたときに表示される
    print('ログインしました')

# 月の加算関数の定義


def get_eventday(eventday):
    return eventday + relativedelta(months=1)


# 2050年12月31日までループし、イベントがある日付リストに追加する
while 1:
    calc = eventday1 - today
    eventday1 = get_eventday(eventday1)
    if 0 < calc.days+1 < 16:  # 17日以内にイベントがある場合表示する
        outputdays1.append(calc.days+1)
    else:  # イベントが日付に達した場合ループを抜ける
        break
while 1:
    calc = eventday2 - today
    eventday2 = get_eventday(eventday2)
    if 0 < calc.days+1 < 16:  # 17日以内にイベントがある場合表示する
        outputdays2.append(calc.days+1)
    else:  # イベントが日付に達した場合ループを抜ける
        break


@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content == '!rasen_day':
        if len(outputdays1) == 0:
            await message.channel.send(outputdays2[0])
        else:
            await message.channel.send(outputdays1[0])

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
