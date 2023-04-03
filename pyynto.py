import json
import requests

def main():
    mittaus = {"x": 6,
               "y": 10}
    
    while(True):
        mittaus["x"] = int(input("Anna viikonpäivän numero >"))
        mittaus["y"] = int(input("Anna lämpötila >"))

        viesti = json.dumps(mittaus)
        vastaus = requests.post('http://localhost:5000/lisaa', data = viesti)



if __name__ == "__main__":
    main()
    