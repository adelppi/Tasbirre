import PySimpleGUI as sg
import numpy as np
import cv2
import os

windowSizeX = 1125
windowSizeY = 750
allowedImageSizeX = 750
allowedImageSizeY = 300

blankImage = cv2.imencode(".png", np.zeros((allowedImageSizeX, allowedImageSizeY, 4), np.uint8))[1]

sg.theme("Default")

previewPart = sg.Frame(
    "",
    [
        [sg.FileBrowse("ファイルを選択", font = ("Meiryo UI", 15), key = "fileBrowse"), sg.InputText(key = "inputText", font = ("Meiryo UI", 10))],
        [sg.T("", font = ("Meiryo UI", 15), key = "before")],
        [sg.Image(data = blankImage.tobytes(), key = "imageRawPreview")],
        [sg.T("", font = ("Meiryo UI", 15), key = "after")],
        [sg.Image(data = blankImage.tobytes(), key = "imageResultPreview")]
    ],
    key = "framePreview"
)

editPart = sg.Frame(
    "",
    [
        [
            sg.T("明るさ", size = (8, 0), justification = "right", font = ("Meiryo UI", 15)),
            sg.Slider(
                range = (0, 100),
                default_value = 50,
                resolution = 1,
                orientation = "h",
                key = "sliderBrightness"
            )
        ],
        [
            sg.T("コントラスト", size = (8, 0), justification = "right", font = ("Meiryo UI", 15)),
            sg.Slider(
                range = (0, 100),
                default_value = 50,
                resolution = 1,
                orientation = "h",
                key = "sliderContrast"
            )
        ],
        [
            sg.T("彩度", size = (8, 0), justification = "right", font = ("Meiryo UI", 15)),
            sg.Slider(
                range = (0, 100),
                default_value = 50,
                resolution = 1,
                orientation = "h",
                key = "sliderSaturation"
            )
        ],
        [
            sg.B("保存", font = ("Meiryo UI", 15), key = "buttonSave"),
            sg.B("最初に戻す", font = ("Meiryo UI", 15), key = "buttonRevert")
        ]
    ],
    key = "frameEdit"
)

layout = [
    [previewPart, editPart]
]

window = sg.Window("Tasbirre", layout, size = (windowSizeX, windowSizeY), resizable = True)
window.Finalize()

while True:
    event, values = window.read(timeout = 100)

    if event == sg.WIN_CLOSED:
        break

window.close()