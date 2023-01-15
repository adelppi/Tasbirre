import PySimpleGUI as sg
import numpy as np
import cv2
import os
from pathlib import Path

blankImage = cv2.imencode(".png", np.zeros((250, 250, 4), np.uint8))[1]
blankImageBytes = blankImage.tobytes()

def getImageData(path: str, blank: bool = False):
    if blank:
        return blankImage
    else:
        image = cv2.imread(path)
        convertedImage = cv2.imencode(".png", image)[1]
        return convertedImage

sg.theme("Default")

previewPart = sg.Frame(
    "",
    [
        [sg.FileBrowse("ファイルを選択", key = "fileBrowse"), sg.InputText(key = "inputText")],
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
                range = (-5, 5),
                default_value = 0,
                resolution = 0.01,
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
    event, values = window.read(timeout = 0)

    # LUTS
    brightness = values["sliderBrightness"]
    contrast = values["sliderContrast"]
    saturation = values["sliderSaturation"]

    baseLUT = np.arange(256)
    gamma = (baseLUT / 255) ** brightness * 255

    try:
        imagePath = values["inputText"]
        rawImage = getImageData(imagePath) if os.path.exists(imagePath) else blankImage # not sure if it works on both WINDOWS and MAC
        window["imageRawPreview"].update(data = rawImage.tobytes())
        editImage = cv2.imread(imagePath) if os.path.exists(imagePath) else rawImage.copy()
        editImage = cv2.LUT(editImage, gamma)
        resultImage = cv2.imencode('.png', editImage)[1]
        window["imageResultPreview"].update(data = resultImage.tobytes())

    except Exception:
        window["inputText"].update("")
        sg.popup("画像ファイルを選択してください")

    if event == "imageRawPreview__DRAG":
        print("dragged")

    if event == "buttonRevert":
        window["sliderBrightness"].update(0)
        window["sliderContrast"].update(50)
        window["sliderSaturation"].update(50)

    if event == sg.WIN_CLOSED:
        break

window.close()