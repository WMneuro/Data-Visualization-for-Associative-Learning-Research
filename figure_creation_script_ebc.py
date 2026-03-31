# python script for generating figures using seaborn, matplotlib.
import seaborn as sns
import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np
from pathlib import Path

try: 
    script_dir = Path(__file__).resolve().parent
except NameError: 
    script_dir = Path.cwd()

data_path = script_dir / "asymetrical_gen_offcues_data.xlsx"

male_female_all_data = pd.read_excel(data_path) 

male_female_toneoff_data = male_female_all_data[male_female_all_data['cs_type'] == 'toneoff'].reset_index(drop=True)

group_colors = {'male': 'tab:purple', 'female': 'tab:orange', 'toneon': 'tab:cyan', 'toneoff': 'tab:pink'}

# plot tone-off acquisition data between sex
def reshape_acquisition_data(male_female_toneoff_data): 
    '''prepares the acquisition data for plotting'''
    
    session_cols_acquisition = [f'session_{i}' for i in range(1,11)] # define which columns are the timepoints (session numbers 1-10)
    
    data_long = male_female_toneoff_data.melt(id_vars= ['rat_id', 'sex', 'cs_type'], # melt the data so it can be used in lineplot
                              value_vars= session_cols_acquisition, 
                              var_name= 'session', 
                              value_name= 'cr_percent'
                              )
    data_long['session'] = data_long['session'].str.extract(r'(\d+)').astype(int) # extracts the session number as an int
    
    data_long['sex'] = pd.Categorical(data_long['sex'], # turn sex into a categorical variable so sns.linplot goes in the right order
                                          categories= ['male', 'female'],   # specify order
                                          ordered= True
                                          )
    data_long['cs_type'] = pd.Categorical(data_long['cs_type'],
                                          categories= ['toneon', 'toneoff'],
                                          ordered= True
    )
    return data_long

# set defaults plt.show
def plot_style():
    '''sets the style for the acquisition plot'''

    sns.set_theme(style= "ticks")
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.size": 12,
        "axes.labelsize": 12,
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,
        "axes.labelcolor": "black",
        "axes.edgecolor": "black",
        "xtick.color": "black",
        "ytick.color": "black"
        })

plot_style()

# plot male vs. female tone-off acquisition
def plot_acquisition(male_female_toneoff_data, hue, style, markers, labels, base_name):
    '''generates the lineplot of the acquisition data'''
    
    male_female_toneoff_data_long = reshape_acquisition_data(male_female_toneoff_data)

    fig, ax = plt.subplots(figsize= (7,4))
       
    sns.lineplot(data= male_female_toneoff_data_long, 
                x='session', 
                y= 'cr_percent',
                err_style= 'bars',
                errorbar= 'se',
                linewidth= 2,
                markersize= 7,
                hue= hue,
                style= style,
                dashes= False,
                markers= markers,
                markeredgewidth= 0,
                palette= group_colors,
                ax= ax
    )
    sns.despine()
    ax.set_xlabel('Session (days)')
    ax.set_ylabel('%CR')
    ax.set_xlim(.5,10.5)
    ax.set_ylim(0, 100)
    ax.set_yticks(np.arange(0, 101, 10))
    ax.set_xticks(range(1, 11))
    legend_aq = ax.legend(labels= labels,
        title= None,
        loc= 'upper left',
        frameon= False, 
        framealpha= 0,
        )

    for text in legend_aq.get_texts():
        text.set_color('black')
    
    plt.tight_layout()
    
    fig_dir = Path("Figures")
    fig_dir.mkdir(exist_ok=True)

    base_name = base_name

    fig.savefig((fig_dir / base_name).with_suffix('.pdf'),
            bbox_inches='tight',
            dpi=300)

    fig.savefig((fig_dir / base_name).with_suffix('.png'),
            bbox_inches='tight',
            dpi=300)
    
    plt.show()
    
    return fig, ax

plot_acquisition(male_female_toneoff_data= male_female_toneoff_data, 
                 hue= 'sex', style= 'sex',
                 markers= {'male': 'o', 'female': 's'},
                 labels= ['Male', 'Female'],
                 base_name= "Tone-off males and females acquisition")

