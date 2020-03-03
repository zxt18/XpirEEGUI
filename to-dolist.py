import PySimpleGUI as sg
from datetime import datetime
import re, datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

cred = credentials.Certificate('./serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'xpiree-a5ac6.appspot.com'
})

bucket =storage.bucket()
blob = bucket.blob('groceries.txt')
blob.download_to_filename('./groceries.txt')


def merge(list1, list2):
    merged_list = list(zip(list1, list2))
    return merged_list

def month_num_to_word(input_date):
    from datetime import datetime
    x: str = datetime.strptime(input_date, '%d-%m-%y').strftime("%d-%B-%y")
    return x

BG_COLOR = '#1B1B26'
INPUT_BG_COLOR = '#2C2C37'
BUTTON_BG_COLOR = BG_COLOR
TEXT_COLOR = '#FCFDFF'
file_name='groceries.txt';

with open(file_name) as f:
    content = f.read().splitlines()
    date = []
    grocery_items=[]
    for i in content :
        match=re.search('\d{2}-\d{2}-\d{2}',i)
        if (match):
            date_tmp= match.group()
            date.append(date_tmp);
        print(date)

        match_str=re.search('[^0-9]+', i)
        if match_str:
            grocery_items_tmp= match_str.group()
            grocery_items.append(grocery_items_tmp)
        print(grocery_items)
# dataList = [["Bananas", '09-March-20'], ["Apple", '04-March-20'], ["Pineapple", '04-March-20']]
x=[]
for i in date:
    x.append(month_num_to_word(i))

dataList=merge(grocery_items,x)


def zip_tuple_first(tup):
    b = zip(*tup)
    first_elem, second_elem = map(list, b)
    return first_elem


def zip_tuple_second(tup):
    b = zip(*tup)
    first_elem, second_elem = map(list, b)
    return second_elem


def the_gui():
    global dataList
    sg.theme_background_color(BG_COLOR)
    sg.theme_element_background_color(BG_COLOR)
    sg.theme_input_background_color(INPUT_BG_COLOR)
    sg.theme_input_text_color(TEXT_COLOR)
    sg.theme_text_color(TEXT_COLOR)
    sg.theme_button_color((TEXT_COLOR, BUTTON_BG_COLOR))
    sg.set_options(text_element_background_color=BG_COLOR)
    sg.set_options(border_width=0)

    def top_button(text, image_key, set_as_default=False):
        col = [[sg.Button(text, size=(46, 1), font='Helvetica 15 bold', button_color=(TEXT_COLOR, BG_COLOR))],
               [sg.Image(data=red_line,key=image_key, pad=(0, 0))]]
        return sg.Column(col, pad=(0, 0))

    task_col_1 = sg.Column([[sg.InputText('Enter Item Name', key='grocery_item', size=(22, 1),
                                          font='courier 16 italic'),
                             sg.InputText(default_text='DD-03-20', pad=(95, 0), key='expiration_dates', size=(25, 1),
                                          font='courier 16 italic')],
                            [sg.Listbox(values=zip_tuple_first(dataList), size=(26, 10), font='Helvetica 15',pad=((1,0),(15,0)),
                                        key="items_list_box",
                                        no_scrollbar=True),
                             sg.Listbox(values=zip_tuple_second(dataList), size=(18, 10), font='Helvetica 15',pad=((90,0),(15,0)),
                                        key="dates_list_box",
                                        no_scrollbar=True)],
                            [sg.Button(key='add_save',image_data=add_button),sg.Button(key='Delete',image_data=delete_button)]],key='-COL-TASKS-1')

    layout = [
        [top_button('Expiration List', '-L1-', True)],
        [task_col_1]
    ]

    window = sg.Window('Grocery List', layout, use_default_focus=False, size=(800, 480),no_titlebar=True)

    top_button_selected = 1
    while True:  # Event Loop
        event, values = window.read()
        window['-COL-TASKS-1'].update(visible=True)
        print(event, values)
        top_button_selected = 1;
        if event == "add_save":
            tuple_1 = (values['grocery_item'], month_num_to_word(values['expiration_dates']))
            dataList.append(tuple_1)
            dataList.sort(key=lambda L: datetime.datetime.strptime(L[1], '%d-%B-%y'))
            window.FindElement("items_list_box").Update(values=zip_tuple_first(dataList))
            window.FindElement("dates_list_box").Update(values=zip_tuple_second(dataList))
        elif event == "Delete":
            List = [(val, key) for (val, key) in dataList if val != values["items_list_box"][0]]
            dataList=List;
            dataList.sort(key=lambda L: datetime.datetime.strptime(L[1], '%d-%B-%y'))
            window.FindElement('items_list_box').Update(values=zip_tuple_first(dataList))
            window.FindElement('dates_list_box').Update(values=zip_tuple_second(dataList))
        elif event == "Edit":
            if values is not None:
                edit_val = values["items"][0]
                tasks.remove(values["items"][0])
                window.FindElement('items').Update(values=dataList[0])
                window.FindElement('grocery_item').Update(value=edit_val)
                window.FindElement('add_save').Update("Save")
            else:
                print(event, values);
        elif event == None:
            break
    window.Close()


