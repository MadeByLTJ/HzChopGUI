from PIL import Image, ImageDraw

def draw_hzchop_logo(output_path="logo.png"):
    width, height = 320, 180
    bg_color = (255, 255, 255, 0)
    line_color = "#000000"
    line_width = 8
    
    img = Image.new("RGBA", (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    draw.line([(50, 30), (10, 150)], fill=line_color, width=line_width)
    draw.line([(10, 150), (150, 150)], fill=line_color, width=line_width)
    draw.line([(110, 30), (310, 30)], fill=line_color, width=line_width)
    draw.line([(190, 30), (150, 150)], fill=line_color, width=line_width)
    draw.line([(310, 30), (270, 150)], fill=line_color, width=line_width)
    draw.line([(210, 150), (270, 150)], fill=line_color, width=line_width)

    img.save(output_path)

if __name__ == "__main__":
    draw_hzchop_logo()
