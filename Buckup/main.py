#coding:utf-8
import discord
import os
import subprocess
from time import  sleep
import random
import create_base_data

token = 'NzU5NjIwODM3OTQxODM3ODM3.X3AKCA.htvmDaL4WAvpvAUV9fEQJBFMxlU'

my_channel = 'genkantv'   # 根城とするチャンネル名
use_message_limit = 3        # 根城から取得する過去メッセージ数（自分の発言は除外されるので実際はもっと少ない）

base_file = 'messages_759750762262691871.txt'      # こいつが学習データ
use_markov_file = "base_text.txt"     # マルコフ連鎖プログラム実行時に使うセリフファイル

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    # 特定のチャンネルで発言があるまたは話しかけられたら、その発言を学習用データにする
    if message.channel.name == my_channel or (str(client.user.id) in message.content):

        # 学習用データに追記。いちおうチャンネルごと
        # いまのところ特にこの学習用データを使うコードはない
        if '@' not in message.content:
            f = open('messages_' + str(message.channel.id) + '.txt','a', encoding="utf-8")
            f.write(message.content)
            f.write('\n')
            f.close()

            # 話しかけられたらマルコフ連鎖で生成したテキストを投稿する
        if str(client.user.id) in message.content:
            # 直近の発言のうち、Botでない発言を取得
            
            msg = ""
            async for log in message.channel.history():
            # client.logs_from(discord.utils.get(message.server.channels, name=my_channel), limit=use_message_limit):
                if message.author != client.user:
                    # マルコフ連鎖で文章生成する 
                    # ここまで
                    msg += log.content + "\n"
            if '@' not in message.content:
                # Bot以外の発言を、マルコフ連鎖の元となるテキストに追加
                create_base_data.create_base_data(base_file, use_markov_file, msg, use_message_limit * 2)

            murmur = create_base_data.generate_text()

            # sleep(5 * random.random())  # あんまりはやく返事するとBotっぽいのでちょっと待つ
            msg = (murmur).format(message)
            await message.channel.send(msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(token)
