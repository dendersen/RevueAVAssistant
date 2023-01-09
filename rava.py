# Dependencies
import numpy as np
import argparse
import os

from rava_utils import PPTXSong, tex_to_pptx, pptx_to_png


def main():

    # Set up the arguments and parse it.
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=str, help='Project name, e.g. "Revy2022".')

    args = parser.parse_args()

    assert args.project is not None, "--project name not given."

    # Find the songs in tex folder.
    tex = [
        os.path.join(args.project, "tex", x)
        for x in os.listdir(os.path.join(args.project, "tex"))
        if x.endswith(".tex")
    ]

    for tex_file in tex:

        # Infile is .tex, outfile is .pptx
        pptx_file = tex_file.replace("/tex/", "/pptx/").replace(".tex", ".pptx")

        # Else convert the tex to pptx.
        tex_to_pptx(
            infile=tex_file,
            outfile=pptx_file,
            config_path=f"{args.project}/config.yaml",
        )

        # And the pptx to png.
        pptx_to_png(infile=pptx_file, outfolder=os.path.join(args.project, "lyrics"))

    return


if __name__ == "__main__":
    main()
