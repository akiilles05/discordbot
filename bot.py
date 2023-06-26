import discord
from discord import File
from discord.ext import commands
from easy_pil import Editor, load_image_async, Font
import yaml

with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

token = config["Bot_token"]
guild = config["GuildID"]
hatter = config["Hatterkep"]

intents = intents = discord.Intents.all()
intents.guilds = True
intents.members = True
intents.messages = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print("------")


@bot.event
async def on_member_join(member):
    # Channel ID bekérése a config.yaml fájlból
    channel = bot.get_channel(guild)

    # Beágyazott üzenet
    embed = discord.Embed(
        title=f"<:icon_join:1122789374539616306> Hello {member.name} !",
        description="Kérlek olvasd el a <#1107914497944989738>",
        color=discord.Color.green()
    )
    embed.set_footer(text=f"Te vagy a szerveren az {len(member.guild.members)} tag!")
    embed.set_image(url=f"attachment://{hatter}")

    # Fotó generálása
    background = Editor(hatter)
    profile_image = await load_image_async(str(member.avatar.url))

    profile = Editor(profile_image).resize((150, 150)).circle_image()
    poppins = Font.poppins(size=50, variant="bold")

    poppins_small = Font.poppins(size=20, variant="light")

    background.paste(profile, (325, 90))
    background.ellipse((325, 90), 150, 150, outline="white", stroke_width=5)

    background.text((400, 260), f"Üdvözöllek {member.guild.name}", color="white", font=poppins, align="center")
    background.text((400, 325), f"{member.name}#{member.discriminator}", color="white", font=poppins_small,
                    align="center")

    file = File(fp=background.image_bytes, filename=hatter)
    await channel.send(embed=embed, file=file)


bot.run(token)
