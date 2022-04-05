import datetime
from email import message
from http import client
from multiprocessing.connection import Client
from tracemalloc import stop
from unittest import async_case
from dateutil.relativedelta import relativedelta
import discord
import urllib.request
from bs4 import BeautifulSoup
import time

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

    if message.content == '!gacha':
        # スクレイピングするURL
        url = "https://kamigame.jp/genshin/page/124661894958054216.html"
        # urlからhtmlを取得
        html = urllib.request.urlopen(url)
        # 構文解析
        soup = BeautifulSoup(html.read(), "lxml")
        tables = soup.find("table", {"class": "fixed_table tabbed_gacha_期間限定"}).find(
            "tbody").find_all("tr")
        # ピックアップ中のガチャの写真とキャラ表示
        for i in range(len(tables)):
            get_gacha_names = []
            get_gacha_imgs = []
            # ガチャのピックアップ中のキャラ、日程の配列をつくるのための空の配列
            output_list = []
            # 空欄も含めたリストの作成
            output_list2 = tables[i].text.split("\n")
            for j in output_list2:
                if j != "":
                    output_list.append(j)
            # 日程 + 【おすすめ】 + 星の数から日程のみを取り出す
            part_list = list(output_list[1])
            # フォーマットし、∧日程のみを取り出す
            start_date = str(
                today.year) + "/" + part_list[0] + part_list[1] + part_list[2] + part_list[3] + part_list[4]
            finish_date = str(
                today.year) + "/" + part_list[8] + part_list[9] + part_list[10] + part_list[11] + part_list[12]
            # 日程
            today_date = str(today.year) + "/" + \
                str(today.month) + "/" + str(today.day)
            try:
                time.strptime(start_date, "%Y/%m/%d")
                time.strptime(finish_date, "%Y/%m/%d")
                time.strptime(today_date, "%Y/%m/%d")
                # ガチャのピックアップ中のキャラ、日程を取り出す
                get_gacha_img = tables[i].find(
                    "a").find("img", {"class": ""})
                get_gacha_names.append(get_gacha_img.get("alt"))
                get_gacha_imgs.append(get_gacha_img.get("src"))
                await message.channel.send(get_gacha_names[0])
                await message.channel.send(get_gacha_imgs[0])
                m3 = "開催日:" + start_date + "〜" + "終了日:" + finish_date
                await message.channel.send(m3)
            except ValueError:
                # ガチャのピックアップ中のキャラ、日程を取り出す
                get_gacha_img = tables[i].find(
                    "a").find("img", {"class": ""})
                get_gacha_names.append(get_gacha_img.get("alt"))
                get_gacha_imgs.append(get_gacha_img.get("src"))
                await message.channel.send(get_gacha_names[0])
                await message.channel.send(get_gacha_imgs[0])
                except_part_list = []
                for k in range(26):
                    except_part_list.append(part_list[k])
                m4 = ''.join(except_part_list)
                await message.channel.send(m4)


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
