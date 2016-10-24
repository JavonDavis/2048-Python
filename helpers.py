from PIL import Image, ImageTk
from random import choice

number2 = None
number4 = None
number8 = None
number16 = None


class NumberTile:
    def __init__(self, image, value):
        self.image = image
        self.value = value


def find_number(num):
    global number2,number4,number8,number16
    if num == 2:
        if number2 is None:
            image = Image.open("img/img_2.jpg")
            number2 = NumberTile(ImageTk.PhotoImage(image), 2)
        return number2
    elif num == 4:
        if number4 is None:
            image = Image.open("img/img_4.jpg")
            number4 = NumberTile(ImageTk.PhotoImage(image), 4)
        return number4
    elif num == 8:
        if number8 is None:
            image = Image.open("img/img_8.jpg")
            number8 = NumberTile(ImageTk.PhotoImage(image), 8)
        return number8
    elif num == 16:
        if number16 is None:
            image = Image.open("img/img_16.jpg")
            number16 = NumberTile(ImageTk.PhotoImage(image), 16)
        return number16


def random_number():
    global number2, number4
    if number2 is None:
        image2 = Image.open("img/img_2.jpg")
        number2 = NumberTile(ImageTk.PhotoImage(image2), 2)

    if number4 is None:
        image4 = Image.open("img/img_4.jpg")
        number4 = NumberTile(ImageTk.PhotoImage(image4), 4)

    number_choices = ['2'] * 95 + ['4'] * 5
    return number2 if choice(number_choices) == '2' else number4
