import os
import turtle
from turtle import Turtle, Screen
import pandas as pd
from Bio import SeqIO
from PIL import Image


def sequences_drawer(fasta_file, tsv_file, analysis_used):
    # COUNT HOW MUCH PROTEIN SEQUENCES THERE ARE IN FASTA FORMAT
    protein_list = []
    with open(fasta_file, "r") as file:
        for everyrecord in SeqIO.parse(file, "fasta"):
            if everyrecord.id in protein_list:
                pass
            else:
                protein_list.append(everyrecord.id)
    num_prot = 0
    z = 1

    for everyprotein in protein_list:
        dataframe1 = pd.read_table(tsv_file)
        df_first_filter = dataframe1.loc[dataframe1["3"] == analysis_used]
        df_second_filter = df_first_filter.loc[df_first_filter["0"] == everyprotein]

        number_of_result_filtered = int(len(df_second_filter))
        unsorted_dict_result_filtered = df_second_filter.to_dict("records")
        dict_result_filtered = sorted(unsorted_dict_result_filtered, key=lambda i: (i["0"], i["6"]), reverse=True)

        if number_of_result_filtered == 0:
            pass
        else:

            screen = Screen()
            turtle.TurtleScreen._RUNNING = True
            # The arg 0 for tracer provides an instant draw
            screen.tracer(0)
            turtle.screensize(canvwidth=1000,
                              canvheight=500,
                              bg="white")

            single_protein_drawer = Turtle()
            # Hide the turtle-cursor
            single_protein_drawer.hideturtle()

            style_text_domain = ("Arial", 8, "")
            style_text_nameprotein = ("Arial", 20, "bold")
            style_text_scale = ("Arial", 20, "italic")
            style_text_segment_scale = ("Arial", 10, "")
            seq_length = int(dict_result_filtered[0]["2"])

            # SCALE THE LENGTH OF THE PROTEIN
            scale = 1
            if seq_length * 2 < 800:
                scale = scale * 2
            elif seq_length > 1500:
                scale = 0.25
            elif seq_length > 700:
                scale = 0.5
            x_point_to_start = -350
            y_point_to_start = -70

            # DRAW THE NAME OF THE PROTEIN
            prot_name = dict_result_filtered[0]["0"]
            single_protein_drawer.penup()
            single_protein_drawer.goto(x_point_to_start, 130)
            single_protein_drawer.pendown()

            single_protein_drawer.write(prot_name, font=style_text_nameprotein)

            # DRAW THE REPORT OF THE SCALE UNDER THE NAME FO THE PROTEIN
            if scale == 2:
                single_protein_drawer.penup()
                single_protein_drawer.goto(x_point_to_start, 100)
                single_protein_drawer.pendown()
                single_protein_drawer.write(f"Protein dimension scaled by {scale}", font=style_text_scale)
            elif scale == 0.25:
                single_protein_drawer.penup()
                single_protein_drawer.goto(x_point_to_start, 100)
                single_protein_drawer.pendown()
                single_protein_drawer.write(f"Protein dimension scaled by {scale}", font=style_text_scale)
            elif scale == 0.5:
                single_protein_drawer.penup()
                single_protein_drawer.goto(x_point_to_start, 100)
                single_protein_drawer.pendown()
                single_protein_drawer.write(f"Protein dimension scaled by {scale}", font=style_text_scale)

            # DRAW THE ENTIRE LENGTH OF THE PROTEIN
            scalated_seq_lenght = int(seq_length) * scale
            single_protein_drawer.pensize(5)
            single_protein_drawer.pencolor("black")
            single_protein_drawer.penup()
            single_protein_drawer.goto(x_point_to_start, y_point_to_start)
            single_protein_drawer.pendown()
            single_protein_drawer.forward(scalated_seq_lenght)

            # DRAW THE LENGTH REFERNCE UNDER THE PROTEIN
            single_protein_drawer.pensize(2)
            single_protein_drawer.pencolor("black")
            single_protein_drawer.penup()
            single_protein_drawer.goto(x_point_to_start, y_point_to_start - 40)
            single_protein_drawer.pendown()
            single_protein_drawer.forward(scalated_seq_lenght)
            segments = int(scalated_seq_lenght / 100)
            segments_exceed = int((scalated_seq_lenght % 100) + 1)
            segments_starting_point = x_point_to_start
            milestone = 0
            for n in range(0, segments + 1):
                if n < segments:
                    single_protein_drawer.penup()
                    single_protein_drawer.goto(segments_starting_point, y_point_to_start - 30)
                    single_protein_drawer.pendown()
                    single_protein_drawer.goto(segments_starting_point, y_point_to_start - 50)
                    single_protein_drawer.penup()
                    single_protein_drawer.goto(segments_starting_point - 5, y_point_to_start - 65)
                    single_protein_drawer.pendown()
                    single_protein_drawer.write(milestone, font=style_text_segment_scale)
                    single_protein_drawer.penup()
                else:
                    if segments_exceed < 50:
                        segments_add = segments_starting_point + segments_exceed
                        single_protein_drawer.penup()
                        single_protein_drawer.goto(segments_add, y_point_to_start - 30)
                        single_protein_drawer.pendown()
                        single_protein_drawer.goto(segments_add, y_point_to_start - 50)
                        single_protein_drawer.penup()
                        single_protein_drawer.goto(segments_add - 5, y_point_to_start - 65)
                        single_protein_drawer.pendown()
                        single_protein_drawer.write(seq_length, font=style_text_segment_scale)
                        single_protein_drawer.penup()
                    else:
                        single_protein_drawer.penup()
                        single_protein_drawer.goto(segments_starting_point, y_point_to_start - 30)
                        single_protein_drawer.pendown()
                        single_protein_drawer.goto(segments_starting_point, y_point_to_start - 50)
                        single_protein_drawer.penup()
                        single_protein_drawer.goto(segments_starting_point - 5, y_point_to_start - 65)
                        single_protein_drawer.pendown()
                        single_protein_drawer.write(milestone, font=style_text_segment_scale)
                        single_protein_drawer.penup()
                        segments_starting_point += segments_exceed
                        single_protein_drawer.penup()
                        single_protein_drawer.goto(segments_starting_point, y_point_to_start - 30)
                        single_protein_drawer.pendown()
                        single_protein_drawer.goto(segments_starting_point, y_point_to_start - 50)
                        single_protein_drawer.penup()
                        single_protein_drawer.goto(segments_starting_point - 5, y_point_to_start - 65)
                        single_protein_drawer.pendown()
                        single_protein_drawer.write(seq_length, font=style_text_segment_scale)
                        single_protein_drawer.penup()
                milestone += int(100 / scale)
                segments_starting_point += 100

            altitudine = 20
            verso = "+"
            for er in range(0, number_of_result_filtered):
                # ----> EXTRACT MULTIPLE VARIABLE
                start_location = dict_result_filtered[er]["6"]
                stop_location = dict_result_filtered[er]["7"]
                interpro_annotation = dict_result_filtered[er]["12"]
                interpro_annotation_mod = interpro_annotation.upper()

                # SCALED DIMENSION OF THE START, STOP AND DOMAIN
                scalated_start_location = int(start_location * scale)
                scalated_stop_location = int(stop_location * scale)
                scalated_domain_length = scalated_stop_location - scalated_start_location

                # DRAW THE DOMAIN
                single_protein_drawer.pencolor("red")
                single_protein_drawer.pensize(10)
                single_protein_drawer.penup()
                single_protein_drawer.goto(x_point_to_start, y_point_to_start)
                single_protein_drawer.forward(scalated_start_location)
                single_protein_drawer.pendown()
                single_protein_drawer.forward(scalated_domain_length)
                single_protein_drawer.penup()

                # DRAW THE DOMAIN'S NAME
                single_protein_drawer.pensize(1)
                single_protein_drawer.penup()
                single_protein_drawer.backward(scalated_domain_length)
                single_protein_drawer.pencolor("grey40")
                single_protein_drawer.left(90)
                single_protein_drawer.forward(5)
                single_protein_drawer.pendown()
                single_protein_drawer.forward(altitudine)
                single_protein_drawer.penup()
                single_protein_drawer.backward(7)
                single_protein_drawer.right(90)
                single_protein_drawer.forward(5)
                single_protein_drawer.pendown()
                single_protein_drawer.pencolor("black")
                single_protein_drawer.write(interpro_annotation_mod, font=style_text_domain)
                single_protein_drawer.penup()

                if altitudine > 130:
                    verso = "-"
                    altitudine -= 15
                elif verso == "-" and altitudine > 40:
                    verso = "-"
                    altitudine -= 30
                elif verso == "-" and altitudine < 40:
                    verso = "+"
                    altitudine += 15
                elif verso == "+":
                    altitudine += 30

            # TIME TO SAVE THE DRAW!
            # GOD SAVE THE SCREEN
            ts = single_protein_drawer.getscreen()

            # SET THE AREA'S DIMENSION
            ts.getcanvas().postscript(file="temp_%s.ps" % z,
                                      x=-500,
                                      width=1000,
                                      y=-250,
                                      height=500)

            # UNCOMMENT = MANUAL CLICK FOR EVERY SEQUENCE DREW
            # screen.exitonclick()

            # OPEN THE IMAGE BY PILLOW
            psimage = Image.open("temp_%s.ps" % z)
            psimage.load(scale=8)

            # FOR PNG FORMAT JUST CHANGE EXTENSION IN .png
            psimage.save('domains_view_%s.jpg' % z, dpi=(100, 100), quality=95)
            psimage.close()

            os.remove("temp_%s.ps" % z)
            ts.reset()

            # INCREASE THE COUNTER SAVE THE NEXT IMG WITHOUT OVERWRITE THIS ONE
            z += 1

            # INCREASE THE COUNTER TO PASS TO THE NEXT PROTEIN
            num_prot += 1
