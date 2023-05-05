import discord
from discord import Embed, Interaction, ui
from discord.ext import commands
import asyncio
import os
client = discord.Client(intents=discord.Intents.all())
#slash = SlashCommand(client, sync_commands=True)
application_id = int(os.environ["APPLICATION_ID"])
TOKEN = str(os.environ["DISCORD_TOKEN"])
chid = int(os.environ["CH_ID"])
bot = commands.Bot(
    command_prefix="/",
    intents=discord.Intents.all(),
    application_id=application_id
)
tree = bot.tree

@bot.event
async def on_ready():
    await tree.sync()
    print('connected')

@bot.event
async def on_message(message: discord.Message):
    #print(message)
    if message.author.bot:
        return
    if(message.guild == None):
        cl = bot.get_channel(chid)
        await cl.send(message.content)
        print(message.content)

@tree.command(name="set", description="匿名ちゃんがこのチャンネルに降臨するよ！")
async def set(interaction: Interaction):
    global chid
    chid = interaction.channel.id
    await interaction.response.send_message("変更しました！")

class usersel(ui.UserSelect):
    def __init__(self):
        super().__init__()

    async def callback(self, interaction:Interaction):
        await interaction.response.send_message(f"{self.values[0].name}")

@tree.command(name="user", description="ゆーざーひょうじ")
async def user(interaction: Interaction):
    view=ui.View()
    view.add_item(usersel())
    await interaction.response.send_message(content="表示するぞ", view=view)

async def main():
    # start the client
    async with bot:

        await bot.start(TOKEN)

asyncio.run(main())
