import polars as pl
import os

# change directory to the directory of this file
# this script creates a directory in the parent directory of the directory of this file
# meaning, if script is in folder/scripts, the directory created will be folder/data
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

def load_gpa_data() -> pl.DataFrame:
    gpa_data = pl.read_ipc("data/gpa.feather")
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


gpa_dataframe = load_gpa_data()

print(gpa_dataframe)