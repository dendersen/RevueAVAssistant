# Dependencies
import argparse
import logging
import os

import rava_utils
import shutil

def main():
    # Set up the logging.
    logging.basicConfig(
        level=logging.INFO,
        format="RevueAVAssistant: %(asctime)s - %(levelname)s - %(message)s",
    )

    # Set up the arguments and parse it.
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("--project", type=str, help='Project name, e.g. "revue_2022".')
    
    args: argparse.Namespace = parser.parse_args()
    assert args.project is not None, "--project name not given."
    assert os.path.exists(args.project), f"The folder {args.project} does not exist. Please copy revue_template and populate the <project>/lyrics/00_raw/ folder."

    #Find the tex files in the folder.
    raw_paths:list[str] = sorted(rava_utils.find_raw_lyrics(args.project))

    if len(raw_paths) == 0:
        logging.info(f'No files found in {args.project}/lyrics/00_raw. Quitting.')
        return

    for path_raw in raw_paths:
        #p_00 is the raw path, p_01 is the .txt path, p_02 is the .pptx path, p_03 is the .png folder path.
        song = os.path.basename(path_raw).split('.')[0]

        logging.info(f'{song}: processing...')
        path_txt = os.path.join(".",f'{args.project}','lyrics', '01_preprocessed', f'{song}.txt')
        path_pptx = os.path.join(".",f'{args.project}','lyrics', '02_pptx', f'{song}.pptx')
        path_png = os.path.join(".",f'{args.project}','lyrics', '03_png', f'{song}')

        #If p_01 exists, skip. 
        
        # NEW removed skip, in case of manual fixes, always do them all again
        # who even cares about speed at this point, we have time for now
        
        # if os.path.exists(path_txt):
        #     logging.info(f'{song}: 00 -> 01 skipped, preprocessed song already exists.')
        # elif path_raw.endswith('.txt'):
        if path_raw.endswith('.txt'):
            #If the file is already a .txt file, just copy it.
            shutil.copy(path_raw, path_txt)
        else:
            valid = rava_utils.preprocess_tex(path_in = path_raw, path_out = path_txt, name = song)
            if not valid:
                logging.info(f'{song}: skipped, no \\begin{{obeylines}} and \\end{{obeylines}} found or othwise invlaid')
                continue
            else:
                logging.info(f'{song}: 00 -> 01 done.')
        
        # NEW always make new, don't check time
        # if os.path.exists(path_pptx) and os.path.getmtime(path_pptx) > os.path.getmtime(path_txt):
        #     #If p_02 is newer than p_01, skip.
        #     logging.info(f'{song}: 01 -> 02 skipped, pptx is up to date.')
        # elif not os.path.exists(path_txt):
        if not os.path.exists(path_txt):
            logging.info(f'{song}: 01 -> 02 skipped. preprocessed file does not exist.')
            logging.info(f'{song}: 02 -> 03 skipped. preprocessed file does not exist.')
            print('')
            continue
        else:
            #Load the preprocessed song.
            song_preprocessed = open(path_txt, "r").readlines()

            #Create the pptx.
            rava_utils.create_pptx(song_preprocessed, path_pptx)
            logging.info(f'{song}: 01 -> 02 done.')

        os.makedirs(path_png, exist_ok=True)
        # NEW always make new, don't check time
        # if os.path.isdir(path_png):
        #     #Check if all of the pngs in this folder are newer than the pptx.
        #     png_files = [os.path.join(path_png, x) for x in os.listdir(path_png) if x.endswith('.png')]
        # 
        #     if len(png_files) > 0:
        #         #Check that all png files are newer than the pptx.
        #         if all([os.path.getmtime(x) > os.path.getmtime(path_pptx) for x in png_files]):
        #             logging.info(f'{song}: 02 -> 03 skipped. png is already up to date.')
        #             print('')
        #             continue

        # else:
        #     os.mkdir(path_png)

        
        #remove old png's
        for x in os.listdir(path_png):
            if x.endswith('.png'):
                os.remove(os.path.join(path_png, x))
        
        #Fill the folder with pngs.
        logging.info(f'{song}: 02 -> 03 creating pngs, please wait...')
        rava_utils.pptx_to_png(path_pptx, outfolder=path_png)

        #Check the number of pngs in the folder.
        png_files = [os.path.join(path_png, x) for x in os.listdir(path_png) if x.endswith('.png')]

        # NEW removes before creating new png's
        # #Remove pngs that are *older* than the pptx. 
        # any_png_removed = False
        # for png in png_files:
        #     if os.path.getmtime(png) < os.path.getmtime(path_pptx):
        #         os.remove(png)
        #         any_png_removed = True

        # number_of_png_files = len([os.path.join(path_png, x) for x in os.listdir(path_png) if x.endswith('.png')])
        # 
        # if any_png_removed:
        #     logging.info(f'{song}: 02 -> 03 removed old pngs. Make sure that QLab is not using them.')

        logging.info(f'{song}: 02 -> 03 complete, {len(png_files)} pngs written to {path_png}.')

        print('')

    return

if __name__ == "__main__":
    main()
