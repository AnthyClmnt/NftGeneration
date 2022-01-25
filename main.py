# Imports
from PIL import Image, ImageFont, ImageDraw
import random
import os

path = os.path.join(os.path.dirname(__file__))  # Find project directory
island_route = os.listdir(path + '/Input/')  # Base Route

traits = ["Background", "Islands", "Rivers", "Top Decor", "Ground Decor"]  # Array of traits


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


def gen_nft_name(rare_trait):
    """
    @author: Anthony Clermont, Theodor Palmer

    :param rare_trait: The rarest trait in image: [name, rarity]
    :return: name of image
    """
    word = rare_trait

    return word


completed_output = []  # Includes all created images to compare to see if unique
count = 1  # Do not change
nft_no = 25  # Number of images to generate
# Will continuously generate images until count = number of images wanted + 1
while count < nft_no + 1:
    image_files = []  # Array of layers in image
    output_string = ""  # String of names of images to check if unique
    font_colour = (0, 0, 0)  # Default font colour is set to black

    island_opt = choose_traits(island_route)  # Chooses island

    # Sets the directory route for the rest of the images
    dir_route = path + '/Input/' + str(island_opt[0]) + "#" + str(island_opt[1])

    island_image = get_trait_image(dir_route, "/" + "Islands" + "/", island_opt)  # Gets the island image
    output_string += str(island_opt[0])  # Adds the name of island to output string

    rare_trait = island_opt  # Set the rare trait to first layer = island option
    # Loops through each trait
    for trait in traits:
        if trait != "Islands":  # Skips island choice
            trait_opt = choose_traits(os.listdir(dir_route + '/' + trait + '/'))  # Chooses trait
            if trait_opt[1] < rare_trait[1]:  # Checks if the trait is more rare than the current rare trait
                rare_trait = trait_opt

            trait_image = get_trait_image(dir_route, "/" + trait + "/", trait_opt)  # Gets the trait image
            image_files.append(trait_image)  # Adds the trait image to array
            output_string += str(trait_opt[0])  # Adds the name of the trait to the output string

            # If the trait is a background
            if trait == "Background":
                if trait_opt[0] == "Outer Space":  # If the background trait is outer space
                    font_colour = (255, 255, 255)  # Set the font colour to white

    name = gen_nft_name(rare_trait[0])  # Generate image name

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

        w, h = draw.textsize(name, font=font)  # Get the width, height of the text of the image
        x_pos = (width-w)/2   # Calculate the starting x position relative of the font size
        draw.text((x_pos, 2250), name, font_colour, font=font)  # Draw the name of the image on the image

        # Save the image
        image_files[0].save(path + "/output/" + "World #" + str(count) + ".png", "PNG")

        count += 1  # Increment the count by 1
        print("NFT MADE")  # Output to console


