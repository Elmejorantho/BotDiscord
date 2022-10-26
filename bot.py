from email import message
from email.mime import image
from urllib import response
from wsgiref.util import request_uri
from aiohttp import request
from dotenv import load_dotenv
from datetime import date
from PIL import Image

load_dotenv()
import datetime
import urllib.request
import json
import requests
import os
import discord
import sqlite3
connectionDB = sqlite3.connect("tutorial.db")
cur = connectionDB.cursor()

intents = discord.Intents.default()
intents.message_content = True


token = os.environ['TOKEN']

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello AnthoKz!')
        
        
    if message.content.startswith('$Comandos'):
        await message.channel.send('''Hola amig@ aqui te dejo los comados que vamos a utilizar para que hagas un recorrdido por toda la informacion que quieras buscar acerca de tu jugador favorito
                                   utiliza: >!Jugador< seguido de >Nombre y apellido<
                                   para conseguir los detalles mas buscados sobre el jugador de tu interes.
                                   
                                   utiliza: >!EnqueEquipo< seguido de >Nombre, apellido y anho<
                                   para conseguir los detalles de en que equipo jugo en el anho que indiques.
                                   
                                   utiliza: >$Carrerade< seguido de >Nombre, apellido y la inicial de la Sesion<
                                   para conseguir los detalles del desempenho de tu jugador en la sesion que le indiques.
                                   ''')  
        
    if message.content.startswith('!Jugador'):
        nombre = message.content.split(' ')[1]
        apellido = message.content.split(' ')[2]
        idDeJugadorR = requests.get(f'http://lookup-service-prod.mlb.com/json/named.search_player_all.bam?sport_code=%27mlb%27&active_sw=%27Y%27&name_part=%27{nombre}%25{apellido}%27')
        response = idDeJugadorR.json()
        idDeJugador = response['search_player_all']['queryResults']['row']['player_id']
        responseFotos = f'https://img.mlbstatic.com/mlb-photos/image/upload/d_people:generic:headshot:67:current.png/w_213,q_auto:best/v1/people/{idDeJugador}/headshot/67/current'
        informacionJugador = requests.get(f'https://lookup-service-prod.mlb.com/json/named.player_info.bam?sport_code=%27mlb%27&player_id=%27{idDeJugador}%27')
        responseJugador = informacionJugador.json()
        
        nombreJugador = responseJugador['player_info']['queryResults']['row']['name_display_last_first']
        sobreNombre = responseJugador['player_info']['queryResults']['row']['name_display_roster']
        paisNacimientoJugador = responseJugador['player_info']['queryResults']['row']['birth_country']
        fechaNacimientoJugador = responseJugador['player_info']['queryResults']['row']['birth_date']
        equipoActualJugador = responseJugador['player_info']['queryResults']['row']['team_name']
        alturaJugador = responseJugador['player_info']['queryResults']['row']['height_feet']
        estatusActivoOInactivo = responseJugador['player_info']['queryResults']['row']['status']
        
        await message.channel.send(f'Apellido y nombre de tu jugador: {nombreJugador}')
        await message.channel.send(f'Apodo: {sobreNombre}')
        await message.channel.send(f'Pais de nacimiento : {paisNacimientoJugador}')
        await message.channel.send(f'Fecha de nacimiento: {fechaNacimientoJugador}'.split('T, 0'))
        await message.channel.send(f'Equipo actual: {equipoActualJugador}')
        await message.channel.send(f'Altura: {alturaJugador} pies.')
        await message.channel.send(f'Estatus de actividad: {estatusActivoOInactivo}.')
        await message.channel.send(f'Foto de tu jugador: {responseFotos}')
        
   
   
    if message.content.startswith('!EnqueEquipo'):
        nombre = message.content.split(' ')[1]
        apellido = message.content.split(' ')[2]
        anhoIndicado = message.content.split(' ')[3]
        idDeJugadorRes = requests.get(f'http://lookup-service-prod.mlb.com/json/named.search_player_all.bam?sport_code=%27mlb%27&active_sw=%27Y%27&name_part=%27{nombre}%25{apellido}%27')
        responseIdEquipo = idDeJugadorRes.json()
        idDeJugador = responseIdEquipo['search_player_all']['queryResults']['row']['player_id']
        
        
        informacionDelEquipo = requests.get(f"https://lookup-service-prod.mlb.com/json/named.player_teams.bam?player_id=%27{idDeJugador}%27&season=%27{anhoIndicado}%27") 
        responseDeEquipo = informacionDelEquipo.json()
        nombreDelEquipo = responseDeEquipo['player_teams']['queryResults']['row']['team']
        inicioDeContrato = responseDeEquipo['player_teams']['queryResults']['row']['start_date']
        posicionDelJugador = responseDeEquipo['player_teams']['queryResults']['row']['primary_position']
        accionDelJugador = responseDeEquipo['player_teams']['queryResults']['row']['primary_stat_type']
        finalizacionDeContrato = responseDeEquipo['player_teams']['queryResults']['row']['end_date']
        
        
        await message.channel.send(f'El nombre del equipo en el que jugo para el año que buscaste es para tu jugador: {nombreDelEquipo}')
        await message.channel.send(f'Comenzo a jugar en la fecha: {inicioDeContrato}')
        await message.channel.send(f'La posicion en campo era: {posicionDelJugador}')
        await message.channel.send(f'Posicion: {accionDelJugador}')
        await message.channel.send(f'Finalizo su contrato en la fecha: {finalizacionDeContrato}')
        
        
    
    
    
    if message.content.startswith('$Carrerade'):
        nombre = message.content.split(' ')[1]
        apellido = message.content.split(' ')[2]
        sesion = message.content.split(' ')[3]
        idDeJugadorR = requests.get(f'http://lookup-service-prod.mlb.com/json/named.search_player_all.bam?sport_code=%27mlb%27&active_sw=%27Y%27&name_part=%27{nombre}%25{apellido}%27')
        responseId = idDeJugadorR.json()
        idDeJugador = responseId['search_player_all']['queryResults']['row']['player_id'] 
    
        
        informacionDeLaSesion = requests.get(f"http://lookup-service-prod.mlb.com/json/named.sport_career_hitting.bam?league_list_id='mlb'&game_type='{sesion}'&player_id='{idDeJugador}'") 
        responseCarrera = informacionDeLaSesion.json()
        carreraDeJugador = responseCarrera['sport_career_hitting']['queryResults']['row']['hr']
        alBateDeJugador = responseCarrera['sport_career_hitting']['queryResults']['row']['ab']
        basesPorBolaJugador = responseCarrera['sport_career_hitting']['queryResults']['row']['bb']
        basesRobadasJugador = responseCarrera['sport_career_hitting']['queryResults']['row']['sb']
        hitsJugador = responseCarrera['sport_career_hitting']['queryResults']['row']['h']
        
        
        await message.channel.send(f'Los jonrones de tu jugador en esta sesion: {carreraDeJugador}')
        await message.channel.send(f'Oportunidades al bate de tu jugador en esta sesion: {alBateDeJugador}')
        await message.channel.send(f'Bases por bola de tu jugador en esta sesion: {basesPorBolaJugador}')
        await message.channel.send(f'Bases robadas de tu jugador en esta sesion: {basesRobadasJugador}')
        await message.channel.send(f'Hits de tu jugador en esta sesion: {hitsJugador}')
        
    if message.content.startswith('!infoEquipo'):
        fecha = datetime.datetime.now() 
        nombre1 = message.content.split(' ')[1]
        nombre2 = message.content.split(' ')[2]
        equipos = nombre1 , nombre2
        requestEquipo = requests.get(f'http://lookup-service-prod.mlb.com/json/named.team_all_season.bam?sport_code=%27mlb%27&all_star_sw=%27N%27&sort_order=name_asc&season=%27{fecha.strftime("%Y")}%27')
        responseEquipos = requestEquipo.json()
        
        def filtrado(equipo):
            if equipo == equipos:
                return responseEquipos
            
            equipoFiltrado = filtrado()    
        
        
        
        
        await message.channel.send(f'Esta es la informacion buscada:Tu equipo es: {filtrado}') 
        
       
        
        
                                      
    #     urllib.request.urlretrieve(
    #  f'https://img.mlbstatic.com/mlb-photos/image/upload/d_people:generic:headshot:67:current.png/w_213,q_auto:best/v1/people/{idDeJugador}/headshot/67/current', "jugadores.png")
  
    #     img = Image.open("jugadores.png")
    #     img.show()
   
    
        
    # if message.content.startswith('!clima'):

    #     ciudad = (message.content.split(' '))[1]
    #     info = requests.get(f'https://goweather.herokuapp.com/weather/{ciudad}')
    #     response = info.json()
    #     todayTemp = response['temperature']
    #     tomorrowTemp = response['forecast'][0]['temperature']
    #     tomorrowTemp2 = response['forecast'][1]['temperature']
    #     await message.channel.send(f'Temperatura en {ciudad}')
    #     await message.channel.send(f'El dia de hoy es: {todayTemp}')
    #     await message.channel.send(f'El dia de maniana sera: {tomorrowTemp}')
    #     await message.channel.send(f'El dia de pasado maniana sera: {tomorrowTemp2}')
    
    # if message.content.startswith('!crearUsuario'):
    #     first_name = (message.content.split(' '))[1]
    #     last_name = (message.content.split(' '))[2]
    #     full_name = f'{first_name} {last_name}'
    #     email = message.content.split(' ')[3]
    #     password = message.content.split(' ')[4]
    #     cur.execute('INSERT INTO users (discord_id, name, email, password) VALUES (?, ?, ?)', [
    #                 message.author.id, full_name, email, password])
    #     connectionDB.commit()
    #     await message.channel.send('Usuario creado amigo/a')    
        
        
        
        
    # if message.content.startswith('!borrarUsuario'):
    #     cur.execute('DELETE FROM users WHERE discord_id = ?', [message.author.id])
    #     connectionDB.commit()
    #     await message.channel.send('Usuario eliminado')


    # if message.content.startswith('!')



    

        # response = request.post('http://api.cup2022.ir/api/v1/user', 
        # data={'name': full_name, 'email': email, 'password': password, 'passwordConfirm': confirmPass}) 
        # print(response.json().message)
        # res = requests.post()


# def getUSer(name)
    # for i, persona in enumerate(personas):
    #     if persona.name == name:
    #         return persomas[1]
    #     break



client.run(token)