import os
import numpy as np
import yaml

# Dependencies for doing PowerPoint magic.
from pptx import Presentation
from pptx.util import Pt
from pptx.dml.color import RGBColor
import shutil


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
        for s in string.split("\n"):
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


def tex_to_pptx(infile, outfile, config_path):
    """
    Convert a .tex file to a .pptx file.
    """

    # Load the config file.
    background_color, font_color, font_name, font_bold, font_size = load_config(
        config_path
    )

    song = PPTXSong(background_color, font_color, font_name, font_bold, font_size)

    # Remove leading and trailing spaces and double spaces too.
    lyrics = np.array(
        [x.strip().replace("  ", " ") for x in open(infile, "r").read().splitlines()]
    )

    # Make sure that we have the same number of \begin{obeylines} and \end{obeylines}.
    assert sum([r"\begin{obeylines}" == x for x in lyrics]) == sum(
        [r"\end{obeylines}" == x for x in lyrics]
    ), r"Different number of \begin{obeylines} and \end{obeylines}."

    lines = []

    # In case we have multiple \begin{obeylines} ... \end{obeylines}, then we loop over them. This cuts out the comments in between.
    for idx1, idx2 in zip(
        np.argwhere(lyrics == r"\begin{obeylines}").flatten(),
        np.argwhere(lyrics == r"\end{obeylines}").flatten(),
    ):
        lines = lyrics[idx1 + 1 : idx2]

        # \n in the document is loaded as \\n.
        lines = [
            x.replace("\\n", "\n")
            for x in lines
            if not (x.startswith("\\") or x == "" or x.startswith("%"))
        ]

        for line in lines:
            if line == "<blank>":
                line = ""
            song.add_slide(line)

    song.save(outfile)
    return


def pptx_to_png(infile, outfolder):
    assert infile.endswith(".pptx"), "Infile should be a .pptx"
    # Get the name of the song.
    name = os.path.basename(infile).replace(".pptx", "")

    subfolder = os.path.join(outfolder, name)

    if os.path.isdir(subfolder):
        # If the subfolder exists, nuke it.
        shutil.rmtree(subfolder)
        os.mkdir(subfolder)
    else:
        os.mkdir(subfolder)

    # Convert the pptx to a pdf.
    os.system(f"unoconv {infile} -f pdf")

    # Grab the name of the infile (but as pdf).
    infile_pdf = infile.replace(".pptx", ".pdf")

    # Convert the pdf to .pngs.
    os.system(f"convert -density 300 {infile_pdf} ./{subfolder}/{name}_%03d.png")

    # Delete the pdf in the /pptx/ folder afterwards.
    os.remove(infile_pdf)
