# Imports
from PIL import Image, ImageFont, ImageDraw
import random
import os

path = os.path.join(os.path.dirname(__file__))  # Find project directory
island_route = os.listdir(path + '/Input/')  # Base Route

# Array of trait types
traits = ["Background", "Islands", "Ground Decor", "Rivers", "Top Decor", "Right Decor", "Left Decor", "Overlay"]

thesaurus = {"Green": ["Turf", "Grassland", "Meadow", "Field", "Lawn"],
             "Ice": ["Frost", "Glaze", "Freeze", "Glacier", "Polar", "Blizzard"],
             "Mars": ["Wasteland", "Galaxy", "Cosmos", "Space", "Planet"],
             "Sand": ["Desert", "Wasteland", "Shore", "Beach", "Sandy Hills"],

             "Blizzard Blue": ["Blue", "Sapphire", "Sky", "Aqua"],
             "Outer Space": ["Dark", "Smokey", "Tragic", "Blackened", "Woeful"],
             "Sidecar": ["Boring", "Bright", "Cream", "Beige"],
             "Tea Green": ["Mint", "Olive", "Lime", "Green"],
             "Lilac": ["Plum", "Violet", "Lavender"],
             "Mandy Pink": ["Rosy", "Girly", "Pink"],
             "Off White": ["Bright", "White"],

             "Coal": ["Ash", "Coal", "Miners", "Charcoal"],
             "Diamond": ["Jewel", "Diamond", "Miners", "Gem"],
             "Diamond Vein": ["Jewel", "Veins", "Miners", "Gem", "Diamond"],
             "Diamond Vein 2": ["Jewel", "Veins", "Miners", "Gem", "Diamond"],
             "Gold": ["Gold", "Miners", "Gem", "Jewel"],
             "Tent": ["Campers", "Camp Out"],
             "River": ["River", "Stream", "Canal", "Creek"],
             "Pine Trees": ["Timber", "Pine Forrest", "Pine", "Wood"],
             "satellite": ["Satellite", "Orbiting", "Exploring"],
             "Veins": ["Veiny", "Erupting"],

             "empty": ["Mini", "Tiny", "Empty", "Boring"]
             }


def combinations_num():
    dir_list = os.listdir(os.path.dirname(os.path.realpath(__file__)) + "/Input/")

    number = 0
    for island in dir_list:
        trait_route = os.listdir(os.path.dirname(os.path.realpath(__file__)) + "/Input/" + island)

        trait_number = 1
        for t in trait_route:
            trait_dir = os.listdir(os.path.dirname(os.path.realpath(__file__)) + "/Input/" + island + "/" + t)
            trait_number = trait_number * len(trait_dir)

        number += trait_number

    return number


def get_traits(traits):
    """
    @author: Anthony Clermont

    :param traits: Array of traits from directory
    :return: Array of trait arrays, split into the name and rarity
    """
    trait_array = []  # Empty Trait array
    for trait in traits:  # Loops through all the traits given
        split_file_name = trait.split("#")  # Split the filename by #
        split_rarity = split_file_name[1]  # Set the second position to the rarity
        rarity = split_rarity.split(".")[0]  # Removes the .png tag from the rarity

        trait = [split_file_name[0], int(rarity)]  # Array of trait, [0] = name, [1] = rarity
        trait_array.append(trait)  # Adds array into array of traits

    return trait_array


def choose_traits(trait_route):
    """
    @author: Anthony Clermont

    :param trait_route: Directory path to use
    :return: the trait name, rarity chosen at random
    """
    traits = get_traits(trait_route)  # Calls get_traits function
    # Randomly chooses trait from list, factoring in weights
    choice_trait = random.choices(population=traits, weights=[item[1] for item in traits], k=1)

    return choice_trait[0]


