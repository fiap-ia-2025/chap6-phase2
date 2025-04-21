import requests
import pandas as pd
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
from requests import HTTPError
from farm import Farm
from agriculture_type import AgricultureType

API_KEY = "1c5de160d5299d773c6c2e8b4ce89279"


def print_weather(city, state):
    city_full = city + ', ' + state + ', BR'
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city_full, "appid": API_KEY, "units": "metric", "lang": "pt_br"}

    try:
        resp = requests.get(url, params=params)
        resp.raise_for_status()
    except HTTPError:
        print("Não foi possível buscar informações da temperatura na sua cidade, tente novamente em alguns minutos!\n")
        return

    weather_data = resp.json()

    weekday_names = ("Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo")
    weekday_today = weekday_names[datetime.today().weekday()]

    print("As informações de temperatura na sua cidade:\n")
    print(
        f"{city} - {state} \n{weekday_today}, {datetime.now().strftime("%H:%M")} \n{weather_data["weather"][0]["description"].upper()}\n")
    print(f"Temperatura: {weather_data['main']['temp']}°C")
    print(f"Sensação térmica: {weather_data['main']['feels_like']}C°")
    print(f"Temperatura mínima: {weather_data['main']['temp_min']}°C")
    print(f"Temperatura máxima: {weather_data['main']['temp_max']}°C")
    print(f"Umidade: {weather_data['main']['humidity']}%")

def state_choice_is_valid(state_choice):
    states = pd.read_csv("../files/states.csv")
    states = states.fillna('') #Remove opções em branco
    states['State'] = states['SIGLA'].str.strip()
    states = states['State'].tolist()

    state_is_valid = state_choice in states
    if not state_is_valid:
            print("\nO estado informado não existe!\n")

    return state_is_valid

def city_choice_is_valid(city_choice, state_choice):
    cities = pd.read_csv("../files/cities.csv")
    cities = cities.fillna('') #Remove opções em branco
    cities['City'] = cities['MUNICIPIO_TOM'].str.strip() + ", " +  cities['UF'].str.strip()
    cities = cities['City'].tolist()

    city_and_state_choice = city_choice + ", " + state_choice

    city_and_state_is_valid = city_and_state_choice in cities
    if not city_and_state_is_valid:
            print("\nA cidade informada não existe ou não pertence ao estado informado anteriormente!\n")
    return city_and_state_is_valid

def is_string(input_char):
    if input_char.isdigit():
        print("\nDigite apenas letras!\n")
    return not input_char.isdigit()

def save_response_data_on_log_file(response):
    try:
        arq = open("../files/search_weather_log.txt", "a")
        arq.write("\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "," + str(response.json()))
        arq.close()
    except Exception as e:
        print(repr(e))
        print("Não foi possível gravar o log da consulta!")

def determine_irrigation_for_farm(farm):

    geolocator = Nominatim(user_agent="clima_app")
    location = geolocator.geocode(farm.get_city_state_full())
    latitude = location.latitude
    longitude = location.longitude

    #Define intervalo de datas: últimos 3 dias
    end = datetime.now() - timedelta(days=1)  # evita usar o dia atual que pode não ter dados
    start = end - timedelta(days=10)

    start_date = start.strftime('%Y-%m-%d')
    end_date = end.strftime('%Y-%m-%d')

    #Monta a URL da API Open-Meteo
    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={latitude}&longitude={longitude}&"
        f"start_date={start_date}&end_date={end_date}&"
        f"daily=precipitation_sum&timezone=America/Sao_Paulo"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError:
        print("Não foi possível buscar o histórico de informações da temperatura na sua cidade, tente novamente em alguns minutos!\n")
        return

    save_response_data_on_log_file(response)
    data = response.json()

    #Analisa os dados
    days = data.get("daily", {}).get("time", [])
    rains = data.get("daily", {}).get("precipitation_sum", [])

    #Ordena dados em ordem descendente
    data_sorted_desc = sorted(zip(days, rains), reverse=True)

    dry_days = 0
    for dt, rain in data_sorted_desc:
        if rain == 0 or rain is None:
            dry_days += 1

    print(f"Total de dias secos: {dry_days}")

    #Alerta ao produtor
    for agriculture_type in farm.agriculture_types:
        if dry_days >= agriculture_type.max_days_without_irrigation():
            if dry_days > 1:
                print(f"\nALERTA: Há {dry_days} dias não chove. Considere iniciar irrigação para a plantação de {agriculture_type.describe()}.")
            else:
                print(f"\nALERTA: Há {dry_days} dia não chove. Considere iniciar irrigação para a plantação de {agriculture_type.describe()}.")

def main():

    print("\nOlá, bem vindo ao Sistema de Controle de Irrigação com alerta por tempo sem chuva para sua fazenda!\n")

    state_is_not_valid = True
    state_choice = ''

    while state_is_not_valid:
        state_choice = input("Para começar, digite a sigla do estado de sua Fazenda (ex: caso seja São Paulo, digite SP):\n")

        if is_string(state_choice):
            state_choice = state_choice.strip().upper()
            state_is_not_valid = not state_choice_is_valid(state_choice)

    city_is_not_valid = True
    city_choice = ''

    while city_is_not_valid:
        city_choice = input("\nAgora, digite a sua cidade: \n")

        if is_string(city_choice):
            city_choice = city_choice.upper()
            city_is_not_valid = not city_choice_is_valid(city_choice, state_choice)

    print_weather(city_choice, state_choice)

    choice = 0

    while choice not in (1, 2):
        choice = int(input("\nVocê deseja realizar o controle de irrigação da sua fazenda conosco (apenas café, soja ou cana de açúcar)? Digite uma das opções abaixo: \n1-Sim \n2-Não\n"))
        if choice not in (1, 2):
            print("Opção inválida!")

    if choice == 2:
        print("Tchau, obrigada!")
        return

    farm_name = input("Ótima escolha, vamos continuar. \nAgora, digite o nome da sua fazenda: ")
    qtd = int(input("Quantas plantações você deseja controlar? "))

    agriculture_types = [None] * qtd

    valid_agriculture_types = tuple(item.value for item in AgricultureType)

    input_valid = 0
    while input_valid < qtd:
        print(f"{AgricultureType.SOYA.value} - {AgricultureType.SOYA.describe()}")
        print(f"{AgricultureType.SUGAR_CANE.value} - {AgricultureType.SUGAR_CANE.describe()}")
        print(f"{AgricultureType.COFFE.value} - {AgricultureType.COFFE.describe()}")

        value = int(input("Escolha uma das opções acima: "))
        if value in agriculture_types:
            print("Por favor, escolha uma opção ainda não selecionada!")
        elif value not in valid_agriculture_types:
            print(f"A opção selecionada precisar ser um dos valores: {valid_agriculture_types}")
        else:
            agriculture_types[input_valid] = AgricultureType(value)
            input_valid = input_valid + 1

    farm = Farm(farm_name, city_choice, state_choice, agriculture_types)

    print("Iniciando o monitoramento...")

    determine_irrigation_for_farm(farm)

# Chama a função principal
if __name__ == "__main__":
    main()
