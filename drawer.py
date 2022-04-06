import os
import turtle
from turtle import Turtle, Screen
from PIL import Image


def sequences_drawer(protein_list, table_list, result_dictionary):
    # Color list
    main_domains_color = ["purple", "red", "violet", "blue", "green", "yellow", "orange", "brown", "cyan"]
    secondary_domains_color = ["gray75"]

    # Style text
    style_text_domain = ("Arial", 8, "")
    style_text_nameprotein = ("Arial", 20, "bold")
    style_text_scale = ("Arial", 20, "italic")
    style_text_segment_scale = ("Arial", 10, "")

    # Counter to rename output file when another file with the same name exist
    list_of_file = os.listdir("./")
    if "domains_view.jpg" in list_of_file:
        z = 1
        while os.path.exists("domains_view%s.jpg" % z):
            z += 1
    else:
        z = 1

    item_in_list = len(table_list)

    if item_in_list < 9:
        number_of_domains = item_in_list
    else:
        number_of_domains = 9

    dict_domain_color = {}

    for n in range(0, number_of_domains):
        dict_domain_color[table_list[n][1]] = main_domains_color[n]


    # ***********************************************************************
    # STARTING THE DRAWING PROCESS - FOR CYCLE TAKE ONE PROTEIN AT TIME
    # ***********************************************************************

    # For every protein in protein list extract the lines containing analysis_used
    for everyprotein in protein_list:
        domain_counter = 0
        protein_length = len(result_dictionary[everyprotein]["Sequence"])

        # Counting the domain
        for everydomain in result_dictionary[everyprotein]["Extracted_domains"]:
            domain_counter += 1

        # If the protein hasn't ANY domains, skip
        if domain_counter == 0:
            pass
        else:
            screen = Screen()
            turtle.TurtleScreen._RUNNING = True
            # The arg 0 for tracer provides an instant draw
            screen.tracer(0)
            # Setting the screensize
            turtle.screensize(canvwidth=1000,
                              canvheight=500,
                              bg="white")

            # drawer ex name was "spd" (Single Protein Drawer)
            drawer = Turtle()

            # Hide the turtle-cursor
            drawer.hideturtle()

            # Scale the length of the protein
            seq_length = protein_length
            scale = 1
            if seq_length * 2 < 800:
                scale = scale * 2
            elif seq_length > 1500:
                scale = 0.25
            elif seq_length > 700:
                scale = 0.5
            scalated_seq_lenght = int(seq_length) * scale

            # Set the origin (x, y) where the protein's draw begin
            x_point_to_start = -350
            y_point_to_start = -70

            # Draw the name of the protein
            prot_name = everyprotein
            drawer.penup()
            drawer.goto(x_point_to_start, 130)
            drawer.pendown()
            drawer.write(prot_name, font=style_text_nameprotein)

            # Check if is needed to report the scale under the name of the protein
            if scale != 1:
                drawer.penup()
                drawer.goto(x_point_to_start, 100)
                drawer.pendown()
                drawer.write(f"Protein dimension scaled by {scale}", font=style_text_scale)

            # Draw the entire length of the protein
            drawer.pensize(5)
            drawer.pencolor("black")
            drawer.penup()
            drawer.goto(x_point_to_start, y_point_to_start)
            drawer.pendown()
            drawer.forward(scalated_seq_lenght)

            # Draw the length reference **LINE** under the protein
            drawer.pensize(2)
            drawer.pencolor("black")
            drawer.penup()
            drawer.goto(x_point_to_start, y_point_to_start - 40)
            drawer.pendown()
            drawer.forward(scalated_seq_lenght)

            # Draw the length reference **MILESTONES** under the protein
            segments = int(scalated_seq_lenght / 100)
            segments_exceed = int((scalated_seq_lenght % 100) + 1)
            segments_starting_point = x_point_to_start
            milestone = 0

            # For every segments there are three possibilities:
            # 1) If the segment is within the range, print it entirely
            # 2) If the last segment is < 50, add it to the last one and print them together
            # 3) If the last segment is > 50, print the (last one -1) and print the last segments
            for n in range(0, segments + 1):
                if n < segments:
                    drawer.penup()
                    drawer.goto(segments_starting_point, y_point_to_start - 30)
                    drawer.pendown()
                    drawer.goto(segments_starting_point, y_point_to_start - 50)
                    drawer.penup()
                    drawer.goto(segments_starting_point - 5, y_point_to_start - 65)
                    drawer.pendown()
                    drawer.write(milestone, font=style_text_segment_scale)
                    drawer.penup()
                else:
                    if segments_exceed < 50:
                        segments_add = segments_starting_point + segments_exceed
                        drawer.penup()
                        drawer.goto(segments_add, y_point_to_start - 30)
                        drawer.pendown()
                        drawer.goto(segments_add, y_point_to_start - 50)
                        drawer.penup()
                        drawer.goto(segments_add - 5, y_point_to_start - 65)
                        drawer.pendown()
                        drawer.write(seq_length, font=style_text_segment_scale)
                        drawer.penup()
                    else:
                        drawer.penup()
                        drawer.goto(segments_starting_point, y_point_to_start - 30)
                        drawer.pendown()
                        drawer.goto(segments_starting_point, y_point_to_start - 50)
                        drawer.penup()
                        drawer.goto(segments_starting_point - 5, y_point_to_start - 65)
                        drawer.pendown()
                        drawer.write(milestone, font=style_text_segment_scale)
                        drawer.penup()
                        segments_starting_point += segments_exceed
                        drawer.penup()
                        drawer.goto(segments_starting_point, y_point_to_start - 30)
                        drawer.pendown()
                        drawer.goto(segments_starting_point, y_point_to_start - 50)
                        drawer.penup()
                        drawer.goto(segments_starting_point - 5, y_point_to_start - 65)
                        drawer.pendown()
                        drawer.write(seq_length, font=style_text_segment_scale)
                        drawer.penup()

                milestone += int(100 / scale)
                segments_starting_point += 100

            # Setting the altitude for the name of the domains and the direction
            altitudine = 20
            direction = "+"

            for everydomain in result_dictionary[everyprotein]["Extracted_domains"]:

                start_location = everydomain["START"]
                stop_location = everydomain["STOP"]
                interpro_annotation = everydomain["DOMAIN_NAME"]
                interpro_annotation_mod = interpro_annotation.upper()

                # Stop/start/domain dimension scaled
                scalated_start_location = int(start_location * scale)
                scalated_stop_location = int(stop_location * scale)
                scalated_domain_length = scalated_stop_location - scalated_start_location

                # # Choose the color for the domain
                if interpro_annotation in dict_domain_color.keys():
                    color_choosen = dict_domain_color[interpro_annotation]
                else:
                    color_choosen = secondary_domains_color[0]

                # Reset the position
                drawer.home()

                # Draw the domain
                drawer.pencolor(color_choosen)
                drawer.pensize(10)
                drawer.penup()
                drawer.goto(x_point_to_start, y_point_to_start)
                drawer.forward(scalated_start_location)
                drawer.pendown()
                drawer.forward(scalated_domain_length)
                drawer.penup()

                # Draw the domain's name background (to delete the line colliding with the name)
                drawer.pensize(2)
                drawer.penup()
                drawer.backward(scalated_domain_length)
                drawer.pencolor(color_choosen)
                drawer.left(90)
                drawer.forward(5)
                drawer.pendown()
                drawer.forward(altitudine)
                position_to_save_02 = drawer.pos()
                drawer.penup()
                drawer.backward(7)
                drawer.right(90)
                drawer.forward(5)
                position_to_save_01 = drawer.pos()
                drawer.forward(3)
                drawer.left(90)
                drawer.forward(5)
                drawer.right(90)
                drawer.pendown()
                drawer.pensize(10)
                drawer.pencolor("white")
                length_name = int(len(interpro_annotation) * 4.7)
                drawer.forward(length_name)
                drawer.penup()

                # Draw domain's name
                drawer.goto(position_to_save_01)
                drawer.pendown()
                drawer.pencolor("black")
                drawer.write(interpro_annotation_mod, font=style_text_domain)
                drawer.penup()

                # Draw indicator
                drawer.pencolor(color_choosen)
                drawer.goto(position_to_save_02)
                drawer.pensize(2)
                drawer.pendown()
                drawer.right(45)
                drawer.forward(4)
                drawer.right(90)
                drawer.forward(3.5)
                drawer.penup()

                # If cycle to setting up the order of each domain
                if altitudine > 130:
                    direction = "-"
                    altitudine -= 15
                elif direction == "-" and altitudine > 40:
                    direction = "-"
                    altitudine -= 30
                elif direction == "-" and altitudine < 40:
                    direction = "+"
                    altitudine += 15
                elif direction == "+":
                    altitudine += 30

            # Time to save the draw
            # GOD SAVE THE SCREEN!
            ts = drawer.getscreen()

            # Set the dimension of the area
            ts.getcanvas().postscript(file="temp_%s.ps" % z,
                                      x=-500,
                                      width=1000,
                                      y=-250,
                                      height=500)

            # UNCOMMENT = MANUAL CLICK FOR EVERY SEQUENCE DREW
            # screen.exitonclick()

            # Open the image with pillow
            psimage = Image.open("temp_%s.ps" % z)
            psimage.load(scale=7)

            # Saving the image as .png
            # For PNG format just change .jpg in .png
            psimage.save('domains_view%s.jpg' % z, dpi=(100, 100), quality=95)
            psimage.close()

            # Removing the temporary image .ps created before
            os.remove("temp_%s.ps" % z)
            ts.reset()

        # Increase the counter for the images' name
        z += 1
