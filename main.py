from PIL import Image, ImageFont, ImageDraw
import random
import os

island_route = os.listdir('./Input/')

traits = ["Background", "Islands", "Rivers", "Top Decor"]


def get_traits(traits):
    trait_array = []
    for trait in traits:
        split_file_name = trait.split("#")
        split_rarity = split_file_name[1]
        rarity = split_rarity.split(".")[0]

        trait = [split_file_name[0], int(rarity)]
        trait_array.append(trait)

    return trait_array


def choose_traits(trait_route):
    traits = get_traits(trait_route)
    choice_trait = random.choices(population=traits, weights=[item[1] for item in traits], k=1)

    return choice_trait[0]


def get_trait_image(route, trait_type, trait):
    return Image.open(
        os.path.dirname(os.path.realpath(__file__)) + route + trait_type + str(trait[0]) + "#" +
        str(trait[1]) + ".png")


def gen_nft_name(rare_trait):
    word = rare_trait

    return word


completed_output = []
count = 1
nft_no = 25
while count < nft_no + 1:
    image_files = []
    output_string = ""
    font_colour = (0, 0, 0)

    island_opt = choose_traits(island_route)

    dir_route = '.\\Input\\' + str(island_opt[0]) + "#" + str(island_opt[1])

    island_image = get_trait_image(dir_route, "\\" + "Islands" + "\\", island_opt)
    output_string += str(island_opt[0])

    rare_trait = island_opt
    for trait in traits:
        if trait != "Islands":
            trait_opt = choose_traits(os.listdir(dir_route + '\\' + trait + '\\'))
            if trait_opt[1] < rare_trait[1]:
                rare_trait = trait_opt

            trait_image = get_trait_image(dir_route, "\\" + trait + "\\", trait_opt)
            image_files.append(trait_image)
            output_string += str(trait_opt[0])

            if trait == "Background":
                if trait_opt[0] == "Outer Space":
                    font_colour = (255, 255, 255)

    name = gen_nft_name(rare_trait[0])

    image_files.insert(1, island_image)
    if output_string not in completed_output:
        completed_output.append(output_string)

        for trait in image_files:
            if trait != image_files[0]:
                image_files[0].paste(trait, (0, 0), mask=trait)

        draw = ImageDraw.Draw(image_files[0])
        width, height = image_files[0].size

        font = ImageFont.truetype("Poppins-Bold.ttf", 200)

        draw.text((150, 125), "#"+str(count), font_colour, font=font)

        w, h = draw.textsize(name, font=font)
        draw.text(((width-w)/2, 2250), name, font_colour, font=font)

        image_files[0].save(os.path.dirname(os.path.realpath(__file__)) + "\\output\\" + "World #" + str(count) + ".png", "PNG")

        count += 1
        print("NFT MADE")