if __name__ == '__main__':
    blank_line = b'iVBORw0KGgoAAAANSUhEUgAAAFgAAAAGCAMAAABwz6mBAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAMAUExURQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALMw9IgAAAEAdFJOU////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////wBT9wclAAAACXBIWXMAAA7DAAAOwwHHb6hkAAAAFUlEQVQoU2P4TyMwajAcDDWD//8HAKuCDg94rot1AAAAAElFTkSuQmCC'
    captcha_button = b'iVBORw0KGgoAAAANSUhEUgAAAHMAAAArCAMAAAB8QEdOAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAMAUExURQAAABYWGRQUHBYXHBcYHBgZGxkaHhcXIRkZIRoaIBwbIRwcIRwdIh4eIB0eIx0dJR4eJh8fKR8gJSAfJSAfJyAgIiAhJSAgJiIiJCEiJiQkJiAgKCEhKyIiKCIiKiIiLCMkKCQjKSQkKSQkKiYmKCUmKiQkLCQkLiYnLCYmLicoLCgnLSgnLygoKigpLSkoLioqLCkqLiwtLyYmMCgoMCgoMioqMCoqMioqNCssMCwrMSwrMywsMSwsMi4uMC0uMiwsNCwsNi4vNC4uNi4uOC8wNDAvNDAvNzAwMjAwNTAwNjIyNDEyNjQ0NjAwODAwOjIyODIyOjIyPDM0ODQzODQzOzQ1OTQ0OjY2ODU2OzQ0PDQ0PjY2PDY2Pjc4PTg3PTg3Pzg4Ojg4PTk4Pjk6Pzw8PjY2QDg4QDg4Qjo6QDo6Qjo6RDs8QDw7QDw8QTw9Qj4+QD0+Qj09RTw8Rj4+RD4+RkFBQ0FCRUNERkJBSUJCSkNESEZGS0VGTEpKTkhIUEtMUUxLUExNUU5PVE9QVFBRVVFRWVNUWVVWWlVVXVhYWlhZXVhYYFxcZF9gZGBfZGFiZmZmamxsbmtscW1uc21udHFydnJzeHJyenN0eXR1eXV1fXh5fXx8fnh4gH59gn+AhIGChYOEiIWGiYqKkoyNkoyMlJCQkpKRl5GSl5OUmZeXn5mYnZubo5yboZ2eoqGipKKiqqOkqaurrampsaytsq6utbCxtrO0uLS1ura2vre4vLi4urm6vby8vru8wby7wb2+wsHBxsXGysTEzMbHzMbGzsnKzcvM0czL0M3N0c7P1M7O1s/Q0s/Q1NDP1dDQ0tHS1tPU1tTU2tbX2dbX29fW3NfY3NnZ29nZ3dvc3tzd39ra4dra5Nzb4N3d4t3d5d/g4uHi5+Pk5uHh6ebn6efo7Onp6+jp7ezs7unp8err8Ovr8+vs8O3u8ezs9O/w9PDw8vDx9vP09vT09vLz+PP0+PTz+PX2+vb3/Pf4/fn5/vv8//z7//7+/gAAAFDaIzYAAAEAdFJOU////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////wBT9wclAAAACXBIWXMAAA7DAAAOwwHHb6hkAAAG1UlEQVRYR72YDXgbZR3Ai+IUmF1FoBtZk7qapAkb2fXey13W3u4ud1lZd1566bauSTuRDrqVjoIMqw46GHaWMRXUgc5PwPmt42N8jO91aGGPDhUUC0MUdUYmAeLQshv/8H+Ta7KSdGzPQ/jlefrk7t78f/e+9977/7+tyOTxst4ywbJely2hTDidHsLzapmQZZknHtuUd3p4OXupPNDgKmpzrpzTR3j7annhc33NOqmyjN3Mw/vyTlZRNEQpPwI7O+f0UiM9IeQulBU265wtRPG7QMmdLiOaJuBLU4Eji53MKt8TJ3a0YrYStaX2+fIicK5MhUuLCvg4UYl/5Umfdx86mN5MBU7afA9lMffhJU+wJ+IxYwrr4qKKVxNwMFguyrGXe12Xc7kpLggaMYjHaCamQYxmH2lsVrxK1MtiHwQXl4iyXDbo0Qga/niSU5bFHLWdem2939/qUhIXxTQtmqDCGLo5VolpnFfgOLxhTmg2zl9G5vJzlzUajc09shyLYWtN4Lwa3i0XW23HLXAMZ5ipjazrqGcSKMEVWvgIK3B415rR45DJh0yDR+grLp/haSTn9zpmOJY1qsYZhgub4eRIsALemcJ90I5b4BhOXQ+HGH9knQ9/fFEiqiVWX0y7Ks8w+bhJujzoo0sXUc1lvMPXOLfLjHtI89zPrY7iaHBKIoF3yCYupu/gZI7h9Le0+v1t0vtVwyBOp8fHO2d4VFMlXWJNXUhk3KFImPGHxKDYfk710qXB9kDLokBLZ+AUucqjYnYiPhLvIlUOnx23QAmnrRTDp9d36OGOVYbB+9TeuNMR/7TqJIYRnsMs193+C+oi7RLTFJFqFoita8Xq4McW1H1S/OjaFucVvUQ2cdANnpim2mPHLWA7ffS52NhKsTPYEq7s/8lTL/3mBz3vc5jxb9z/2LdIlRza/ewfn37oluEP7Bp95g979/5+31B194//lH7ql2uq1z35aPfSmg2P7exVZfKl/b/eWuXgPcVZA8dAVUs7A62hU67eA6/vB7hnEyHyToCfmXJ81gvw3N8B/jY8+k+AQ4fG/3vJ4AgkXwBrb/upAN0L2nvhpa4qR3ynBXfEiYE5+e3YTr6gzDulVr1+u/XMmtot+2BrDRM5/KqV7A7Pak3CZ88c+C3cNn9hwxhsbmhY9PPxsQtahv8CX2kat7rn6OvhxZVMsC+VOvx6/8ppYd0OW+AYzrbpYeaAtUNqn/O1n36xb+XW9K7RN24W+5h0amgJsyN9O7Ow6VnYLDVNH/v/ju7ASTd+7yb3m3DNWnEIDp6+puUm695HrBuquzum22EL2E4hP4UKcygSqQmm4Wr38tMWu89l3CPw5Zth5GTdDy9+/YZvHoBbgpI4BtdLTd0WXD9v3oULP37e2Rb8G8CCA5I+7QHYtg1G3LpfL1o+7Tl0tHNCWqfXdx6EVf3u5W2VfdLy/8ElA6nx9SH/AUhj3D3BYFjcj05xEQ722Z+49KRPzVwBqYcfvGt3KqlXDkFK6ng5vb5yWvuJOFsrO1oPjm+qZpoGb/yCdCuk7h4B6/uhy96wfvHD727owldQ3g9bZHHxv2Djinlnbv7q5pkAKxoWDsJ426zb0skRbP5tJhI6EWebJNXeCfescV85CtuYkdSRIzAOu88SX/nP5309zhnxCee0hw49+OFLB34H31liwfyZ53XAmC6NQvpI6lXYo0snNrb91aGhJIzctw/GVl0G0Fc7ZyAJw9JfYZMQpclWU56HLYq8aBBe+/OPUtbTSxpeG//M/HkbIR0ZsJLXRPThl63BSv9xOPO5zAySNt+1/7AOw6+uCmyHu+v0lYF9sC3yCiQwT2mYxahTkztPGxrDmfPElUsDb4IkLd6YTrZvh13ucHXwcbi1PzCVc1KSy+drgVeMWOd1Vxk+XDPy2K3yqLjGXXHdBmJfLsJuVoBWBkJ2vS0BvRiNYS4TtFhxepiA1hhKIlY6RCloAWRO7aS1CqZmmoOnjMlqCY1lucLDeSeok0NnyV/QwoVasVDiuOIaw4YmS9rEPjw+2EyFd2ongkocXftkETF2NhfFWsQ+fEeoitZgpZy2UChRRU0iW/1PPQxF4MgptNZ0FmccOVvt5KBbuKOn7iR41cC6wD44DnBPKBMnOkvM9Ik4BgplLFByR8UQ3ueRTZXWR8dF1unAvYODN1GR2w2Xi1yhqBLZ4B3ZfRl5D3aeWSv10h0oOl04CeiMsR90GaCFPzVoysT+M+OyfWWz4nueneJRjiqzzgyW6tmaP9eiHNhWL7XlnBkXXY3K58Tg2RUtp7Sd1IrbHrvJuw4NLBT+LzXhxAEu49DiDGInjJnMW4afJfH6bdHpAAAAAElFTkSuQmCC'
    green_button = b'iVBORw0KGgoAAAANSUhEUgAAABMAAAAWCAMAAAAVQ1dNAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAMAUExURQAAABR4Rh91SB15Rhp5TSV3RyZ8SyV6Ux6HTCaDTiqHWyyDWCiKUSuTViiXVSicWzODXD2BXDCaWjKbYzyZYDKjYTGjaDelaDGoZDmrbzyqazumcj+wcD25cTnCdD3BdTTUcjLeeDrcdT3feDPgbTLiczLjdzPlczDkdjbkdTfldjTmdjXndzPkeDHneTbmeTXmejblfDblfjTnfzXudzHpejHofDfofDTofTXseDnldTnkdzrmdjjmdz/gdj7idT3jdz3mcz3ldjzkdzzmdTvhfTrjfDnifTrjfjrkeTrleznkfjrnfj7heD3ieTzjej3kejzmeT/odT7pdzroeTjoezzoeDzufkCAZUaJZk2SdVSPeUWrakKpcUmkeE23d0DJd0bLfEjCdUrNf0DddEXce0TefkXff0jdd0/cfk3ffUHic0DidUPkckDkc0Pmc0LkdEPldkLmdULmdkDjekHjfEPleEDoeTbmgTvlgjjngDzkgjzsgEi7glu6gl29j26+m0fOgkvEgUrMhk3Lgk3KhkzMgUzOhEzKiELYgUnQgUrTg0jWgkvWhU/ShE3VgE3VgU3UhU3XiUjbgEvagkrag0jfgkjehUjciE/YiFLGiVHLglLJh1LOhlDNi1LNjFfOjFjLhlzMhFnMi1PRh1TUgVbVjlXagVLZjFnTilLckVfbkFvalUPjg0PhhEPghUHihEPihULkgUDmgkDlhkPkh0PnhELmhUXhgEXggkTigUXjhETihUXjhkfih0Tkgkbkg0TkhETiiUfki0HrgUvig0jmh0/gg0zgiFDmjFvjj1LmkFjjkFrokmLGlGfDkGbPl2rCmGPYkmbZnmbgkwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACXBECsAAAEAdFJOU////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////wBT9wclAAAACXBIWXMAAA7DAAAOwwHHb6hkAAABQ0lEQVQoU2P4H8X+Hw0w/K+vlWSGcqCA4f+FNcviRVihXDBg+L94Us+VRTE8UD4IMPxfMn1H5vKlSRIcUBGQ2MSDR1Iyso5PleeDCgHFul31ywtzSrbtS5ThgonNdNdQcQzW0q0+sWKeGCNErHGLQZiLlbae0brp6zvl+MFizVsNA52sdEyNN6xVqzmQIMoGFOs45O3nYK1vVrFxk6VJwOSVdYIgMQ9fe2dbi6o9u1TVladcOh/J8L91n5tdtr2Nuc/OaQrHzs6NFQDqbdnrn5Od5xLqlT7lzOomYbAdbbutC3Lzg0I8UycskGaBuCV5v7VLUXFZaVr/Qm6QCEisa7tauKbS0VOzhSAiILH2w5WKm0/2SXFCRUBis1bNON0rywvlgwDD/3OX588Rh/IggOF/w8U4JigHChj+R0dAmVDw/z8AkbkcWUjJmvYAAAAASUVORK5CYII='
    plus_button = b'iVBORw0KGgoAAAANSUhEUgAAABoAAAAYCAMAAADTXB33AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAMAUExURQAAAAsbGAUpHQ01Kgo9KhUlIhEjLREqLxkpKB4qKhwtKR4sMBwsORI2KBE2LhY1LRA4LRkwJh00JBsxLh4xLR00Lhs+KBw9LBY3MBk2NB4yOx46MSAfJSEdKjMdLDgfMiM0GSM7GSEnJyAjKiMjLSMmKyUkLSAtJiIpLSIsLSUpLSUuKyglLS4kLCkoLiosKSgtLi4sLyIlMSUjMCYmMCAqMSMpNSYqMScrNCYuMSUtNCQtOCkmMSklNC0nMSkpMioqNCktMikuNS0qMS0qNS0tMSwsNSktOC4uOC0vPCI0JCQ4LSc8LSAxMSEwNSA0MiYwMSUzNCU1MSY2NCEyOiA1OiYwOSc1PiM6MiM5NiA+NCY4MiY7NiU9NyA/OSkxNCk1Ni4yMy4wNCgyOSk2PS8yOS43Pio5My05Oi45PzMnJzUmKzEqLjgpJjUjMzEqMjErNTAuMTEuNjUpMzQvMzYvNzQsODspNzksOz81KTEwNTY5MjU7Ny01QDE6RAJRMQ9XMhtNKh1DNhdZPh5VPg5kJQlmNxVhMCJCNyVANyRCOCZJMyZOMydOOSdOPClAOi9MNihKPC1JPS1NPiVXJCFZKCVUMi9YOCxdPTJAMDRAMjBEOTFSPzhRNDRpOxVeQQ1/QRltSy1ARylFSC9fRy9ZSzFQSDJcRiZiSSBtTS5qSCRxQzNlQDZjTzthVDB6STp2UkJrXURvXEh2XB+KOiicVTSGRDWMVTiIUz6QXzqdbjWgXDKzVjyyXjSlZzK6Zj2+azfDYj3LdzvbbTHXczjYdC/ibTXmdDvrfj/pfD/wfkWaVlGMXEGNZ0uObUKbZUWbbkqQa0mSdFaJaFCTcFeZfUGiXUSpZ0C6cUjDckDVd0PbdkXadkPeeUXff1LBf0HsejjPgD/eimWwkUrKjU/XjUnfhk3YhUvcj03UklbLh1rPi1jEkFvOlV7JlV3NlVPXg1TYhVvZhVvcgkfjgErnjlDngFHljVfhlmbKlmrDl2zLk2DQmGnWk3PelgAAAEiibAcAAAEAdFJOU////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////wBT9wclAAAACXBIWXMAAA7DAAAOwwHHb6hkAAACNElEQVQoU2P4Dwc5/3Ny8p311KDc/1ApHR0958JCQ9eiqiJnG6gkRMquqCop0UDJwMBAz965oMgELAiWcnbWU9UMCg6Kjg4KcHR2cXOxV4FIqdmUudhb+opKd3R1xgbHu7kVubmB5Bj+q9gDWfEZkfxNSzeuW9YfHOBW5ACWY/iv5uDhoaEVwMW74tLjq5smiXBqxms5eLiZ/GcwcbB3CkuTKakWa3vy8v2GCT7egjFWDvYODiYM9g727qYpWjWzpi14+OjpjjU93eIRlg5AYMLg4OaQapIQtXzG+q2Hnj3fvX31qjnpjm4g2xgcPBw8Uv1bzu68fuDWl3v7b+y7sHk20JUgKTcPh6QMgYVvXn+8e/L4iSNfX7y9Mjnew83DwwEkFR/MvPLn30+3Hxw7dfT7jz/nJiZAdbnZO1mJ9F0+c3rP4cPf9l47f3FtbLwbyK8gKTcPJ+2ZClO2HLzzedvUxl5pXyc3V5CUmpubg6eDblalYuvND//mzfUK4vZztAcCNYb/9m5O1u5l2bkK7fdf/Z4+Uz0hNNwCZB5QSs3enUcqRVNfqGHXu19LJklKsrNZuXm42YNC3sQ6RCqUOymdZX59M5Ow5OJFde4ebg6Q+DJ3t0o2Ly7lkOCL43TiNpWVBcuApZT1NDJc5fJsMv2SyypcPCoqXOyBomCp/1ysQUly8i511kZ5eTr2hUWQxAGW4mTkTCqvsDWrNaqocEt01gHLQKQgwNjIwQGWmv7///8fAJ7/NhA3zMv/AAAAAElFTkSuQmCC'
    red_line=b'iVBORw0KGgoAAAANSUhEUgAAAtoAAAADCAIAAAAiIj+qAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAArSURBVFhH7dYxAQAwDMOwdPxxjdb6jEMe6TEFz80LAEDP+QUAKLEjAEBVstS1Acsj8gf3AAAAAElFTkSuQmCC'
    red_button = b'iVBORw0KGgoAAAANSUhEUgAAABYAAAAVCAMAAAB1/u6nAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAMAUExURQAAAF0jPF0mO18lPWEYM2EbNWAcM2AfN2QZN2cbNWQeNmEdOWAdPGYaOGQdO2oTNWoVNmwXOGgcNmwZN2gbO2keOmkePG0YOGwdOm4ePXAKL3MKMnMPNXAXNXIXNnIXOHAaPXEcOXIdOnIfOXUZOXcZPXYcOHYdPXwTO3oZPHocPnofPn0ZPWEjOGEhPGQiPWQkPGkgO2ohPGwiO2wgPG0hP2wkPHAgO3YgPXUZQH8bQWwmQGwrQ4cOO4QQNYMWPYAXP4UXPIEdP4UaPYYdPooTO4sVPZMPN5YYPoMdQocfRIsWQYkbQIocQ4geRI0YQo8bQo4aRJsOQpAQQJEUQJUXQpYWRpIZQpUbQpYeRJMbSJIfSpgUQp0VQ5wXRpkaQ5gbRZ4ZRoAhQYUiQYwjS5UhRqQPRqsMRKYSRKEYRqEZSaYeTqsTRqgURK0XR6kSSakVSa0VSK8ZR6sbTKwYSq8bTb0MQ7IQQrAURLAWTLEaT7oTR7oVTb0VSb0VTrkcT70ZTr4ZUaIgTq8gTKYgUqogUakkU6klVLMgVLcjV7MkWbQkWbkjU7ojWMIOS8ENTMUPTMQSTs8TTcUSUMUXVMYeWc0XVMgbUcodVc0ZVMsdWM4aWdcMTNIOUNsPVtYQTdIWU9AWVdQSVdUUU9QVWNAaVdAdVdcaVNMZWNYZW9kSU9sSVtoWVd4RUt0VWN8ZVtsaWdgfWdwaWd8eYcEgUscjWMggW8siWc8gW9MhX9YgXdUjYeMHUeIIVOMMUOoOVu0KVOwPVOgOWO8OWuMRVeMRWOUQWOcWWuQZWOQdXugRV+gWV+4TV+oSWusUWeoVXOwQWO4VWegaWukYXOoYX/IKVfYJVvYMV/ENWPMMWvAOWPMPWvANXPYJWPUNWPYPX/8GVvoHWf8CWv8EWP8EWv4GWP8HW/8FXfoIVfwKVvkKWfkMWfkOXf4JWf4KXP0NXPERWvASXfQQW/YWX/kQX/4QXOEeYukXYO0bYv8OYvYSYfUUYPIYYuIjZucgYQAAAAr+GkYAAAEAdFJOU////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////wBT9wclAAAACXBIWXMAAA7DAAAOwwHHb6hkAAABy0lEQVQoU2P4zyjCL2D0HwG4OFn+/2f4Lx6dnRUgBxX7r5ycmuonDhR26N69ojFRTRckKOSYN2Pp9jat/wx6Udu+H76yI17W4P9/E5/CVZ9vnewECouFzb7/5OefhlAvdRXf0gX33r293KH+n4HPdsqv589frdlaHBdTMvPc2yfv1zWZAs2WKZh3992z/f8WTp648Pint2/P1ngyA4W57dPn/npz9cP5Y8fO3rv76sK0GF6QA///18ycef7NtVsf7l17+/XD4gwnoBBImCmpZNG9t6/fv3384OqccjdDqPB/s5i+A+/evn379MW+MndFkAhY2Dx2woF3D54+fXtvbbWHEkxYIrxm9Q2g2pf3Lq6f3uwMCiCgsGho3bqPt699vX7w9KUTa5bl+IuBhPUDJx96/+7ehSPzJy0/ceb66z393jxAYavKY++ePzy1obaiaMvGcw+ePNmbb/mfgTdoyZfnb87P7Il0cY6o3/T60fM3U7z/MwimLbpz88euXDsLM2PthJojb96drXNjY+AInvp386wSVxXW///Z5UNqVn7b2aoDNFujpbcqzlHRBuTc/8KB2V3tKaJAYTFVaSl1a7AgEOhJKkhy//8PAMoKLCsLw4FtAAAAAElFTkSuQmCC'
    yellow_button = b'iVBORw0KGgoAAAANSUhEUgAAABIAAAASCAMAAABhEH5lAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAMAUExURQAAALWfL7+lN7esQrinS72mSbirQrmqQ7+oSr2nUsGmPcGlQcOnRMCnSsKnU8OmVsOmWMGnWsGoUcGpU8OqWsSjYMSnY8GoZs2sae/WPvfOJvbPKvrOJfjPKfzMKv/PK/PON/PPPfLOP//HNf/HP/rPM/vMNv3KMf7LMv3KM//LNv/NMP3MMf/MM/7OMP/NNf7ON/jLOvrJPvrOOf/LOf/IPP/LPP/KPf/KPv/MOv/MO//MPP/MPv7OPP/PPf3PPv/OP/PSL/bRK/DYLv/RL//SLfPWMPPVNfHWNPLWNfLWN/fTNPfTN/XVNPXUNfXUN/PUPPPUPvbSOfXSPPbSPvfTP/XUOfDYMPnTNP/RMP3RMv/SMP7SM//RNvrROfnRO/nSOfrQPPnRPv3QOfzQO9nAWe/MTOnPVu3OUezOUunOXe3MWO3QRu/URe/TTu7US+7UTO3ZRufRWe/SVO7WUu/RWfXHTfXLQfXLRfXMQPbJSPXPSP3HQP7GQf/FR//HR//ESP/GSf/GSv/HS//HTPvLQ/nPRfrOR//KQP/KQv/JRP/JRf/IR//KRP/KRf/LRv/LR/7NQP/MQv/MQ/zOQPzOQv/MRP3MRf7ORP/ORfzOR/rOSfrOS/nOTv/JSP/ISf/JS/zLSP/KSfzLSv/JTv7LTP3LTvzNSfzNS/PPVPfOWvfOXPbOXf/GUP/GUv/FVP/GVP/HVvrLVfnNUPrMUv/IUP7KUP/LUf7IVP7JV/3KV/vLXfjNXP/IXv3LXPPSRfDWQ/bRQvbQRPbQRfbQR/bWR/TSSvbVSvHZQ/nQQPnQRPjUSPrWTvzQS/PQUPPRU/DTU/LQVPLTVPXTVffTWOTMaubMa+zFYO/Hb+/KYO/PYu/Ia+DOfOfRbu3TZO7SbvPFZ/bJbPTNbvrKY/jMYfPMcfPTZPLUYvfQZ/TRafbVavLRcgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAN+7z/YAAAEAdFJOU////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////wBT9wclAAAACXBIWXMAAA7DAAAOwwHHb6hkAAABYUlEQVQoUwFWAan+AP8LCgUEAwYIDQYHCQ4MAgH//wBlz8bQdHHIx8sZwNPUzMVtcv8A6ngxeSFBQi4rGhsxMiYlUtAUAOihPJeUXEQvLR8uNyQjJ2PTEADhuKC4t5mTn5+Jj7GvgH2FrBUA4K6CuLijoq2tfqS9vbWep6wYAOSijaadw8qlpZqcurmilcnRDwC8ljuHxFFQyoZUwbOzlV9SbhIAqpEwyVFIV09WSErDw19LSG8SAKuRMGJTV0NOTkZJwsJgS05wEwDjkDuYwU9NX2FMU5uolF9TcxEA44w4kJdfXpKSP5W2to09YtERAL6KNYyQPDyMgY6isK+LO2TODgC7jTQ4ODo2f4GKi4SDiDuUqQ8A181jW0VZMJKWQDkqKCwze9oWAOtmIB0cHil8fZg+XVpYVdLfFwD/db9STGKHtLJ2enciImxn1f8A/9ZqaWhr2dvY5eLp5ufe3dz/ZdGaljRkmtwAAAAASUVORK5CYII='
    add_button=b'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'
    delete_button=b'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'
    the_gui()
