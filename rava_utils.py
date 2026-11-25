import itertools
import logging
import os
import shutil

import numpy as np
import yaml
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Emu, Pt, Inches
from re import sub

def find_raw_lyrics(project_path:str) -> list[str]:
    # Find the songs in tex folder.
    raw_folder: str = os.path.join(project_path, "lyrics", "00_raw")
    files: list[str] = [
        os.path.join(raw_folder, x)
        for x in os.listdir(raw_folder)
        if (x.endswith(".tex") or x.endswith('.txt'))
    ]

    return files

def remove_consecutive_blanks(l:list[str]) -> list[str]:
    #Remove consecutive '' elements in a list.
    res:list[str] = []

    for line in l:
        if line != '\n':
            res.append(line)
        elif res and res[-1] != '\n':
            res.append('\n')
        else:
            continue

    return res

lyricStarters = ["obeylines","center","omkv","vers"]

def preprocess_tex_format(path_in: str, path_out: str) -> bool:
    return preprocess_tex(path_in, path_out, keepTags=True)

def preprocess_tex(path_in: str, path_out: str, keepTags:bool = False) -> bool:
    """
    Preprocess the tex file.
    returns True when the file was valid
    returns False when the file was invalid
    
    lines are written to path_out, but if the file is invalid, the output file will not be touched
    """
    # Read the tex file.
    with open(path_in, "r") as f:
        tex_lines: np.ndarray = np.array(f.readlines())

    # Take everything between the \begin{obeylines} and \end{obeylines}.
    begin_obeylines:list[int] = []
    end_obeylines:list[int] = []
    for idx, line in enumerate(tex_lines):
        for controller in lyricStarters:
            control_in = r"\begin{" + controller + "}"
            control_out = r"\end{" + controller + "}"
            if control_in in line:
                begin_obeylines.append(idx)
            elif control_out in line:
                end_obeylines.append(idx)
    np_begin_obeylines = np.array(begin_obeylines)
    np_end_obeylines = np.array(end_obeylines)

    # Assert that we have the same number of \begin{obeylines} and \end{obeylines}.
    assert len(np_begin_obeylines) == len(
        np_end_obeylines
    ), f"Number of \\begin{{obeylines}} and \\end{{obeylines}} do not match in {path_in}."
    if len(np_begin_obeylines) == 0:
        return False

    clean_lines:list[str] = []

    # Loop over the \begin{obeylines} and \end{obeylines} and take everything in between.
    for idx1, idx2 in zip(np_begin_obeylines, np_end_obeylines):
        lines:list[str] = list(tex_lines[idx1 + 1 : idx2])
        lines = [x.replace("\\n", "\n").replace("\\newline", "\n").replace("\\\\", "\n").replace("\n\n","\n") for x in lines]
        
        #new \vspace filtering
        if not keepTags:
            for i in range(len(lines)):
                # lines[i] = sub(r"\vspace\{[0-9](.?[0-9]?){2}\}", "", lines[i])
                # lines[i] = sub(r"\vspace{.*?}", "", lines[i])
                lines[i] = sub(r"(-\ )?\\[a-zA-Z]*\{[a-zA-Z0-9.,\ ]*\}(:\ )?", "", lines[i])
                if lines[i].count("{") != lines[i].count("}"):
                    lines[i] = lines[i].replace("{","").replace("}","")

        lines = [
            x
            for x in lines
            if not (
                (x.startswith("\\") and not keepTags) or x == "" or x.startswith("%")
            )
        ]

        clean_lines += lines

    clean_lines = remove_consecutive_blanks(clean_lines)

    if len(clean_lines) == 0:
        logging.info(f"No lines found in {path_in}. Skipping.")
        return False

    if os.path.isdir(path_out):
        path_out = os.path.join(path_out, os.path.basename(path_in))
        path_out = os.path.splitext(path_out)[0] + ".txt"
    # Write the preprocessed lines to the outpath.
    with open(path_out, "w") as f:
        f.writelines(clean_lines)

    return True

def load_config(path:str) -> tuple[RGBColor, RGBColor, str, bool, Pt]:

    with open(path) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    background_color = RGBColor(*tuple(config["project"]["background_color"]))
    font_color = RGBColor(*tuple(config["project"]["font_color"]))
    font_name = str(config["project"]["font_name"])
    font_bold = bool(config["project"]["font_bold"])
    font_size = Pt(config["project"]["font_size"])

    return background_color, font_color, font_name, font_bold, font_size

class PPTXSong:
    def __init__(self, background_color: RGBColor, font_color: RGBColor, font_name: str, font_bold: bool, font_size: Pt):

        self.prs = Presentation()
        self.background_color = background_color
        self.font_color = font_color
        self.font_name = font_name
        self.font_bold = font_bold
        self.font_size = font_size

    def add_slide(self, text:str):
        """
        Adds a slide with input string. \n means new line, and <blank> is a blank slide.
        """

        title_slide_layout = self.prs.slide_layouts[5]
        slide = self.prs.slides.add_slide(title_slide_layout)
        title = slide.shapes.title
        if title is None:
            logging.warning("No title placeholder found in the slide layout. This should not happen, check the template.")
            return

        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = self.background_color

        # Make the box take up the entire thing.
        title.left = Inches(0)
        slide_width:Emu | None = self.prs.slide_width # type: ignore
        slide_height:Emu | None = self.prs.slide_height # type: ignore
        if slide_width is None:
            logging.warning("No slide width found in the presentation. This should not happen, check the template.")
            return
        if slide_height is None:
            logging.warning("No slide height found in the presentation. This should not happen, check the template.")
            return
        title.width = slide_width
        title.height = slide_height

        # Add the text and change the font.
        text_frame = title.text_frame
        p = text_frame.paragraphs[0]

        n_line = 1
        for s in text.split("\\n"):
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

    def save(self, outpath:str):
        """
        Save the presentation.
        """
        self.prs.save(outpath)

