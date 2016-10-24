from PIL import Image, ImageTk
from random import choice

number2 = None
number4 = None
number8 = None
number16 = None
number32 = None
number64 = None
number128 = None
number256 = None
number512 = None
number1024 = None
number2048 = None


class NumberTile:
    def __init__(self, image, value):
        self.image = image
        self.value = value


def find_number(num):
    global number2, number4, number8, number16, number32, number64, number128, number256, number512, number1024 \
        , number2048
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
    elif num == 32:
        if number32 is None:
            image = Image.open("img/img_32.jpg")
            number32 = NumberTile(ImageTk.PhotoImage(image), 32)
        return number32
    elif num == 64:
        if number64 is None:
            image = Image.open("img/img_64.jpeg")
            number64 = NumberTile(ImageTk.PhotoImage(image), 64)
        return number64
    elif num == 128:
        if number128 is None:
            image = Image.open("img/img_128.jpg")
            number128 = NumberTile(ImageTk.PhotoImage(image), 128)
        return number128
    elif num == 256:
        if number256 is None:
            image = Image.open("img/img_256.jpg")
            number256 = NumberTile(ImageTk.PhotoImage(image), 256)
        return number256
    elif num == 512:
        if number512 is None:
            image = Image.open("img/img_512.jpg")
            number512 = NumberTile(ImageTk.PhotoImage(image), 512)
        return number512
    elif num == 1024:
        if number1024 is None:
            image = Image.open("img/img_1024.jpg")
            number1024 = NumberTile(ImageTk.PhotoImage(image), 1024)
        return number1024
    elif num == 2048:
        if number2048 is None:
            image = Image.open("img/img_2048.jpeg")
            number2048 = NumberTile(ImageTk.PhotoImage(image), 2048)
        return number2048


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