# plot immediate generalization between sex 
def plot_immediate_generalization(male_female_toneoff_data, x_bar, x_tick_labels, order, group_colors, base_name): 
    '''generates a barplot to visualize immediate generalization between sex''' 

    fig, ax = plt.subplots(figsize= (4,4))

    sns.barplot(data= male_female_toneoff_data,
                x= x_bar,
                y= 'session_11',
                order= order,
                errorbar= 'se',
                errcolor= 'black',
                capsize= .15,
                edgecolor= 'black',
                linewidth= 2,
                palette= group_colors,
                ax= ax
                )
    
    sns.despine()
    ax.set_xlabel(None)
    ax.set_ylabel('%CR')
    ax.set_ylim(0, 100)
    ax.set_yticks(np.arange(0, 101, 10))
    ax.set_xticklabels(x_tick_labels)
        
    plt.tight_layout()
    
    fig_dir = Path("Figures")
    fig_dir.mkdir(exist_ok=True)

    base_name = base_name

    fig.savefig((fig_dir / base_name).with_suffix('.pdf'),
            bbox_inches='tight',
            dpi=300)

    fig.savefig((fig_dir / base_name).with_suffix('.png'),
            bbox_inches='tight',
            dpi=300)
    
    plt.show()
    
    return fig, ax

plot_immediate_generalization(male_female_toneoff_data= male_female_toneoff_data,
                              x_bar= 'sex',
                              order= ['male', 'female'],
                              x_tick_labels= ['Male', 'Female'],
                              group_colors= group_colors,
                              base_name = "Tone-off sex immediate gen")

# reshape the immediate generalization data and plot 
def reshape_immediate_gen_blocks(male_female_toneoff_data): 
    '''reshapes the immediate generalization 10-trial block data''' 
    
    gen_cols = ['immediate_gen_block_1', 'immediate_gen_block_2']
    
    gen_block10_data = male_female_toneoff_data.melt(id_vars= ['rat_id', 'sex', 'cs_type'],
                                                     value_vars= gen_cols,
                                                     var_name= 'block',
                                                     value_name= 'cr_percent'
    )

    gen_block10_data['block'] = gen_block10_data['block'].str.extract(r'(\d+)').astype(int)

    gen_block10_data['sex'] = pd.Categorical(gen_block10_data['sex'],
                                             categories= ['male', 'female'],
                                             ordered= True
    )

    gen_block10_data['cs_type'] = pd.Categorical(gen_block10_data['cs_type'],
                                                 categories= ['toneon', 'toneoff'],
                                                 ordered= True
    )

    return gen_block10_data

def plot_immediate_gen_blocks(male_female_toneoff_data, hue, style, markers, labels, base_name): 
    '''creates a lineplot visualization of the immediate gen data in 10-trial blocks'''

    gen_block10_data = reshape_immediate_gen_blocks(male_female_toneoff_data)

    fig, ax = plt.subplots(figsize= (4,4))

    sns.lineplot(data= gen_block10_data,
                 x='block', 
                 y= 'cr_percent',
                 err_style= 'bars',
                 errorbar= 'se',
                 linewidth= 3,
                 markersize= 10,
                 hue= hue,
                 style= style,
                 dashes= False,
                 markers= markers,
                 markeredgewidth= 0,
                 palette= group_colors,
                 ax= ax
    )

    sns.despine()
    ax.set_xlabel('10-Trial Blocks')
    ax.set_ylabel('%CR')
    ax.set_yticks(np.arange(0, 101, 10))
    ax.set_xticks([1, 2])
    ax.margins(x= 0)
    ax.set_xlim(.75, 2.25)
    ax.set_ylim(0, 100)
    legend_imgen = ax.legend(
        labels= labels,
        title= None,
        loc= 'upper left',
        frameon= False, 
        framealpha= 0,
        )
    
    for text in legend_imgen.get_texts():
        text.set_color('black')
    
    plt.tight_layout()
    
    fig_dir = Path("Figures")
    fig_dir.mkdir(exist_ok=True)

    base_name = base_name

    fig.savefig((fig_dir / base_name).with_suffix('.pdf'),
            bbox_inches='tight',
            dpi=300)

    fig.savefig((fig_dir / base_name).with_suffix('.png'),
            bbox_inches='tight',
            dpi=300)
    
    plt.show()
    
    return fig, ax

