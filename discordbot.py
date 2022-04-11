import datetime
from http import client
from multiprocessing.connection import Client
from tracemalloc import stop
from dateutil.relativedelta import relativedelta
import discord
import urllib.request
from bs4 import BeautifulSoup as bs
import time
import requests
import os
import cv2
import tempfile
from matplotlib import pyplot as plt

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
    eventday1 = datetime.datetime(2022, 3, 1, 5, 0, 0, 0)
    eventday2 = datetime.datetime(2022, 3, 16, 5, 0, 0)
    stopday = datetime.datetime(2050, 12, 31, 23, 59, 59)
    # 空の配列を作成
    outputdays1 = []
    outputdays2 = []
    if message.author.bot:
        return
    if message.content == '!help':
        embed = discord.Embed(title="This is help command", color=0x7b68ee)
        embed.add_field(name="!help", value="コマンド一覧", inline=False)
        embed.add_field(name="!rasen_all", value="いつ螺旋が終了するかを表示し、全ての敵の編成を表示する", inline=False)
        embed.add_field(name="!rasen9", value="いつ螺旋が終了するかを表示し、9層の敵の編成を表示する", inline=False)
        embed.add_field(name="!rasen10", value="いつ螺旋が終了するかを表示し、10層の敵の編成を表示する", inline=False)
        embed.add_field(name="!rasen11", value="いつ螺旋が終了するかを表示し、11層の敵の編成を表示する", inline=False)
        embed.add_field(name="!rasen12", value="いつ螺旋が終了するかを表示し、12層の敵の編成を表示する", inline=False)
        embed.add_field(name="!gacha", value="ピックアップ中のガチャを表示する", inline=False)
        await message.channel.send(embed=embed)
    if message.content == '!rasen_all':
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

        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        header = {'User-Agent': user_agent}
        before_url = "https://spiralabyss.org/floor-"

        if len(outputdays1) == 0:
            m1 = "螺旋終了まであと"+str(outputdays2[0])+"日"
            await message.channel.send(m1)
        else:
            m2 = "螺旋終了まであと"+str(outputdays1[0])+"日"
            await message.channel.send(m2)

        for i in range(4):
            add = str(i+9)
            url = before_url + add
            re = requests.get(url, headers=header)
            soup = bs(re.content, 'html.parser')
            #n-m 1st | 2nd の部分を取得
            for_j_element  = soup.find_all("h5", {"class": "mb-3"})
            for j in range(len(for_j_element)):
                #n-m 1st | 2nd の分繰り返す
                await message.channel.send(for_j_element[j].text)
                for_k_element = for_j_element[j].find_all("img", {"class": "enemy hover-scale"})
                list_show_img = []
                #敵のイメージを取得
                for k in range(len(for_k_element)):
                    element = for_k_element[k].get("src").replace(" ", "%20")
                    list_show_img.append(element)
                    hconcat_img = []
                    for l in range(len(list_show_img)):
                    # 画像をリクエストする
                            img_url = list_show_img[l]
                            res = requests.get(img_url)
                            # Tempfileを作成して即読み込む
                            fp = tempfile.NamedTemporaryFile(dir='./', delete=False)
                            fp.write(res.content)
                            fp.close()
                            img = cv2.imread(fp.name)
                            hconcat_img.append(img)
                            os.remove(fp.name)
                img = cv2.hconcat(hconcat_img)
                cv2.imwrite(for_j_element[j].text + ".png", img)
                await message.channel.send(file=discord.File(for_j_element[j].text + ".png"))
                os.remove(for_j_element[j].text + ".png")

    if message.content == '!rasen9':
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

        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        header = {'User-Agent': user_agent}
        before_url = "https://spiralabyss.org/floor-"

        if len(outputdays1) == 0:
            m1 = "螺旋終了まであと"+str(outputdays2[0])+"日"
            await message.channel.send(m1)
        else:
            m2 = "螺旋終了まであと"+str(outputdays1[0])+"日"
            await message.channel.send(m2)

        add = str(9)
        url = before_url + add
        re = requests.get(url, headers=header)
        soup = bs(re.content, 'html.parser')
        #n-m 1st | 2nd の部分を取得
        for_j_element  = soup.find_all("h5", {"class": "mb-3"})
        for j in range(len(for_j_element)):
            #n-m 1st | 2nd の分繰り返す
            await message.channel.send(for_j_element[j].text)
            for_k_element = for_j_element[j].find_all("img", {"class": "enemy hover-scale"})
            list_show_img = []
            #敵のイメージを取得
            for k in range(len(for_k_element)):
                element = for_k_element[k].get("src").replace(" ", "%20")
                list_show_img.append(element)
                hconcat_img = []
                for l in range(len(list_show_img)):
                # 画像をリクエストする
                        img_url = list_show_img[l]
                        res = requests.get(img_url)
                        # Tempfileを作成して即読み込む
                        fp = tempfile.NamedTemporaryFile(dir='./', delete=False)
                        fp.write(res.content)
                        fp.close()
                        img = cv2.imread(fp.name)
                        hconcat_img.append(img)
                        os.remove(fp.name)
            img = cv2.hconcat(hconcat_img)
            cv2.imwrite(for_j_element[j].text + ".png", img)
            await message.channel.send(file=discord.File(for_j_element[j].text + ".png"))
            os.remove(for_j_element[j].text + ".png")

    if message.content == '!rasen10':
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

        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        header = {'User-Agent': user_agent}
        before_url = "https://spiralabyss.org/floor-"

        if len(outputdays1) == 0:
            m1 = "螺旋終了まであと"+str(outputdays2[0])+"日"
            await message.channel.send(m1)
        else:
            m2 = "螺旋終了まであと"+str(outputdays1[0])+"日"
            await message.channel.send(m2)

        add = str(10)
        url = before_url + add
        re = requests.get(url, headers=header)
        soup = bs(re.content, 'html.parser')
        #n-m 1st | 2nd の部分を取得
        for_j_element  = soup.find_all("h5", {"class": "mb-3"})
        for j in range(len(for_j_element)):
            #n-m 1st | 2nd の分繰り返す
            await message.channel.send(for_j_element[j].text)
            for_k_element = for_j_element[j].find_all("img", {"class": "enemy hover-scale"})
            list_show_img = []
            #敵のイメージを取得
            for k in range(len(for_k_element)):
                element = for_k_element[k].get("src").replace(" ", "%20")
                list_show_img.append(element)
                hconcat_img = []
                for l in range(len(list_show_img)):
                # 画像をリクエストする
                        img_url = list_show_img[l]
                        res = requests.get(img_url)
                        # Tempfileを作成して即読み込む
                        fp = tempfile.NamedTemporaryFile(dir='./', delete=False)
                        fp.write(res.content)
                        fp.close()
                        img = cv2.imread(fp.name)
                        hconcat_img.append(img)
                        os.remove(fp.name)
            img = cv2.hconcat(hconcat_img)
            cv2.imwrite(for_j_element[j].text + ".png", img)
            await message.channel.send(file=discord.File(for_j_element[j].text + ".png"))
            os.remove(for_j_element[j].text + ".png")

    if message.content == '!rasen11':
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

        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        header = {'User-Agent': user_agent}
        before_url = "https://spiralabyss.org/floor-"

        if len(outputdays1) == 0:
            m1 = "螺旋終了まであと"+str(outputdays2[0])+"日"
            await message.channel.send(m1)
        else:
            m2 = "螺旋終了まであと"+str(outputdays1[0])+"日"
            await message.channel.send(m2)

        add = str(11)
        url = before_url + add
        re = requests.get(url, headers=header)
        soup = bs(re.content, 'html.parser')
        #n-m 1st | 2nd の部分を取得
        for_j_element  = soup.find_all("h5", {"class": "mb-3"})
        for j in range(len(for_j_element)):
            #n-m 1st | 2nd の分繰り返す
            await message.channel.send(for_j_element[j].text)
            for_k_element = for_j_element[j].find_all("img", {"class": "enemy hover-scale"})
            list_show_img = []
            #敵のイメージを取得
            for k in range(len(for_k_element)):
                element = for_k_element[k].get("src").replace(" ", "%20")
                list_show_img.append(element)
                hconcat_img = []
                for l in range(len(list_show_img)):
                # 画像をリクエストする
                        img_url = list_show_img[l]
                        res = requests.get(img_url)
                        # Tempfileを作成して即読み込む
                        fp = tempfile.NamedTemporaryFile(dir='./', delete=False)
                        fp.write(res.content)
                        fp.close()
                        img = cv2.imread(fp.name)
                        hconcat_img.append(img)
                        os.remove(fp.name)
            img = cv2.hconcat(hconcat_img)
            cv2.imwrite(for_j_element[j].text + ".png", img)
            await message.channel.send(file=discord.File(for_j_element[j].text + ".png"))
            os.remove(for_j_element[j].text + ".png")

    if message.content == '!rasen12':
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

        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        header = {'User-Agent': user_agent}
        before_url = "https://spiralabyss.org/floor-"

        if len(outputdays1) == 0:
            m1 = "螺旋終了まであと"+str(outputdays2[0])+"日"
            await message.channel.send(m1)
        else:
            m2 = "螺旋終了まであと"+str(outputdays1[0])+"日"
            await message.channel.send(m2)

        add = str(12)
        url = before_url + add
        re = requests.get(url, headers=header)
        soup = bs(re.content, 'html.parser')
        #n-m 1st | 2nd の部分を取得
        for_j_element  = soup.find_all("h5", {"class": "mb-3"})
        for j in range(len(for_j_element)):
            #n-m 1st | 2nd の分繰り返す
            await message.channel.send(for_j_element[j].text)
            for_k_element = for_j_element[j].find_all("img", {"class": "enemy hover-scale"})
            list_show_img = []
            #敵のイメージを取得
            for k in range(len(for_k_element)):
                element = for_k_element[k].get("src").replace(" ", "%20")
                list_show_img.append(element)
                hconcat_img = []
                for l in range(len(list_show_img)):
                # 画像をリクエストする
                        img_url = list_show_img[l]
                        res = requests.get(img_url)
                        # Tempfileを作成して即読み込む
                        fp = tempfile.NamedTemporaryFile(dir='./', delete=False)
                        fp.write(res.content)
                        fp.close()
                        img = cv2.imread(fp.name)
                        hconcat_img.append(img)
                        os.remove(fp.name)
            img = cv2.hconcat(hconcat_img)
            cv2.imwrite(for_j_element[j].text + ".png", img)
            await message.channel.send(file=discord.File(for_j_element[j].text + ".png"))
            os.remove(for_j_element[j].text + ".png")
    
    if message.content == '!dev':
        embed = discord.Embed(
            title="This is development command", color=0x7b68ee)
        embed.add_field(name="today", value=today, inline=False)
        await message.channel.send(embed=embed)

    if message.content == '!gacha':
        # スクレイピングするURL
        url = "https://kamigame.jp/genshin/page/124661894958054216.html"
        # urlからhtmlを取得
        html = urllib.request.urlopen(url)
        # 構文解析
        soup = bs(html.read(), "lxml")
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
                formatted_finish_date = time.strptime(finish_date, "%Y/%m/%d")
                formatted_today_date = time.strptime(today_date, "%Y/%m/%d")
                if formatted_finish_date < formatted_today_date:
                    return
                # ガチャのピックアップ中のキャラ、日程を取り出す
                else:
                    get_gacha_img = tables[i].find(
                        "a").find("img", {"class": ""})
                    get_gacha_names.append(get_gacha_img.get("alt"))
                    get_gacha_imgs.append(get_gacha_img.get("src"))
                    m5 = "開催日:" + start_date + "〜" + "終了日:" + finish_date
                    embed = discord.Embed(
                        title=get_gacha_names[0], description=m5, color=0x7b68ee)
                    embed.set_image(url=get_gacha_imgs[0])
                    await message.channel.send(embed=embed)
            except ValueError:
                get_gacha_img = tables[i].find(
                    "a").find("img", {"class": ""})
                get_gacha_names.append(get_gacha_img.get("alt"))
                get_gacha_imgs.append(get_gacha_img.get("src"))
                except_part_list = []
                for k in range(26):
                    except_part_list.append(part_list[k])
                m6 = ''.join(except_part_list)
                embed = discord.Embed(
                    title=get_gacha_names[0], description=m6, color=0x7b68ee)
                embed.set_image(url=get_gacha_imgs[0])
                await message.channel.send(embed=embed)
# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)