def get_trait_image(route, trait_type, trait):
    """
    @author: Anthony Clermont

    :param route: The directory route
    :param trait_type: the trait type the image is, e.g. 'Background'
    :param trait: The trait array chosen: [name, rarity]
    :return: The image of the chosen trait
    """
    return Image.open(route + trait_type + str(trait[0]) + "#" + str(trait[1]) + ".png")


def gen_nft_name(rare_trait_name, island_type_name):
    """
    @author: Anthony Clermont, Theodor Palmer

    :param island_type_name: The island type name chosen:
    :param rare_trait_name: The rarest trait in image: [name, rarity]

    :return: name of image
    """

    island_desc_opt = random.choice(thesaurus[island_type_name])
    rare_desc_opt = random.choice(thesaurus[rare_trait_name])

    return rare_desc_opt + " " + island_desc_opt


images_possible = combinations_num()

completed_output = []  # Includes all created images to compare to see if unique
count = 1  # Do not change
nft_no = 50  # Number of images to generate
# Will continuously generate images until count = number of images wanted + 1
if images_possible > nft_no:
    while count < nft_no + 1:
        image_files = []  # Array of layers in image
        output_string = ""  # String of names of images to check if unique
        font_colour = (0, 0, 0)  # Default font colour is set to black

        island_opt = choose_traits(island_route)  # Chooses island

        # Sets the directory route for the rest of the images
        dir_route = path + '/Input/' + str(island_opt[0]) + "#" + str(island_opt[1])

        island_image = get_trait_image(dir_route, "/" + "Islands" + "/", island_opt)  # Gets the island image
        output_string += str(island_opt[0])  # Adds the name of island to output string

        rare_trait = ["", 100]  # Set the rare trait to first layer = island option
        # Loops through each trait
        for trait in traits:
            if trait != "Islands":  # Skips island choice
                trait_opt = choose_traits(os.listdir(dir_route + '/' + trait + '/'))  # Chooses trait
                if trait_opt[1] < rare_trait[1]:  # Checks if the trait is more rare than the current rare trait
                    rare_trait = trait_opt

                trait_image = get_trait_image(dir_route, "/" + trait + "/", trait_opt)  # Gets the trait image
                image_files.append(trait_image)  # Adds the trait image to array
                output_string += str(trait_opt)  # Adds the name of the trait to the output string

                # If the trait is a background
                if trait == "Background":
                    if trait_opt[0] == "Outer Space":  # If the background trait is outer space
                        font_colour = (255, 255, 255)  # Set the font colour to white

        name = gen_nft_name(rare_trait[0], island_opt[0])  # Generate image name

        image_files.insert(1, island_image)  # Insert island image into correct position

        if output_string not in completed_output:  # Check if image's output string doesnt exist
            completed_output.append(output_string)  # Add output string to completed outputs

            for trait in image_files:  # For all the traits
                if trait != image_files[0]:  # No need to paste first layer over the first layer
                    image_files[0].paste(trait, (0, 0), mask=trait)  # Paste the layer over the background

            draw = ImageDraw.Draw(image_files[0])  # With the completed image set to draw
            width, height = image_files[0].size  # Get the width, height of the image

            font = ImageFont.truetype("Poppins-Bold.ttf", 200)  # Set the font size and colour

            draw.text((150, 125), "#"+str(count), font_colour, font=font)  # Draw the number of the image on the image

            #w, h = draw.textsize(name, font=font)  # Get the width, height of the text of the image
            #x_pos = (width-w)/2   # Calculate the starting x position relative of the font size
            #draw.text((x_pos, 2250), name, font_colour, font=font)  # Draw the name of the image on the image
            #logo = Image.open("Logo.png")
            #image_files[0].paste(logo, (0, 0), mask=logo)

            # Save the image
            image_files[0].save(path + "/output/" + "#" + str(count) + " " + name + ".png", "PNG")

            count += 1  # Increment the count by 1
            print("NFT MADE")  # Output to console
else:
    print("Not enough layers to make: " + str(nft_no) + " images")