def create_pptx(list_of_lyrics:list[str] | str, out_path:str, name:str = ""):

    # Load the config file.
    
    background_color: RGBColor
    font_color: RGBColor
    font_name: str
    font_bold: bool
    font_size: Pt

    if isinstance(list_of_lyrics, str):
        if os.path.isfile(list_of_lyrics):
            name = os.path.basename(list_of_lyrics)
            name = os.path.splitext(name)[0]
            with open(list_of_lyrics, 'r', encoding='utf-8') as f:
                list_of_lyrics = f.read().splitlines()
        elif os.path.isdir(list_of_lyrics):
            for filename in os.listdir(list_of_lyrics):
                create_pptx(os.path.join(list_of_lyrics, filename), os.path.join(out_path, filename.replace(".txt", ".pptx")))

    background_color, font_color, font_name, font_bold, font_size = load_config(
        os.path.join(".", "revue_template", "config.yaml")
    )
    pptx = PPTXSong(background_color, font_color, font_name, font_bold, font_size)
    
    for line in list_of_lyrics:
        pptx.add_slide(line)

    if os.path.isdir(out_path):
        out_path = os.path.join(out_path, name + ".pptx")
    pptx.save(out_path)
    return


def pptx_to_png(pptxPath:str, outfolder:str):
    assert pptxPath.endswith(".pptx"), "pptxPath should be a .pptx file"

    # Get the name of the song from the .pptx file.
    name = os.path.basename(pptxPath).replace(".pptx", "")

    if os.path.isdir(outfolder):
        # If the subfolder exists, nuke it.
        shutil.rmtree(outfolder)
        os.mkdir(outfolder)
    else:
        os.mkdir(outfolder)

    # Convert the pptx to a pdf using soffice.
    os.system(f"soffice --headless --convert-to pdf:writer_pdf_Export '{pptxPath}'")

    # Grab the name of the infile (but as pdf).
    infile_pdf = pptxPath.replace(".pptx", ".pdf")
    
    #Move the file to where the pptx is located.
    os.rename(f'{name}.pdf', f'{infile_pdf}')

    # Convert the pdf to .pngs.
    os.system(
        f"convert -density 300 {infile_pdf} {outfolder}/{name}_%03d.png"
    )

    # Delete the pdf in the /pptx/ folder afterwards.
    os.remove(infile_pdf)

    return


TEMPLATES = os.path.join(os.path.dirname(os.path.abspath(__file__)),"templates")
HTML_TEMPLATE    = open(os.path.join(TEMPLATES, "HTML_TEMPLATE.html")).read()
RUNDOWN_TEMPLATE = open(os.path.join(TEMPLATES, "RUNDOWN_TEMPLATE.xml")).read()
HTML_GROUP_TEMPLATE = open(os.path.join(TEMPLATES, "HTML_GROUP_TEMPLATE.xml")).read()

def txt_to_html(rawPath:str, outPath:str):
    """
        convert all files in a directory (or a single file)
        to a corresponding HTML file(s) using the HTML template.
        will seek recursively through directories. for .txt files, it will generate corresponding HTML files.
    """
    if os.path.isdir(rawPath):
        for filename in os.listdir(rawPath):
            txt_to_html(os.path.join(rawPath, filename), os.path.join(outPath, filename))
    elif rawPath.endswith(".txt"):
        os.makedirs(outPath, exist_ok=True)
        with open(rawPath, "r") as f:
            for i, line in enumerate(f.readlines()):
                while line.endswith("\n"):
                    line = line[:-1]
                html_content = HTML_TEMPLATE.replace("$YOUR_TEXT$", line.replace("\n", "<br>"))
                out_dir = os.path.join(outPath, os.path.basename(rawPath).replace(".txt", ""))
                os.makedirs(out_dir, exist_ok=True)
                out_file = os.path.join(out_dir, f"{i}.html")
                with open(out_file, "w") as f_out:
                    f_out.write(html_content)
        print(f"Generated HTML for {rawPath}")
    else:
        print(f"Skipping non-text file: {rawPath}")

def generateRundowns(htmlPath:str, outPath:str):
    """
        generate rundown XML files from HTML files using the rundown template.
        will seek recursively through directories. for .html files.
        it will generate a corresponding XML file for each directory with html files.
    """
    if not os.path.isdir(htmlPath):
        print(f"HTML path not directory: {htmlPath}")
        return
    
    contents = os.listdir(htmlPath)
    htmlFiles:list[str] = []
    for filename in contents:
        if os.path.isdir(os.path.join(htmlPath, filename)):
            generateRundowns(os.path.join(htmlPath, filename), os.path.join(outPath, filename))
        elif filename.endswith(".html"):
            htmlFiles.append(os.path.join(htmlPath, filename))
    
    if not htmlFiles:
        print(f"No HTML files found in {htmlPath}")
        return

    print(f"found {len(htmlFiles)} HTML files in {htmlPath}")
    os.makedirs(outPath, exist_ok=True)
    xml_group_content = HTML_GROUP_TEMPLATE
    xml_groups:list[str] = []
    for html_file in htmlFiles:
        xml_group = xml_group_content.replace("$YOUR_HTML$", html_file)
        xml_groups.append(xml_group)

    xml_content = RUNDOWN_TEMPLATE.replace("$YOUR_HTML_GROUP$", "\n".join(xml_groups))
    name = os.path.basename(htmlPath)
    name = os.path.splitext(name)[0]
    out_file = os.path.join(outPath, f"{name}.xml")
    with open(out_file, "w") as f_out:
        f_out.write(xml_content)
    
    print(f"Generated rundown XML at {out_file}")