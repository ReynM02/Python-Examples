import requests
import urllib
import numpy as np
import cv2
import PySimpleGUI as sg
import webbrowser

URL = 'https://api.unsplash.com/photos/random/?client_id=3Iqs26tTMit-i9hFTLDHnohG-OpPM4WDQ6MtNdLAAoQ'

LAYOUT = [
    [sg.Text("Image Viewer", size=(30, 1), text_color="#134A8F", justification="center", font=["Kanit",48,"bold"], expand_x= True)],
    [sg.Image(filename="", key="-IMAGE-", size=(80, 80), expand_x=True, expand_y=True)],
    [sg.Text("Search Term:", font=["Open Sans",15,""]), sg.InputText(enable_events=True, size=(20, 5), font=["",15,""], key="-TERM-", do_not_clear=True)],
    [sg.Button("Search!", size=(10,2), font=["Open Sans",20,"bold"], key="-SEARCH-"), sg.Button("Download", size=(10,2), font=["Open Sans",20,"bold"], visible=False, key="-DOWNLOAD-")]
]

class API:
    response = {}
    
    def __init__(self, url) -> None:
        self.url = url

    def url_to_image(self, url):
        resp = urllib.request.urlopen(url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        self.image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    def MakeRequest(self, term:str):
        parameters = {
            "query": term,
            "count": 1
        }
        r = requests.get(URL, params=parameters)
        response_dict = r.json()
        self.response = response_dict[0]
        #print(self.response)
        self.url_to_image(self.response["urls"]["small"])
        height, width = self.image.shape[:2]
        name = self.response["user"]["name"]
        text = "Image by "+ name + " on Unsplash"
        self.image = cv2.putText(self.image, text, (5,(height-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
        self.downloadlink = self.response["links"]["download"]
        self.imgID = self.response["id"]

window = sg.Window('Image Viewer', LAYOUT, finalize=True, resizable=True)
unsplash = API(URL)
while True:
    event, values = window.read(timeout=20) # Reads window actions waiting for inputs
    # event is an action... event == "Exit" is Exit Button being pressed
    if event == "Exit" or event == sg.WIN_CLOSED: # Exit Button Pressed or Window Closed
        break
    elif event == "-SEARCH-":
        searchTerm = values["-TERM-"]
        unsplash.MakeRequest(searchTerm)
        imgbytes = cv2.imencode(".png", unsplash.image)[1].tobytes()
        window["-IMAGE-"].update(data=imgbytes)
        window["-DOWNLOAD-"].update(visible=True)
    elif event == "-DOWNLOAD-":
        resp = urllib.request.urlopen(unsplash.downloadlink)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        img = cv2.imdecode(image, cv2.IMREAD_COLOR)
        cv2.imwrite(str("C:/Users/matt.reynolds/OneDrive - Smart Vision Lights/Pictures/" + unsplash.imgID + ".jpg"), img)
    elif event == "-IMAGE-":
        webbrowser.open(unsplash.response["links"]["html"])