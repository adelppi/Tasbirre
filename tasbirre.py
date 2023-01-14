import PySimpleGUI as sg
import numpy as np
import cv2
from pathlib import Path

blankImage = cv2.imencode(".png", np.zeros((250, 250, 4), np.uint8))[1].tobytes()

def getImageData(path: str):
    image = cv2.imread(path)
    convertedImage = cv2.imencode(".png", image)[1].tobytes()
    return convertedImage

sg.theme("Default")

previewPart = sg.Frame(
    "",
    [
        [sg.FileBrowse("ファイルを選択", key = "fileBrowse"), sg.T()],
        [sg.Image(data = blankImage, key = "imageRawPreview")],
        [sg.Image(data = blankImage, key = "imageResultPreview")]
    ],
    key = "framePreview"
)

editPart = sg.Frame(
    "",
    [
        [
            sg.T("明るさ"),
            sg.Slider(
                range = (0, 100),
                default_value = 50,
                orientation = "h",
                key = "sliderBrightness"
            )
        ],
        [
            sg.T("コントラスト"),
            sg.Slider(
                range = (0, 100),
                default_value = 50,
                orientation = "h",
                key = "sliderContrast"
            )
        ],
        [
            sg.T("彩度"),
            sg.Slider(
                range = (0, 100),
                default_value = 50,
                orientation = "h",
                key = "sliderSaturation"
            )
        ],
        [
            sg.B("保存", key = "buttonSave"),
            sg.B("最初に戻す", key = "buttonRevert")
        ]
    ],
    key = "frameEdit"
)

layout = [
    [previewPart, editPart]
]

window = sg.Window("Tasbirre", layout, size = (720, 860), resizable = True)
window.Finalize()

window["framePreview"].bind("<Button1-Motion>", "__DRAG")

while True:
    event, values = window.read(timeout = 0)

    imagePath = values["fileBrowse"]
    rawImage = getImageData(imagePath) if ("/" in imagePath) else blankImage # not sure if it works on both WINDOWS and MAC

    window["imageRawPreview"].update(data = rawImage)
    # if "/" in imagePath:
    #     # resultImage = cv2.convertScaleAbs(rawImage, alpha = 1, beta = 40)
    #     resultImage = 
    # else:
    #     resultImage = blankImage

    # window["imageResultPreview"].update(data = resultImage)
    
    if event == "framePreview__DRAG":
        print("dragged")

    if event == sg.WIN_CLOSED:
        break

window.close()