plot_immediate_gen_blocks(male_female_toneoff_data= male_female_toneoff_data,
                          hue= 'sex', style= 'sex',
                          markers= {'male': 'o', 'female': 's'},
                          labels = ['Male', 'Female'],
                          base_name = 'Tone-off males and females immediate gen blocks')

# reshape general transfer data
def reshape_transfer_data(male_female_toneoff_data): 
    '''prepares the general transfer data for plotting'''
    
    session_cols_transfer = [f'session_{i}' for i in range(12,15)] # define which columns are the timepoints (session numbers 12-14)
    
    data_long_transfer = male_female_toneoff_data.melt(id_vars= ['rat_id', 'sex', 'cs_type'], # melt the data so it can be used in lineplot
                              value_vars= session_cols_transfer, 
                              var_name= 'session', 
                              value_name= 'cr_percent'
                              )
    data_long_transfer['session'] = data_long_transfer['session'].str.extract(r'(\d+)').astype(int) # extracts the session number as an int
    
    data_long_transfer['sex'] = pd.Categorical(data_long_transfer['sex'], # turn sex into a categorical variable so sns.linplot goes in the right order
                                          categories= ['male', 'female'],   # specify order
                                          ordered= True
                                          )
    data_long_transfer['cs_type'] = pd.Categorical(data_long_transfer['cs_type'],
                                          categories= ['toneon', 'toneoff'],
                                          ordered= True
    )
    return data_long_transfer

# plot general transfer
def plot_general_transfer(male_female_toneoff_data, hue, style, markers, labels, base_name): 
    '''generates the lineplot of the general transfer data'''
        
    male_female_toneoff_data_long_transfer = reshape_transfer_data(male_female_toneoff_data)

    fig, ax = plt.subplots(figsize= (7,4))
       
    sns.lineplot(data= male_female_toneoff_data_long_transfer, 
                x='session', 
                y= 'cr_percent',
                err_style= 'bars',
                errorbar= 'se',
                linewidth= 2,
                markersize= 7,
                hue= hue,
                style= style,
                dashes= False,
                markers= markers,
                markeredgewidth= 0,
                palette= group_colors,
                ax= ax
    )
    sns.despine()
    ax.set_xlabel('Session (days)')
    ax.set_ylabel('%CR')
    ax.set_xlim(11.5,14.5)
    ax.set_ylim(0, 100)
    ax.set_yticks(np.arange(0, 101, 10))
    ax.set_xticks(range(12, 15))
    legend_aq = ax.legend(labels= labels,
        title= None,
        loc= 'center right',
        frameon= False, 
        framealpha= 0,
        )

    for text in legend_aq.get_texts():
        text.set_color('black')
    
    plt.tight_layout()
    
    fig_dir = Path("Figures")
    fig_dir.mkdir(exist_ok=True)

    base_name = base_name

    fig.savefig((fig_dir / base_name).with_suffix('.pdf'),
            bbox_inches='tight',
            dpi=300)

    fig.savefig((fig_dir / base_name).with_suffix('.png'),
            bbox_inches='tight',
            dpi=300)
    
    plt.show()
    
    return fig, ax    

plot_general_transfer(male_female_toneoff_data= male_female_toneoff_data, 
                 hue= 'sex', style= 'sex',
                 markers= {'male': 'o', 'female': 's'},
                 labels= ['Male', 'Female'],
                 base_name= "Tone-off males and females general transfer")

# reshape the extinction data and plot for male vs female tone off
def reshape_extinction_data(male_female_toneoff_data):
    '''reshapes the extinction data''' 

    session_cols_extinction = [f'session_{i}' for i in range(15,17)] # define which columns are the timepoints (session numbers 15-16)
    
    data_long_ext = male_female_toneoff_data.melt(id_vars= ['rat_id', 'sex', 'cs_type'], # melt the data so it can be used in lineplot
                              value_vars= session_cols_extinction, 
                              var_name= 'session', 
                              value_name= 'cr_percent'
                              )
    data_long_ext['session'] = data_long_ext['session'].str.extract(r'(\d+)').astype(int) # extracts the session number as an int
    
    data_long_ext['sex'] = pd.Categorical(data_long_ext['sex'], # turn sex into a categorical variable so sns.linplot goes in the right order
                                          categories= ['male', 'female'],   # specify order
                                          ordered= True
                                        )
    data_long_ext['cs_type'] = pd.Categorical(data_long_ext['cs_type'],
                                          categories= ['toneon', 'toneoff'],
                                          ordered= True
                                        )
    return data_long_ext   
   
