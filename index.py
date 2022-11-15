from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import requests
import random
import web
import io
import re

# Configure the app
app = web.application(('(.*)', 'Quantum'), globals())
web.config.debug = False
host = "172.0.0.1"
port = 8080

# User-Agent for Tenor requests, it's nice to tell them who you are
headers = {
    'User-Agent': 'A Discord User',
}

class Quantum:
    @staticmethod
    def math_challenge():
        """Return a random math challenge"""
        # Create new image
        imgc = Image.new("RGBA", (450, 135), (255, 255, 255, 255))

        # Draw text on the image
        draw = ImageDraw.Draw(imgc)
        font = ImageFont.truetype("impact.ttf", 32)
        draw.text((450 / 2, 10), f"Math challenge (99% fail):", (255, 255, 255), font=font, anchor="ma",
                  stroke_width=2, stroke_fill=(0, 0, 0))

        # Generate a random math challenge
        num_a = random.randint(2, 6)
        num_b = int(random.randint(3, 12) * num_a)
        num_c = random.randint(3, 24)

        # Draw the math challenge as text
        font = ImageFont.truetype("impact.ttf", 64)
        draw.text((450 / 2, 50), f"{num_b} / {num_a} + {num_c}", (255, 255, 255), font=font, anchor="ma",
                  stroke_width=2, stroke_fill=(0, 0, 0))

        # Return the image to the client
        out = io.BytesIO()
        imgc.save(out, "PNG")
        return out.getvalue()
    

    def handle_request(self, name):
        try:

            # Math challenge
            if re.search(r'^/(math|math_?challenge)/?[A-Za-z0-9_-]*$', name):
                web.header('Cache-Control', 'no-store')
                return self.math_challenge()

        except Exception as e:
            """We catch Exceptions because we want to show the default image instead of an error page"""
            print(e)

    def GET(self, name):
        """Handle a request"""
        web.header('Content-type', 'image/png')
        # Return default image if one was not generated
        return self.handle_request(name) or self.default_response()


if __name__ == "__main__":
    web.httpserver.runsimple(app.wsgifunc(), (host, port))

    #http://178.189.203.225:8080/mathchallenge
