import requests
from PIL import Image, ImageTk
from io import BytesIO


class Logo:
    def __init__(self) -> None:
        self.url = None
        self.response = None
        self.character = "Felix"
        self.params = {"seed": self.character}
        self.logo = None
        self.fetch_logo()

    def fetch_avatar(self):
        self.url = f"https://api.multiavatar.com/{self.character}.png"
        self.response = requests.get(self.url)
        img = Image.open(BytesIO(self.response.content))
        return img

    def fetch_logo(self):
        image = Image.open("./logo/typing.png")
        resized_image = image.resize((100, 100), Image.ANTIALIAS)
        self.logo = ImageTk.PhotoImage(image=resized_image)
