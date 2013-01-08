colorList = """
red
green
blue
white
black
gray
brown
yellow
orange
purple
pink
""".strip().split('\n')

def generate():
    random = ENVIRONMENT.random
    return colorList[random.randint(0, len(colorList)-1)]
