# Importación de librerías necesarias de Discord
import discord
from discord.ext import commands

# Configuración de los intents (permisos) para el bot
intents = discord.Intents.default()
intents.message_content = True  # Necesario para que el bot pueda leer mensajes

# Inicialización del bot con el prefijo de comandos '!' y los intents configurados
bot = commands.Bot(command_prefix='!', intents=intents)

# Evento que se ejecuta cuando el bot se conecta exitosamente
@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

# Clase para la vista de botones RPG (Interfaz de usuario interactiva)
class RPGView(discord.ui.View):
    # Botón "Explorar" con estilo primario (azul)
    @discord.ui.button(label="Explorar", style=discord.ButtonStyle.primary, custom_id="explorar_button")
    async def explorar(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Lista de posibles eventos aleatorios con sus imágenes (actualmente placeholders)
        eventos = [
            ("Te encuentras con un grupo de bandidos.", "insertar imagen aqui"),
            ("Descubres un cofre lleno de oro.", "insertar imagen aqui"),
            ("Un dragón aparece y ruge en la distancia.", "insertar imagen aqui"),
        ]
        import random  # Importación local para mejor performance
        evento, imagen = random.choice(eventos)
        
        # Creación de un embed (mensaje enriquecido) para mostrar el evento
        embed = discord.Embed(title="Evento RPG", description=evento, color=discord.Color.gold())
        embed.set_image(url=imagen)
        # Respuesta efímera (solo visible para el usuario que interactuó)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    # Botón "Salir" con estilo peligroso (rojo)
    @discord.ui.button(label="Salir", style=discord.ButtonStyle.danger, custom_id="salir_button")
    async def salir(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Gracias por jugar!", ephemeral=True)

# Comando principal para iniciar el juego (TODO mencionado en el comentario)
@bot.command()
async def start(ctx):
    view = RPGView()
    # Mensaje inicial con la vista que contiene los botones
    await ctx.send("yepa ya estoy por aqui. que tu quiere ase manito?", view=view)

# Clase para el menú desplegable de items
class ItemMenu(discord.ui.Select):
    def __init__(self):
        # Opciones del menú desplegable con emojis y descripciones
        options = [
            discord.SelectOption(
                label="Tenedor de plástico",
                description="Te puede sacar de algún apuro",
                emoji="🍴"
            ),
            discord.SelectOption(
                label="Poción de veneno",
                description="Solo apto para cobardes",
                emoji="☠️"
            ),
            discord.SelectOption(
                label="Hacha legendario de juguete",
                description="Algo es algo, ¿supongo?",
                emoji="🪓"
            )
        ]
        # Configuración del menú desplegable
        super().__init__(placeholder="Selecciona un item: ", min_values=1, max_values=1, options=options)

    # Función que maneja la selección del usuario
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Increíble! {self.values[0]} es una puta mierda, pero es tu puta mierda!")

# Vista contenedora del menú de items
class ItemMenuView(discord.ui.View):
    def __init__(self, *items, timeout=None):
        super().__init__(*items, timeout=timeout)
        self.add_item(ItemMenu())  # Añade el menú desplegable a la vista

# Comando para acceder a la tienda
@bot.command()
async def shop(ctx):
    await ctx.send("Selecciona un item:", view=ItemMenuView())

# Advertencia de seguridad: El token debería estar en archivo .env
bot.run('DepositeAquíElToken')
