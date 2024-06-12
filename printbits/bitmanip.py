from PIL import Image
from reedsolo import RSCodec


class BitConversion:
    def __init__(self, dpi: int, width: float, length: float, margin: float, bitsize: int = 3, ecc_symbols: int = 10):
        """
        Initialize a new BitConversion class.
        :param dpi: The DPI of the printer (i.e. 300 or 600)
        :param width: The width, in inches, of the paper.
        :param length: The length, in inches, of the paper.
        :param margin: The minimum margin, in inches, for the printer (i.e. 0.5).
        :param bitsize: The size of each bit (default 3 - each bit is represented by 3x3 dots).
        :param ecc_symbols: The amount of error correction symbols to use
        """
        self.dimensions = (int((width - margin) * dpi), int((length - margin) * dpi))
        if self.dimensions[1] < 100 or self.dimensions[0] < 10:
            raise ValueError(f"Provided parameters have too-small dimensions {self.dimensions[0]}x{self.dimensions[1]}")
        self.bitsize = bitsize
        self.rsc = RSCodec(ecc_symbols)

    def encode_image(self, data: bytes) -> Image.Image:
        """
        Gets a printable image of the provided bits.
        :param data: The data to be converted to an image.
        :return: A PIL.Image.Image object to be printed.
        """
        encoded_data = self.rsc.encode(data)

        image = Image.new('1', self.dimensions, 1)
        image_capacity = (self.dimensions[0] * (self.dimensions[1] - 8)) // (self.bitsize ** 2)

        if image_capacity < len(encoded_data) * 8:
            raise OverflowError("Image capacity is smaller than the size of the encoded data")

        x, y = 0, 0
        for byte in encoded_data:
            for i in range(8):
                bit = (byte >> (7 - i)) & 1
                for dx in range(self.bitsize):
                    for dy in range(self.bitsize):
                        if x + dx < self.dimensions[0] and y + dy < self.dimensions[1]:
                            image.putpixel((x + dx, y + dy), bit)

                x += self.bitsize
                if x >= self.dimensions[0]:
                    x = 0
                    y += self.bitsize
                    if y >= self.dimensions[1]:
                        break

        watermark = Image.open("printbits.png").convert('1')
        watermark = watermark.resize((self.dimensions[0], 8))
        image.paste(watermark, (0, self.dimensions[1] - 8))

        return image

    def decode_image(self, image: Image.Image) -> bytes:
        pass