def plot_extinction(male_female_toneoff_data, hue, style, markers, labels, base_name):
    '''creates a lineplot for the extinction data''' 

    male_female_toneoff_data_long_ext = reshape_extinction_data(male_female_toneoff_data)

    fig, ax = plt.subplots(figsize= (7,4))
       
    sns.lineplot(data= male_female_toneoff_data_long_ext, 
                x='session', 
                y= 'cr_percent',
                err_style= 'bars',
                errorbar= 'se',
                linewidth= 2,
                markersize= 7,
                hue= hue,
                style= style,
                dashes= False,
                markers= markers,
                markeredgewidth= 0,
                palette= group_colors,
                ax= ax
    )
    sns.despine()
    ax.set_xlabel('Session (days)')
    ax.set_ylabel('%CR')
    ax.set_xlim(14.5,16.5)
    ax.set_ylim(0, 100)
    ax.set_yticks(np.arange(0, 101, 10))
    ax.set_xticks(range(15, 17))
    legend_aq = ax.legend(labels= labels,
        title= None,
        loc= 'upper left',
        frameon= False, 
        framealpha= 0,
        )

    for text in legend_aq.get_texts():
        text.set_color('black')
    
    plt.tight_layout()
    
    fig_dir = Path("Figures")
    fig_dir.mkdir(exist_ok=True)

    base_name = base_name

    fig.savefig((fig_dir / base_name).with_suffix('.pdf'),
            bbox_inches='tight',
            dpi=300)

    fig.savefig((fig_dir / base_name).with_suffix('.png'),
            bbox_inches='tight',
            dpi=300)
    
    plt.show()
    
    return fig, ax

plot_extinction(male_female_toneoff_data= male_female_toneoff_data, 
                 hue= 'sex', style= 'sex',
                 markers= {'male': 'o', 'female': 's'},
                 labels= ['Male', 'Female'],
                 base_name= "Tone-off males and females extinction")

# plot tone-on to tone-off males only 
male_tone_data = male_female_all_data[male_female_all_data['sex'] == 'male'].reset_index(drop=True)

plot_acquisition(male_female_toneoff_data= male_tone_data, 
                 hue= 'cs_type', style= 'cs_type', 
                 markers= {'toneon': 'o', 'toneoff': 's'},
                 labels= ['Tone-On', 'Tone-Off'],
                 base_name= 'tone-on and tone-off males aquisition')

plot_immediate_generalization(male_female_toneoff_data = male_tone_data,
                              x_bar= 'cs_type',
                              x_tick_labels= ['Tone-On', 'Tone-Off'],
                              order= ['toneon', 'toneoff'],
                              group_colors= group_colors,
                              base_name= 'tone-on and tone-off immediate gen')

plot_immediate_gen_blocks(male_female_toneoff_data = male_tone_data, 
                          hue= 'cs_type', style= 'cs_type', 
                          markers= {'toneon': 'o', 'toneoff': 's'},
                          labels= ['Tone-On', 'Tone-Off'],
                          base_name= 'tone-on and tone-off gen blocks')

plot_general_transfer(male_female_toneoff_data= male_tone_data, 
                      hue= 'cs_type', style= 'cs_type', 
                      markers= {'toneon': 'o', 'toneoff': 's'},
                      labels= ['Tone-On', 'Tone-Off'],
                      base_name= 'tone-on and tone-off males general transfer')

plot_extinction(male_female_toneoff_data= male_tone_data, 
                 hue= 'cs_type', style= 'cs_type',
                 markers= {'toneon': 'o', 'toneoff': 's'},
                 labels= ['Tone-On', 'Tone-Off'],
                 base_name= "tone-on and tone-off males extinction")
                        