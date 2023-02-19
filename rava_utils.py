import logging
import os
import shutil
import numpy as np
import yaml
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Pt
import itertools

def find_tex_lyrics(project_path):
    # Find the songs in tex folder.
    tex_folder = os.path.join(project_path, "lyrics", "00_tex")
    tex = [
        os.path.join(tex_folder, x)
        for x in os.listdir(tex_folder)
        if x.endswith(".tex")
    ]

    return tex

def remove_consecutive_blanks(l):
    #Remove consecutive '' elements in a list.
    res = []

    for key, group in itertools.groupby(l, lambda x : x=='\n'):
        # check key=='' or not
        # if key!='' extend all values to res
        if not key:
            res.extend(list(group))
        # if key=='' append one '' to res
        else:
            res.append('\n')

    return res

def preprocess_tex(path_in: str, path_out: str, name: str):
    """
    Preprocess the tex file.
    """
    # Read the tex file.
    with open(path_in, "r") as f:
        tex_lines = np.array(f.readlines())

    # Take everything between the \begin{obeylines} and \end{obeylines}.
    begin_obeylines = np.argwhere(
        [r"\begin{obeylines}" in x for x in tex_lines]
    ).flatten()
    end_obeylines = np.argwhere([r"\end{obeylines}" in x for x in tex_lines]).flatten()

    # Assert that we have the same number of \begin{obeylines} and \end{obeylines}.
    assert len(begin_obeylines) == len(
        end_obeylines
    ), f"Number of \begin{{obeylines}} and \end{{obeylines}} do not match in {path_in}."
    if len(begin_obeylines) == 0:
        return 1

    clean_lines = []

    # Loop over the \begin{obeylines} and \end{obeylines} and take everything in between.
    for idx1, idx2 in zip(begin_obeylines, end_obeylines):
        lines = list(tex_lines[idx1 + 1 : idx2])
        lines = [x.replace("\\n", "\n") for x in lines]

        lines = [
            x
            for x in lines
            if not (
                x.startswith("\\") or x == "" or x.startswith("%") or r"\vspace" in x
            )
        ]

        clean_lines += lines

    #clean_lines = [x.lstrip() for x in clean_lines if x != '\n']
    #print(clean_lines)

    clean_lines = remove_consecutive_blanks(clean_lines)

    #Remove intial blank lines:
    #while clean_lines[0] == '\n':
    #    clean_lines.pop(0)

    if len(clean_lines) == 0:
        logging.info(f"No lines found in {path_in}. Skipping.")
        return

    # Write the preprocessed lines to the outpath.
    with open(path_out, "w") as f:
        f.writelines(clean_lines)

    return 0


def load_config(path):

    with open(path) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    background_color = RGBColor(*tuple(config["project"]["background_color"]))
    font_color = RGBColor(*tuple(config["project"]["font_color"]))
    font_name = config["project"]["font_name"]
    font_bold = config["project"]["font_bold"]
    font_size = Pt(config["project"]["font_size"])

    return background_color, font_color, font_name, font_bold, font_size


class PPTXSong:
    def __init__(self, background_color, font_color, font_name, font_bold, font_size):

        self.prs = Presentation()
        self.background_color = background_color
        self.font_color = font_color
        self.font_name = font_name
        self.font_bold = font_bold
        self.font_size = font_size

    def add_slide(self, string):
        """
        Adds a slide with input string. \n means new line, and <blank> is a blank slide.
        """

        title_slide_layout = self.prs.slide_layouts[5]
        slide = self.prs.slides.add_slide(title_slide_layout)
        title = slide.shapes.title

        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = self.background_color

        # Make the box take up the entire thing.
        title.left = 0
        title.width = self.prs.slide_width
        title.height = self.prs.slide_height

        # Add the text and change the font.
        text_frame = title.text_frame
        p = text_frame.paragraphs[0]

        n_line = 1
        for s in string.split("\\n"):
            # Remove leading and trailing spaces.
            s = s.strip()

            if n_line > 1:
                p.add_line_break()

            run = p.add_run()
            run.text = s

            # Add the formatting
            font = run.font
            font.name = self.font_name
            font.bold = self.font_bold
            font.size = self.font_size
            font.color.rgb = self.font_color

            # Signal we're jumping on to the next line.
            n_line += 1

        return

    def save(self, outpath):
        """
        Save the presentation.
        """
        self.prs.save(outpath)


def create_pptx(list_of_lyrics, out_path):

    # Load the config file.
    background_color, font_color, font_name, font_bold, font_size = load_config(
        "./revue_template/config.yaml"
    )
    pptx = PPTXSong(background_color, font_color, font_name, font_bold, font_size)
    
    for line in list_of_lyrics:
        pptx.add_slide(line)

    pptx.save(out_path)
    return


def pptx_to_png(infile, outfolder):
    assert infile.endswith(".pptx"), "Infile should be a .pptx"

    # Get the name of the song from the .pptx file.
    name = os.path.basename(infile).replace(".pptx", "")

    if os.path.isdir(outfolder):
        # If the subfolder exists, nuke it.
        shutil.rmtree(outfolder)
        os.mkdir(outfolder)
    else:
        os.mkdir(outfolder)

    # Convert the pptx to a pdf using soffice.
    os.system(f"soffice --headless --convert-to pdf:writer_pdf_Export {infile} > /dev/null 2>&1")

    #Move the file to where the pptx is located.
    os.rename(f'{name}.pdf', f'{infile.replace(".pptx", ".pdf")}')

    # Grab the name of the infile (but as pdf).
    infile_pdf = infile.replace(".pptx", ".pdf")

    # Convert the pdf to .pngs.
    os.system(
        f"convert -density 300 {infile_pdf} {outfolder}/{name}_%03d.png > /dev/null 2>&1"
    )

    # Delete the pdf in the /pptx/ folder afterwards.
    os.remove(infile_pdf)

    return
