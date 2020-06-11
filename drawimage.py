from PIL import Image, ImageDraw, ImageFont
import random

# Create drawing slate with given noise
def create_bg(DIM, base, intensity, size, keepshade = True):
    img = Image.new('RGBA', (DIM[0], DIM[1]), base)
    if not intensity:
        return img
    d = ImageDraw.Draw(img)
    for x in range(round(DIM[0] / size)):
        for y in range(round(DIM[1] / size)):
            persistant = 1-(random.random() * intensity)
            shade = tuple(round(base[i] * persistant) if keepshade else round(base[i] * (1 - (random.random() * intensity))) for i in range(3))
            d.rectangle([size*x, size*y, size*(x+1), size*(y+1)], fill=shade)
    return img
    

# Add text to an image, return new image
def add_text(img, text, pos, font, fcolor):
    d = ImageDraw.Draw(img)
    d.text(pos, text, font=font, fill=fcolor)
    return img

# Draw an entire page, return image and correct text
def create_page(title, body, DIM, txtcolor, bgcolor, noise, noisequality, titlesize, bodysize, font):
    img = create_bg(DIM, bgcolor, noise, noisequality)
    titlefont = ImageFont.truetype(font, titlesize)
    bodyfont = ImageFont.truetype(font, bodysize)
    titlespaced, titleh = word_space(DIM, title, titlefont, DIM[1] - 40, spaceh=titlesize + 10)
    for i, line in enumerate(titlespaced):
        img = add_text(img, line, (50,(titlesize+10)*i+20),titlefont,txtcolor)
    bodyspaced, margin = word_space(DIM, body, bodyfont, DIM[1] - titleh - 60, spaceh=bodysize + 10)
    for i, line in enumerate(bodyspaced):
        img = add_text(img, line, (50,((bodysize + 10) * i) + titleh + 20), bodyfont, txtcolor)
    return img, titlespaced+bodyspaced

# Generate and return a given number of words
def generate_words(worddict, length):
    words = []
    for j in range(length):
        word = random.choice(worddict)
        print(word)
        mod = random.randint(1,10)
        if mod == 1:
            word = word.upper()
        elif mod == 2:
            word = word.capitalize()
        elif random.randint(1,15) == 1:
            word += "."
        words.append(word)
    return words
    
# Turn words into lines, based on size of page and font, then return lines and height of lines
def word_space(DIM, words, font, height, spaceh=30):
    linew = 0
    linet = "" 
    lines = []
    wordnum = 0
    while wordnum < len(words):
        if len(linet) > 0: linet += " " 
        linet += words[wordnum]
        if font.getsize(linet)[0] > DIM[0] - (2 * DIM[2]):
            if spaceh * (len(lines) + 1) > height:
                linet = linet[:-(len(words[wordnum]) + 1)]
                break
            else:
                linet = linet[:-(len(words[wordnum]) + 1)]
                if font.getsize(words[wordnum])[0] > DIM[0] - (2 * DIM[2]):
                    print("Word too long, skipping: " + words[wordnum])
                    wordnum += 1
                else:
                    lines.append(linet)
                    linet = ""
        else:
            wordnum += 1
    if linet:
        lines.append(linet)
        
    return lines, spaceh * len(lines)
