# Command-line arguments and other functionalities
import os
import sys
import math
import random
import ast
import argparse

# Image handling and OCR
import readimage
import drawimage
import distance

# Constants
DIMENSIONS = [850, 1100, 50, 50] # Width, Height, Side Margin, Top Margin
DICTLOC = "dict.txt"
COLORS = {
    "R" : ((255,0,0), "Red"),
    "G" : ((0,255,0), "Green"),
    "W" : ((255,255,255), "White"),
    "B" : ((0,0,0), "Black"),
    "Y1" : ((255,252,239), "Yellow1"),
    "Y2" : ((255,247,218), "Yellow2"),
    "Y3" : ((255,237,176), "Yellow3"),
    "Y4" : ((255,229,139), "Yellow4"),
}

# Read command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--pages", type=int, help="Pages per Setting", default=1)
parser.add_argument("-f", "--fonts", nargs="+", help="Space seperated List of fonts", default=["freefont/FreeMono.ttf"])
parser.add_argument("-tc", "--txtcolors", nargs="+", help="Space seperated Color Initials", default=["B"])
parser.add_argument("-bc", "--bgcolors", nargs="+", help="Space seperated Color Initials", default=["W"])
parser.add_argument("-hs", "--headsizes", nargs="+", type=int, help="Space seperated Header Font Heights", default=[50])
parser.add_argument("-bs", "--bodysizes", nargs="+", type=int, help="Space seperated Body Font Heights", default=[25])
parser.add_argument("-v", "--verbose", help="Print progress", action="store_true")
parser.add_argument("-n", "--noises", nargs="+", type=float, help="Background noises, 0 to 1", default=[0])
parser.add_argument("-nq", "--noisequalities", nargs="+", type=int, help="Bg noise tile sizes", default=[2])
parser.add_argument("-ao", "--avgout", type=str, help="Filename to output avg results to", default="avgout.txt")
parser.add_argument("-fo", "--fullout", type=str, help="Filename to output full results to", default="fullout.txt")


args = parser.parse_args()
pages = args.pages
fonts = args.fonts
txtcolors = [COLORS[c] for c in args.txtcolors]
bgcolors = [COLORS[c] for c in args.bgcolors]
headsizes = args.headsizes
bodysizes = args.bodysizes
noises = args.noises
noisequalities = args.noisequalities
verbose = args.verbose
fulloutl = args.fullout
avgoutl = args.avgout


# Grab dictionary as list of words
worddict = open(DICTLOC).read()
worddict = worddict.split("\n")

def image_stats(file, correct, language="eng", tessconfig=""):
    tess = {}
    tess_out, tess["time"] = readimage.tess_ocr("img.png")
    tess_out = " ".join(tess_out.split()).strip()
    tess["dist"] = distance.dist(correct, tess_out)
    tess["per"] = round((len(correct) - tess["dist"]) / len(correct), 4)
    tess["tpc"] = round(tess["time"] / len(correct)*1000, 4)

    cune = {}
    cune_out, cune["time"] = readimage.cune_ocr("img.png")
    cune_out = " ".join(cune_out.split()).strip()
    cune["dist"] = distance.dist(correct, cune_out)
    cune["per"] = round((len(correct) - cune["dist"]) / len(correct),4)
    cune["tpc"] = round(cune["time"] / len(correct)*1000, 4)
    return tess, cune

def main():
    if os.path.exists(fulloutl):
        os.remove(fulloutl)
    if os.path.exists(avgoutl):
        os.remove(avgoutl)
    fullout = open(fulloutl, mode='a')
    fullout.write("Font\tTxt Color\tBg Color\tNoise\tNoise Quality\tSize\tTime\t\tTime per Character\t\tErrors\t\tAccuracy\n")
    fullout.write("\t\t\t\t\t\tCuneiform\tTesseract\tCuneiform\tTesseract\tCuneiform\tTesseract\tCuneiform\tTesseract\n")
    avgout = open(avgoutl, mode='a')
    avgout.write("Font\tTxt Color\tBg Color\tNoise\tNoise Quality\tSize\tTime\t\tTime per Character\t\tErrors\t\tAccuracy\n")
    avgout.write("\t\t\t\t\t\tCuneiform\tTesseract\tCuneiform\tTesseract\tCuneiform\tTesseract\tCuneiform\tTesseract\n")

    for font in fonts:
        for txtcolor in txtcolors:
            for bgcolor in bgcolors:
                for noise in noises:
                    for noisequality in noisequalities:
                        for headsize in headsizes:
                            for bodysize in bodysizes:
                                cune_stats = []
                                tess_stats = []
                                avgout.write(f"{font}\t{txtcolor[1]}\t{bgcolor[1]}\t{noise}\t{noisequality}\t{bodysize}")
                                for page in range(pages):
                                    fullout.write(f"{font}\t{txtcolor[1]}\t{bgcolor[1]}\t{noise}\t{noisequality}\t{bodysize}")
                                    title = drawimage.generate_words(worddict, random.randint(1,10))
                                    body = drawimage.generate_words(worddict, 10000)
                                    img, correct = drawimage.create_page(title, body, DIMENSIONS, txtcolor[0], bgcolor[0], noise, noisequality, headsize, bodysize, font)
                                    img.save("img.png")
                                    correct = " ".join(correct).replace("\n", " ")
                                    tess, cune = image_stats("img.png", correct)
                                    tess_stats.append(tess)
                                    cune_stats.append(cune)
                                    fullout.write(f"\t{cune['time']}\t{tess['time']}\t{cune['tpc']}\t{tess['tpc']}\t{cune['dist']}\t{tess['dist']}\t{cune['per']}\t{tess['per']}\n")
                                cune = {}
                                tess = {}
                                for stat in cune_stats[0]:
                                    cune[stat] = round(sum([i[stat] for i in cune_stats]) / len(cune_stats), 4)
                                    tess[stat] = round(sum([i[stat] for i in tess_stats]) / len(tess_stats), 4)
                                avgout.write(f"\t{cune['time']}\t{tess['time']}\t{cune['tpc']}\t{tess['tpc']}\t{cune['dist']}\t{tess['dist']}\t{cune['per']}\t{tess['per']}\n")
    fullout.close()
    avgout.close()
if __name__ == "__main__":
    main()
    
