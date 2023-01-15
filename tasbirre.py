import PySimpleGUI as sg
import numpy as np
import cv2
from pathlib import Path

blankImage = cv2.imencode(".png", np.zeros((250, 250, 3), np.uint8))[1]
blankImageBytes = blankImage.tobytes()

def getImageData(path: str):
    try:
        image = cv2.imread(path)
        convertedImage = cv2.imencode(".png", image)[1]

    except Exception:
        sg.popup("画像ファイルを選択してください")
        window["imageRawPreview"].update(data = blankImageBytes)
        return blankImage

    return convertedImage

sg.theme("Default")

previewPart = sg.Frame(
    "",
    [
        [sg.FileBrowse("ファイルを選択", key = "fileBrowse"), sg.T(key = "")],
        [sg.T("編集前:")],
        [sg.Image(data = blankImageBytes, key = "imageRawPreview")],
        [sg.T("編集後:")],
        [sg.Image(data = blankImageBytes, key = "imageResultPreview")]
    ],
    key = "framePreview"
)

editPart = sg.Frame(
    "",
    [
        [
            sg.T("明るさ", size = (10, 0), justification = "right"),
            sg.Slider(
                range = (0, 100),
                default_value = 50,
                orientation = "h",
                key = "sliderBrightness"
            )
        ],
        [
            sg.T("コントラスト", size = (10, 0), justification = "right"),
            sg.Slider(
                range = (0, 100),
                default_value = 50,
                orientation = "h",
                key = "sliderContrast"
            )
        ],
        [
            sg.T("彩度", size = (10, 0), justification = "right"),
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

window["imageRawPreview"].bind("<Button1-Motion>", "__DRAG")

while True:
    event, values = window.read(timeout = 50)

    imagePath = values["fileBrowse"]
    rawImage = getImageData(imagePath).tobytes() if ("/" in imagePath) else blankImageBytes # not sure if it works on both WINDOWS and MAC
    window["imageRawPreview"].update(data = rawImage)
    
    resultImage = getImageData(imagePath).tobytes() if ("/" in imagePath) else blankImageBytes
    window["imageResultPreview"].update(data = resultImage)


    if event == "imageRawPreview__DRAG":
        print("dragged")

    if event == "buttonRevert":
        window["sliderBrightness"].update(50)
        window["sliderContrast"].update(50)
        window["sliderSaturation"].update(50)

    if event == sg.WIN_CLOSED:
        break

window.close()