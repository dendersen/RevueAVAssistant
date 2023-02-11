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

    #Get the name of the song from the .pptx file.
    name = os.path.basename(infile).replace(".pptx", "")

    if os.path.isdir(outfolder):
        # If the subfolder exists, nuke it.
        shutil.rmtree(outfolder)
        os.mkdir(outfolder)
    else:
        os.mkdir(outfolder)

    # Convert the pptx to a pdf.
    os.system(f"unoconv {infile} -f pdf")

    # Grab the name of the infile (but as pdf).
    infile_pdf = infile.replace(".pptx", ".pdf")

    # Convert the pdf to .pngs.
    os.system(f"convert -density 300 {infile_pdf} {outfolder}/{name}_%03d.png")

    # Delete the pdf in the /pptx/ folder afterwards.
    os.remove(infile_pdf)


def read_files(folder_path):
    return [open(infile, "r").read() for infile in folder_path]


def find_tex_lyrics(project_path):
    # Find the songs in tex folder.
    tex_folder = os.path.join(project_path, "lyrics", "00_txt")
    tex = [
        os.path.join(tex_folder, x)
        for x in os.listdir(tex_folder)
        if x.endswith(".tex")
    ]

    return tex

def find_txt_lyrics(project_path):
    # Find the songs in the txt folder.
    txt_folder = os.path.join(project_path, "lyrics", "00_txt")
    txt = [
        os.path.join(txt_folder, x)
        for x in os.listdir(txt_folder)
        if x.endswith(".txt")
    ]

    return txt

def preprocess_txt_songs(song_contents, song_paths=None):
    def preprocess(txt_string):
        x = txt_string.splitlines()
        x = [y.strip() for y in x]  # Remove leading and trailing spaces.
        x = [y.replace("  ", " ") for y in x]  # Remove double spaces.

        return x

    song_contents_clean = [preprocess(x) for x in song_contents]
    return song_contents_clean

def preprocess_tex_songs(song_contents, song_paths):
    def preprocess(tex_string, song_path):

        x = tex_string.splitlines()
        x = [y.strip() for y in x]  # Remove leading and trailing spaces.
        x = [y.replace("  ", " ") for y in x]  # Remove double spaces.

        # Split the lines.
        x = np.array(tex_string.splitlines())

        # Make sure that we have the same number of \begin{obeylines} and \end{obeylines}.
        assert sum([r"\begin{obeylines}" == y for y in x]) == sum(
            [r"\end{obeylines}" == y for y in x]
        ), (
            r"The number of \begin{obeylines} is not the same as the number of \end{obeylines} in the file "
            + f"{os.path.basename(song_path)}"
        )

        lines = []

        # In case we have multiple \begin{obeylines} ... \end{obeylines}, then we loop over them. This cuts out the comments in between.
        for idx1, idx2 in zip(
            np.argwhere(x == r"\begin{obeylines}").flatten(),
            np.argwhere(x == r"\end{obeylines}").flatten(),
        ):
            lines = x[idx1 + 1 : idx2]

            # \n in the document is loaded as \\n.
            lines = [
                y.replace("\\n", "\n")
                for y in lines
                if not (y.startswith("\\") or y == "" or y.startswith("%"))
            ]

        return lines

    song_contents_clean = [
        preprocess(song_content, song_path)
        for (song_content, song_path) in zip(song_contents, song_paths)
    ]
    return song_contents_clean


def check_for_conflicting_names(p1, p2):
    p1 = set([os.path.basename(p_).split(".")[0] for p_ in p1])
    p2 = set([os.path.basename(p_).split(".")[0] for p_ in p2])
    assert (
        len(p1.intersection(p2)) == 0
    ), "Conflicting names found in /tex/ and /txt/ folder."
    return


def write_preprocessed_songs(project, content, path_in):

    for c, p_in in zip(content, path_in):

        path_out = os.path.join(
            project,
            "lyrics",
            "01_preprocessed",
            f'{os.path.basename(p_in).split(".")[0]}.txt',
        )
        with open(path_out, "w") as f:
            f.write("\n".join(c))

    return

def find_preprocessed_lyrics(project_path):
    # Find the songs in the txt folder.
    txt_folder = os.path.join(project_path, "lyrics", "01_preprocessed")
    txt = [
        os.path.join(txt_folder, x)
        for x in os.listdir(txt_folder)
        if x.endswith(".txt")
    ]

    return txt

def find_pptx_lyrics(project_path):
    # Find the songs in the pptx folder.
    pptx_folder = os.path.join(project_path, "lyrics", "02_pptx")
    pptx = [
        os.path.join(pptx_folder, x)
        for x in os.listdir(pptx_folder)
        if x.endswith(".pptx")
    ]

    return pptx

def find_pdf_lyrics(project_path):
    # Find the songs in the pdf folder.
    pdf_folder = os.path.join(project_path, "lyrics", "03_pdf")
    pdf = [
        os.path.join(pdf_folder, x)
        for x in os.listdir(pdf_folder)
        if x.endswith(".pdf")
    ]

    return pdf

def read_preprocessed_lyrics(song_paths):
    song_contents = [[x.replace('\n','') for x in open(infile, "r").readlines()] for infile in song_paths]
    return song_contents

def create_pptx(list_of_lyrics, out_path):

    # Load the config file.
    background_color, font_color, font_name, font_bold, font_size = load_config(
        './revue_template/config.yaml'
    )

    pptx = PPTXSong(background_color, font_color, font_name, font_bold, font_size)

    for line in list_of_lyrics:
        pptx.add_slide(line)

    pptx.save(out_path)
    return 


