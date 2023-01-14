import PySimpleGUI as sg

layout = [
    [sg.T("Button")]
]

window = sg.Window("Tasbirre", layout, resizable = True)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

window.close()