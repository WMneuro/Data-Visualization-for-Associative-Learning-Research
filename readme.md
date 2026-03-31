Asymmetrical Generalization Off-Cues Analysis
Data visualization of eyeblink conditioning generalization data using Python.

This project visualizes acquisition and generalization data from male and female rats 
trained on tone-off conditioned stimuli, and compares tone-on and tone-off conditioned 
stimulus types in male rats.

Repository Structure:

tone_cs_figures_script.py – main analysis script
asymmetrical_gen_offcues_data.xlsx – dataset used for analysis. This is not provided.
Figures/ – generated figures

Methods:

The script reshapes raw session and generalization block data into long format for plotting.
The script generates acquisition lineplots, immediate generalization barplots, and 
10-trial block lineplots across sex and CS type comparisons.

Installation:

pip install -r requirements.txt

Running the Analysis:

tone_cs_figures_script.py