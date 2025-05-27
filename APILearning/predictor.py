import requests

def intelli(name):
    age = requests.get(f'https://api.agify.io?name={name}')
    gender = requests.get(f'https://api.genderize.io?name={name}')
    nation = requests.get(f'https://api.nationalize.io?name={name}')

    print(f"Name: {name}")  
    print(f"Estimated Age: {age.json()["age"]}")
    print(f"Likely gender: {gender.json()["gender"]} (probability: {gender.json()["probability"]*100}%)")
    top1_c = f'{nation.json()["country"][0]["country_id"]} ({nation.json()["country"][0]["probability"]*100:.2f}%)'

    top2_c = f'{nation.json()["country"][1]["country_id"]} ({nation.json()["country"][1]["probability"]*100:.2f}%)'
    print(f"Top 2 Nationalities: {top1_c}, {top2_c}")

intelli(input("Enter your name: "))