import datetime
from email import message
from http import client
from multiprocessing.connection import Client
from tracemalloc import stop
from unittest import async_case
from dateutil.relativedelta import relativedelta
import discord

# discordのbotのtokenを入力
TOKEN = 'hogehoge'
client = discord.Client()


# 起動時に実行
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

# メッセージ受信時に実行


@client.event
async def on_message(message):
    # イベント日時を設定
    today = datetime.datetime.today()
    eventday1 = datetime.datetime(2022, 3, 1, 5, 0, 0)
    eventday2 = datetime.datetime(2022, 3, 16, 5, 0, 0)
    stopday = datetime.datetime(2050, 12, 31, 23, 59, 59)
    # 空の配列を作成
    outputdays1 = []
    outputdays2 = []
    if message.author.bot:
        return
    if message.content == '!rasen':
        while 1:
            eventday1 += relativedelta(months=1)  # イベント日時を1ヶ月増やす
            calc = eventday1 - today
            if 0 <= calc.days < 16:  # 16日以内にイベントがある場合表示する
                outputdays1.append(calc.days)
            if eventday1 > stopday:  # イベント日時が終了日時を超えたらループを抜ける
                break
        while 1:
            eventday2 += relativedelta(months=1)  # イベント日時を1ヶ月増やす
            calc = eventday2 - today
            if 0 <= calc.days < 16:  # 16日以内にイベントがある場合表示する
                outputdays2.append(calc.days)
            if eventday2 > stopday:  # イベント日時が終了日時を超えたらループを抜ける
                break
        if len(outputdays1) == 0:
            m1 = "螺旋終了まであと"+str(outputdays2[0])+"日"
            await message.channel.send(m1)
        else:
            m2 = "螺旋終了まであと"+str(outputdays1[0])+"日"
            await message.channel.send(m2)
        if message.content == '!dev':
            await message.channel.send(today)
            await message.channel.send(eventday1)
            await message.channel.send(eventday2)
            await message.channel.send(stopday)


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
