from rmpy import fetch_all_professors # type: ignore
import glob
import os
import pickle 
import polars as pl

async def initialize_professor_cache(pickles_dir: str, load_pickles=True):
    if load_pickles:
        # load professor cache from pickle file
        # glob from pickles_dir to get the latest pickle file
        pickle_files = glob.glob(os.path.join(pickles_dir, "professor_cache*.pkl"))
        if len(pickle_files) == 0:
            # initialize the professor cache
            professor_cache = await fetch_all_professors()
        else:
            # load the latest professor cache
            pickle_files.sort(key=os.path.getmtime)
            professor_cache = pickle.load(open(pickle_files[-1], "rb"))
    else:
        # initialize the professor cache
        professor_cache = await fetch_all_professors()
        
    save_professor_cache(pickles_dir, professor_cache)
    return professor_cache

def save_professor_cache(pickles_dir: str, professor_cache: dict):
    # save professor cache to pickle file
    if not os.path.exists(pickles_dir):
        os.makedirs(pickles_dir)
    pickle.dump(professor_cache, open(os.path.join(pickles_dir, "professor_cache.pkl"), "wb"))

def load_gpa_data(feather_file: str):
    gpa_data = pl.read_ipc(feather_file)
    gpa_data = gpa_data.with_columns(
        [
            (
                (
                    gpa_data["A+"] * 4.0
                    + gpa_data["A"] * 4.0
                    + gpa_data["A-"] * 3.7
                    + gpa_data["B+"] * 3.3
                    + gpa_data["B"] * 3.0
                    + gpa_data["B-"] * 2.7
                    + gpa_data["C+"] * 2.3
                    + gpa_data["C"] * 2.0
                    + gpa_data["C-"] * 1.7
                    + gpa_data["D+"] * 1.3
                    + gpa_data["D"] * 1.0
                    + gpa_data["D-"] * 0.7
                )
                / (
                    gpa_data["A+"]
                    + gpa_data["A"]
                    + gpa_data["A-"]
                    + gpa_data["B+"]
                    + gpa_data["B"]
                    + gpa_data["B-"]
                    + gpa_data["C+"]
                    + gpa_data["C"]
                    + gpa_data["C-"]
                    + gpa_data["D+"]
                    + gpa_data["D"]
                    + gpa_data["D-"]
                    + gpa_data["F"]
                )
            ).alias("GPA")
        ]
    )
    return gpa_data