import requests

URL = 'http://192.168.3.213:8080/square/'

class API:
    response = {}

    def __init__(self, url) -> None:
        self.url = url

    def MakeRequest(self, num):
        r = requests.get(self.url + str(num))
        return r.json()["square"]

if __name__ == "__main__":
    square = API(URL)
    while True:
        num = input("Enter a number to be squared ('exit' to quit): ")
        if num == 'exit':
            break
        try:
            int(num)
            squaredNum = square.MakeRequest(num)
            print("The Squared number is: ", squaredNum)
        except:
            print("Please enter a number! ('exit' to quit)")

    