import discord
import random

class RPGView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.jugador = {
            "HP": 100,
            "Ataque": 10,
            "Defensa": 5,
            "Velocidad": 5,
            "Monedas": 0,
            "Inventario": []
        }
        self.objetos_disponibles = {
            "Espada Épica": {"Ataque": 15, "Imagen": "https://i.imgur.com/example.png", "Precio": 100, "Icono": "🗡️"},
            "Escudo Antiguo": {"Defensa": 10, "Imagen": "https://i.imgur.com/example.png", "Precio": 80, "Icono": "🛡️"},
            "Botas Rápidas": {"Velocidad": 7, "Imagen": "https://i.imgur.com/example.png", "Precio": 50, "Icono": "👢"},
            "Poción de Vida": {"HP": 50, "Imagen": "https://i.imgur.com/example.png", "Precio": 20, "Icono": "🧪"}
        }

    @discord.ui.button(label="Explorar", style=discord.ButtonStyle.primary, custom_id="explorar_button")
    async def explorar(self, interaction: discord.Interaction, button: discord.ui.Button):
        eventos = [
            ("Te encuentras con un grupo de bandidos y luchas valientemente. Ganaste 10 monedas y un botín.", self.luchar_con_bandidos),
            ("Encuentras un cofre y lo abres cuidadosamente. Ganaste 5 monedas.", self.encontrar_moneda),
            ("Un dragón aparece y ruge en la distancia, pero logras escapar.", None),
        ]

        evento, accion = random.choice(eventos)
        embed = discord.Embed(title="Evento RPG", description=evento, color=discord.Color.gold())

        if accion:
            accion()
            embed.add_field(name="Monedas", value=f"Ahora tienes {self.jugador['Monedas']} monedas.")
            if self.jugador["Inventario"]:
                inventario_text = "\n".join(self.jugador["Inventario"])
                embed.add_field(name="Inventario", value=inventario_text)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    def luchar_con_bandidos(self):
        self.jugador["Monedas"] += 10
        objeto = random.choice(list(self.objetos_disponibles.keys()))
        self.jugador["Inventario"].append(objeto)
        for stat, value in self.objetos_disponibles[objeto].items():
            if stat != "Imagen" and stat != "Precio" and stat != "Icono":
                self.jugador[stat] += value

    def encontrar_moneda(self):
        self.jugador["Monedas"] += 5

    @discord.ui.button(label="Tienda", style=discord.ButtonStyle.success, custom_id="tienda_button")
    async def tienda(self, interaction: discord.Interaction, button: discord.ui.Button):
        tienda_embed = discord.Embed(
            title="Bienvenido a la Tienda",
            description="Aquí puedes comprar objetos con tus monedas.",
            color=discord.Color.green()
        )

        # Añadir un botón por cada objeto disponible en la tienda
        botones_por_fila = 1  # Solo hay un objeto por botón en la tienda
        fila = 1


        # Agregar los botones correspondientes
        for i, (objeto, detalles) in enumerate(self.objetos_disponibles.items()):
            icono = detalles["Icono"]
            button = discord.ui.Button(
                label=f"{icono} {objeto}",
                style=discord.ButtonStyle.primary,
                custom_id=f"comprar_{objeto}",
                row=fila
            )
            self.add_item(button)

            # En este caso, ya no es necesario cambiar de fila, solo agregamos un objeto por fila
            fila += 1

        await interaction.response.send_message(embed=tienda_embed, view=self, ephemeral=True)

    @discord.ui.button(label="Inventario", style=discord.ButtonStyle.secondary, custom_id="inventario_button")
    async def inventario(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.jugador["Inventario"]:
            await interaction.response.send_message("Tu inventario está vacío.", ephemeral=True)
        else:
            inventario_text = "\n".join(self.jugador["Inventario"])
            embed = discord.Embed(
                title="Tu Inventario",
                description=f"Estos son tus objetos:\n{inventario_text}",
                color=discord.Color.blue()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Salir", style=discord.ButtonStyle.danger, custom_id="salir_button")
    async def salir(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "Si te ibas a salir tan pronto para qué empiezas a jugar, máquina.",
            ephemeral=True
        )

    # Función para comprar un objeto
    async def comprar_objeto(self, interaction: discord.Interaction, button: discord.ui.Button):
        objeto = button.custom_id.replace("comprar_", "")
        precio = self.objetos_disponibles[objeto]["Precio"]

        if self.jugador["Monedas"] >= precio:
            self.jugador["Monedas"] -= precio
            self.jugador["Inventario"].append(objeto)
            await interaction.response.send_message(f"Has comprado {objeto} por {precio} monedas.", ephemeral=True)
        else:
            await interaction.response.send_message("No tienes suficientes monedas para comprar este objeto.", ephemeral=True)