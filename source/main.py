import requests
import pandas as pd
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
from farm import Farm
from agriculture_type import AgricultureType

API_KEY = "1c5de160d5299d773c6c2e8b4ce89279"


def print_weather(city, state):
    city_full = city + ', ' + state + ', BR'
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city_full, "appid": API_KEY, "units": "metric", "lang": "pt_br"}
    resp = requests.get(url, params=params)
    resp.raise_for_status()
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
    arq = open("../files/search_weather_log.txt", "a")
    arq.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "," + response)
    arq.close()

def determine_irrigation_for_farm():
    cidade = "Cidade Ocidental, GO, Brasil"
    geolocator = Nominatim(user_agent="clima_app")
    location = geolocator.geocode(cidade)
    latitude = location.latitude
    longitude = location.longitude

    # === 3. Define intervalo de datas: últimos 3 dias ===
    fim = datetime.now() - timedelta(days=1)  # evita usar o dia atual que pode não ter dados
    inicio = fim - timedelta(days=10)

    data_inicio = inicio.strftime('%Y-%m-%d')
    data_fim = fim.strftime('%Y-%m-%d')

    # === 4. Monta a URL da API Open-Meteo ===
    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={latitude}&longitude={longitude}&"
        f"start_date={data_inicio}&end_date={data_fim}&"
        f"daily=precipitation_sum&timezone=America/Sao_Paulo"
    )

    # === 5. Faz a requisição ===
    resposta = requests.get(url)
    dados = resposta.json()

    # === 6. Analisa os dados ===
    dias = dados.get("daily", {}).get("time", [])
    chuvas = dados.get("daily", {}).get("precipitation_sum", [])

    print(f"\nPrecipitação nos últimos 3 dias em {cidade}:\n")

    dias_secos = 0
    for data, chuva in zip(dias, chuvas):
        print(f"{data}: {chuva} mm")
        if chuva == 0 or chuva is None:
            dias_secos += 1

    # === 7. Alerta ao produtor ===
    if dias_secos >= 3:
        print("\nALERTA: Já são 3 dias sem chuva. Considere iniciar irrigação.")
    else:
        print(f"\nTotal de dias secos: {dias_secos}")

    # geolocator = Nominatim(user_agent="clima_app")
    # location = geolocator.geocode("Londrina, PR, Brasil")
    #
    # end = datetime.now() - timedelta(days=3)
    # start = datetime.now() - timedelta(days=1)
    #
    # end_date = end.strftime('%Y-%m-%d')
    # start_date = start.strftime('%Y-%m-%d')
    #
    # print(f"{start_date} - {end_date}")
    #
    # url = (
    #     f"https://archive-api.open-meteo.com/v1/archive?"
    #     f"latitude={location.latitude}&longitude={location.longitude}&"
    #     f"start_date={start_date}&end_date={end_date}&"
    #     f"daily=precipitation_sum&timezone=America/Sao_Paulo"
    # )
    #
    # response = requests.get(url)
    # response_data = response.json()
    #
    # # save_response_data_on_log_file(response_data)
    #
    # days = response_data.get("daily", {}).get("time", [])
    # rains = response_data.get("daily", {}).get("precipitation_sum", [])
    #
    # print(f"{days} - {rains}")
    #
    # print(f"\nPrecipitação nos últimos 3 dias em :\n")
    #
    # dry_days = 0
    # for data, chuva in zip(days, rains):
    #     print(f"{data}: {chuva} mm")
    #     if chuva == 0 or chuva is None:
    #         dry_days += 1
    #
    # if dry_days >= 3:
    #     print("\nALERTA: Já são 3 dias sem chuva. Considere iniciar irrigação.")
    # else:
    #     print(f"\nTotal de dias secos: {dry_days}")


def main():

    # print("\nOlá, bem vindo ao Sistema de Controle de Irrigação com alerta por tempo sem chuva para sua fazenda!\n")
    #
    # state_is_not_valid = True
    # state_choice = ''
    #
    # while state_is_not_valid:
    #     state_choice = input("Para começar, digite a sigla do estado de sua Fazenda (ex: caso seja São Paulo, digite SP):\n")
    #
    #     if is_string(state_choice):
    #         state_choice = state_choice.strip().upper()
    #         state_is_not_valid = not state_choice_is_valid(state_choice)
    #
    # city_is_not_valid = True
    # city_choice = ''
    #
    # while city_is_not_valid:
    #     city_choice = input("\nAgora, digite a sua cidade: \n")
    #
    #     if is_string(city_choice):
    #         city_choice = city_choice.upper()
    #         city_is_not_valid = not city_choice_is_valid(city_choice, state_choice)
    #
    # # print_weather(city_choice, state_choice)
    #
    # choice = 0
    #
    # while choice not in (1, 2):
    #     choice = int(input("\nVocê deseja realizar o controle de irrigação da sua fazenda conosco (apenas café, soja ou cana de açúcar)? Digite uma das opções abaixo: \n1-Sim \n2-Não\n"))
    #     if choice not in (1, 2):
    #         print("Opção inválida!")
    #
    # if choice == 2:
    #     print("Tchau, obrigada!")
    #     return
    #
    # farm_name = input("Ótima escolha, vamos continuar. \nAgora, digite o nome da sua fazenda: ")
    # qtd = int(input("Quantas plantações você deseja controlar? "))
    #
    # agriculture_types = [None] * qtd
    #
    # for i in range(qtd):
    #     print(f"{AgricultureType.SOYA.value} - {AgricultureType.SOYA.describe()}")
    #     print(f"{AgricultureType.SUGAR_CANE.value} - {AgricultureType.SUGAR_CANE.describe()}")
    #     print(f"{AgricultureType.COFFE.value} - {AgricultureType.COFFE.describe()}")
    #
    #     value = int(input("Escolha uma das opções acima: "))
    #     agriculture_types[i] = value
    #
    # farm = Farm(farm_name, city_choice, state_choice, agriculture_types)
    #
    # print("Iniciando o monitoramento.")

    determine_irrigation_for_farm()

# Chama a função principal
if __name__ == "__main__":
    main()
