from PIL import Image, ImageTk, ImageDraw, ImageFont
import numpy as np
import os


# print(os.listdir("C:/Windows/Fonts"))

class Watermark:
    def __init__(self, watermark_type, watermark_content=None):
        self.watermark_type = watermark_type
        self.watermark_content = watermark_content
        self.original_color = (255, 255, 255, 255)
        self.cur_color = self.original_color
        self.img = None
        self.font = "BAUHS93.TTF"

        if self.watermark_type == "Image":
            self.watermark_file = self.watermark_content
            self.img = Image.open(self.watermark_content)
            self.colored_img = self.img
            self.name = self.watermark_file.split("/")[-1]


        elif self.watermark_type == "Label":
            self.watermark_content = "Watermark-Text"
            self.name = self.watermark_content

    def color_image(self):
        photo_array = np.array(self.colored_img)
        color_selected_array = np.array(self.cur_color)
        sig_pixels = np.where(photo_array[:, :, -1] == 255)
        photo_array[sig_pixels] = color_selected_array
        print(photo_array[sig_pixels])
        self.colored_img = Image.fromarray(photo_array)

    def update_attributes(self, **kw):
        for key, value in kw.items():
            setattr(self, key, value)


class FinalImage:
    def __init__(self, photo_file):

        self.id = 0
        self.photo_file = photo_file
        self.img = Image.open(self.photo_file)
        self.name = photo_file.split("/")[-1]
        self.height = self.img.height
        self.width = self.img.width
        self.ratio = self.height / self.width
        self.size_factor = 1

        self.watermark_obj = None
        self.watermark_pos = (0, 0)

        self.final_img = self.img

    def add_watermark(self, watermark_obj):
        self.watermark_exists = True
        self.watermark_obj = watermark_obj

    def update_attributes(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def format_img(self):

        if self.watermark_obj.watermark_type == "Image":
            self.watermark = self.watermark_obj.colored_img
            watermark_height = int((self.img.width / 10) * self.size_factor)
            watermark_width = int(
                (self.watermark.width * (watermark_height / self.watermark.height)) * self.size_factor)
            watermark_image = self.watermark.resize((watermark_width, watermark_height))
            print("this is watermark info", self.watermark.height, watermark_height, self.watermark.width,
                  watermark_width)
            position = (int(self.watermark_pos[1] * (self.img.width - watermark_width)),
                        int(self.watermark_pos[0] * (self.img.height - watermark_height)),
                        )
            print("pos: ", position)
            print("image info: ", self.img.width, self.img.height)
            merged_image = Image.new("RGBA", self.img.size)

            merged_image.paste(self.img, (0, 0))
            merged_image.paste(watermark_image, position, watermark_image)

            self.final_img = merged_image

        if self.watermark_obj.watermark_type == "Label":
            combined_img = Image.open(self.photo_file)
            print(combined_img)
            draw = ImageDraw.Draw(combined_img)
            font_size = 100 * self.size_factor
            font = ImageFont.truetype(self.watermark_obj.font, font_size)
            width = draw.textlength(text=self.watermark_obj.watermark_content, font=font)
            # width= draw.textlength(text=self.watermark_obj.watermark_content)
            print("result", width)
            position = (int(self.watermark_pos[1] * (self.img.width - width - 20) + 10),
                        int(self.watermark_pos[0] * (self.img.height - font_size - 20) + 10),
                        )
            draw.text((position), text=self.watermark_obj.watermark_content, font=font,
                      fill=self.watermark_obj.cur_color)
            self.final_img = combined_img
            # ImageTk.PhotoImage(combined_img)





