import requests
from PIL import Image, ImageTk
from io import BytesIO


class Logo:
    def __init__(self) -> None:
        self.url = None
        self.response = None
        self.character = "Felix"
        self.params = {"seed": self.character}
        self.pencil_image = None
        self.avatar = None
        self.background = None
        self.container = None
        self.fetch_pencil_image()
        self.fetch_avatar()
        self.fetch_background()
        self.fetch_text_container()

    def fetch_avatar(self):
        self.url = f"https://api.multiavatar.com/{self.character}.png"
        self.response = requests.get(self.url)
        img = Image.open(BytesIO(self.response.content))
        resized_image = img.resize((100, 100), Image.LANCZOS)
        self.avatar = ImageTk.PhotoImage(image=resized_image)
        

    def fetch_pencil_image(self):
        image = Image.open("./logo/feather.png")
        resized_image = image.resize((50, 70), Image.LANCZOS)
        self.pencil_image = ImageTk.PhotoImage(image=resized_image)

    def fetch_background(self):
        image = Image.open("./logo/background.jpg")
        resized_image = image.resize((700, 300), Image.LANCZOS)
        self.background = ImageTk.PhotoImage(image=resized_image)
        
    def fetch_text_container(self):
        image = Image.open("./logo/container.png")
        resized_image = image.resize((50, 50), Image.LANCZOS)
        self.container = ImageTk.PhotoImage(image=resized_image)

if __name__ == "__main__":
    logo = Logo()
    logo.fetch_background()