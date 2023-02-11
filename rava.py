# Dependencies
import numpy as np
import argparse
import os
import logging
import shutil

import rava_utils


def main():
    # Set up the logging.
    logging.basicConfig(
        level=logging.INFO,
        format="RevueAVAssistant: %(asctime)s - %(levelname)s - %(message)s",
    )

    # Set up the arguments and parse it.
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=str, help='Project name, e.g. "revue_2022".')

    args = parser.parse_args()
    assert args.project is not None, "--project name not given."
    assert os.path.exists(
        args.project
    ), f"The folder {args.project} does not exist. Please copy revue_template and populate the <project>/lyrics/tex/ folder."

    # Read in the paths of all existing files.
    tex_paths = rava_utils.find_tex_lyrics(args.project)
    txt_paths = rava_utils.find_txt_lyrics(args.project)

    # Load the songs.
    tex_songs = rava_utils.read_files(tex_paths)
    txt_songs = rava_utils.read_files(txt_paths)

    # Preprocess the songs.
    tex_songs_preprocessed = rava_utils.preprocess_tex_songs(tex_songs, tex_paths)
    txt_songs_preprocessed = rava_utils.preprocess_txt_songs(txt_songs, txt_paths)

    # Now, we loop over the songs and if the png is older than the tex or txt file, we first make it into a pptx and then png.
    for i, (tex_path, tex_song) in enumerate(zip(tex_paths, tex_songs_preprocessed)):
        song_name = os.path.basename(tex_path).replace(".tex", "")
        folder_name = os.path.join(args.project, "lyrics", "02_png", song_name)

        # If the folder doesn't exist in args.project/lyrics/png, we make it.
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)

        # If the folder exists, we check if the png is older than the tex file.
        else:
            # Get the pngs in the folder.
            pngs = [
                os.path.join(folder_name, x)
                for x in os.listdir(folder_name)
                if x.endswith(".png")
            ]

            # Check if they are all older than the tex file.
            print(all([os.path.getmtime(x) < os.path.getmtime(tex_path) for x in pngs]))

    for i, (txt_path, txt_song) in enumerate(zip(txt_paths, txt_songs_preprocessed)):
        song_name = os.path.basename(txt_path).replace(".txt", "")
        folder_name = os.path.join(args.project, "lyrics", "02_png", song_name)

        # Similarly with txt, create the folder.
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)

        else:
            # Get the pngs in the folder.
            pngs = [
                os.path.join(folder_name, x)
                for x in os.listdir(folder_name)
                if x.endswith(".png")
            ]
    
        # Check if all pngs are newer than the txt file.
        if all([os.path.getmtime(x) < os.path.getmtime(txt_path) for x in pngs]):

            # First, we make the pptx.
            pptx_path = os.path.join(
                args.project, "lyrics", "01_pptx", song_name + ".pptx"
            )
            rava_utils.create_pptx(txt_song, pptx_path)

            # Then, we make the pngs.
            rava_utils.pptx_to_png(pptx_path, outfolder=folder_name)
        else:
            print(f"{song_name} is up to date.")

    return


if __name__ == "__main__":
    main()
