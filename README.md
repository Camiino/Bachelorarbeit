# Motion Capture Processing Pipeline

This repository contains a step-by-step pipeline for cleaning and analysing
marker based motion capture recordings. Raw CSV exports are transformed through
a series of scripts into averaged trajectories and final plots.

## Directory structure

- `Exports/`
  - `Probant*/` – raw recordings grouped by participant (`Probant`) and
    experiment.
  - `Daten_Raw/` – copy of all raw CSV files organised by experiment.
  - `Daten_Raw_Formatted/` – output of **Step1**, raw data converted to
    semicolon-separated CSV files with uniform columns.
  - `Daten_Raw_Clean/` – output of **Step2**, cleaned marker positions.
  - `Reference/` – reference recordings for markers 4 and 5 used during
    interpolation.
  - `Daten_Raw_Interpolated/` – output of **Step3**, files where internal gaps
    are interpolated and missing head/tail segments are filled from reference
    data.
  - `Daten_Trimmed/` – output of **Step4**, recordings truncated once movement
    stops.
  - `Daten_Averaged_1M/` – output of **Step5**, averages across repeated trials
    for a single probant and experiment.
  - `Final_Averages_1M/` – output of **Step6**, averages across probants for each
    experiment.
  - `Final_Cleaned/` – output of **Step7**, smoothed trajectories.
  - `Plots/` – output of **Step8**, velocity and acceleration plots.
  - `Clustered/` – output of **Step9**, aggregated data by demographic clusters.

## Processing steps

1. **Step1_csv_formatter.py** – normalize raw CSV files and switch delimiters.
2. **Step2_data_clean_recursive.py** – parse marker columns and replace missing
   base marker values with temporary ones.
3. **Step2-5_references.py** – select best reference recordings for markers 4
   and 5.
4. **Step3_interpolate.py** – interpolate internal gaps and use reference data
   for remaining segments.
5. **Step4_trim.py** – remove trailing frames after motion has ceased.
6. **Step5_average_1M.py** – average multiple trials per probant and experiment.
7. **Step6_average_by_experiment_1M.py** – average probant means for each
   experiment.
8. **Step7_clean_final_data.py** – apply Savitzky–Golay smoothing to averaged
   trajectories.
9. **Step8_plots.py** – generate velocity and acceleration plots for the final
   trajectories.
10. **Step9_Segmentation.py** – aggregate results into demographic clusters and
    produce summary plots.

Additional utilities:

- **data_clean_v1.py** – early prototype of the cleaning procedure.
- **visualize_marker_trajectories.py** – render 3D animations of marker
  trajectories from a processed CSV file.

## Usage

Each step expects the output of the previous step to exist in the `Exports`
folder. Run scripts in numerical order to reproduce the full pipeline:

```bash
python Step1_csv_formatter.py
python Step2_data_clean_recursive.py
python Step2-5_references.py
python Step3_interpolate.py
python Step4_trim.py
python Step5_average_1M.py
python Step6_average_by_experiment_1M.py
python Step7_clean_final_data.py
python Step8_plots.py
python Step9_Segmentation.py
```

The optional `visualize_marker_trajectories.py` can be used on any processed CSV
file to inspect marker paths in three dimensions.
