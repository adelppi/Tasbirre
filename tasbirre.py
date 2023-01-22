import PySimpleGUI as sg
import numpy as np
import cv2
import os

windowSizeX = 1125
windowSizeY = 750
allowedImageSizeX = 750
allowedImageSizeY = 300

blankImage = cv2.imencode(".png", np.zeros((allowedImageSizeX, allowedImageSizeY, 4), np.uint8))[1]
blankImageBytes = blankImage.tobytes()

def getImageData(path: str, blank: bool = False):
    global imageRatioX, imageRatioY
    if blank:
        return blankImage

    else:
        image = cv2.imread(path)
        height, width = image.shape[:2]
        imageRatioX = allowedImageSizeX / width
        imageRatioY = allowedImageSizeY / height
        if imageRatioX > imageRatioY:
            imageRatioX = imageRatioY
        else:
            imageRatioY = imageRatioX
            
        image = cv2.resize(image, dsize = None, fx = imageRatioX, fy = imageRatioY)
        convertedImage = cv2.imencode(".png", image)[1]
        return convertedImage

sg.theme("Default")

previewPart = sg.Frame(
    "",
    [
        [sg.FileBrowse("ファイルを選択", font = ("Meiryo UI", 15), key = "fileBrowse"), sg.InputText(key = "inputText", font = ("Meiryo UI", 10))],
        [sg.T("", font = ("Meiryo UI", 15), key = "before")],
        [sg.Image(data = blankImageBytes, key = "imageRawPreview")],
        [sg.T("", font = ("Meiryo UI", 15), key = "after")],
        [sg.Image(data = blankImageBytes, key = "imageResultPreview")]
    ],
    key = "framePreview"
)

editPart = sg.Frame(
    "",
    [
        [
            sg.T("明るさ", size = (8, 0), justification = "right", font = ("Meiryo UI", 15)),
            sg.Slider(
                range = (0, 5),
                default_value = 1,
                resolution = 0.01,
                orientation = "h",
                key = "sliderBrightness"
            )
        ],
        [
            sg.T("コントラスト", size = (8, 0), justification = "right", font = ("Meiryo UI", 15)),
            sg.Slider(
                range = (0, 100),
                default_value = 50,
                orientation = "h",
                key = "sliderContrast"
            )
        ],
        [
            sg.T("彩度", size = (8, 0), justification = "right", font = ("Meiryo UI", 15)),
            sg.Slider(
                range = (0, 100),
                default_value = 50,
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
window["imageRawPreview"].bind("<Button1-Motion>", "__DRAG")
window["imageRawPreview"].bind("<Button1-ButtonRelease>", "__RELEASE")
window["imageRawPreview"].bind("<Button1-ButtonPress>", "__PRESS")
widget = window["imageRawPreview"].Widget
dragXY = []

while True:
    event, values = window.read(timeout = 100)

    # LUT
    brightness = values["sliderBrightness"]
    contrast = values["sliderContrast"]
    saturation = values["sliderSaturation"]

    baseLUT = np.arange(256)
    gamma = (baseLUT / 255) ** brightness * 255
    contrastLUT = np.clip(255 / contrast * baseLUT, 0, 255)
    resultLUT = (np.clip(255 / contrast * baseLUT, 0, 255) / 255) ** brightness * 255

    try:
        imagePath = values["inputText"]
        # if rawImage is not getImageData(imagePath):
        rawImage = getImageData(imagePath) if os.path.exists(imagePath) else blankImage
        window["imageRawPreview"].update(data = rawImage.tobytes())
        editImage = cv2.resize(cv2.imread(imagePath), dsize = None, fx = imageRatioX, fy = imageRatioY) if os.path.exists(imagePath) else rawImage.copy()
        if event == "imageRawPreview__RELEASE":
            editImage = editImage[cropStart[0]:cropEnd[0], cropStart[1]:cropEnd[1]]
            dragXY = []
            window["imageRawPreview"].draw_line((cropStart[0], cropEnd[0]), (cropStart[1], cropEnd[1]), color='#00FF00', width=1)
            print(cropStart, cropEnd)
        editImage = cv2.LUT(editImage, resultLUT)
        resultImage = cv2.imencode('.png', editImage)[1]
        window["imageResultPreview"].update(data = resultImage.tobytes())

    except Exception:
        window["inputText"].update("")
        sg.popup("エラー")

    if rawImage is not blankImage:
        window["before"].update("編集前:")
        window["after"].update("編集後:")

    if event == "imageRawPreview__DRAG":
        dragXY.append([widget.winfo_pointerx() - widget.winfo_rootx(),
                       widget.winfo_pointery() - widget.winfo_rooty()])
        cropStart = dragXY[0]
        cropEnd = dragXY[-1]
        

    if event == "buttonRevert":
        window["sliderBrightness"].update(0)
        window["sliderContrast"].update(50)
        window["sliderSaturation"].update(50)

    if event == sg.WIN_CLOSED:
        break

window.close()