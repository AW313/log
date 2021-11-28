"""
Load up LAS files, correct any spikes or data gaps, plot for quick display and save out csv if needed

change the file path to a root folder for your LAS files. 

"""



import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import re
import lasio
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class LogLoad:
    def __init__(self):
        pass

    def load_las_paths(self, path):
        """
        search for las files from a root folder path you provide
        """
        # os.chdir(path)
        las_path_list = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if file[-3:].lower()=='las':
                    las_path_list.append(root+'\\'+file)
        return las_path_list

    def load_lasio(self, las_path):
        """
        load las files with Lasio, edit, export as csv
        """
        print('starting ', las_path)
        lasio_las = lasio.read(las_path)
        df = lasio_las.df() # convert to pandas df
        df.replace(-999.25, np.nan, inplace=True)
        df.mask(df<-1000, inplace=True)  #replace outliers with nan
        df.mask(df>1000, inplace=True) #replace outliers with nan
        df.interpolate(method='linear', limit_area='inside', limit=500, inplace=True) #interpolate internal data gaps - removes all nas
        # df.to_csv(f'{las_path[:-4]}_2cleaned.csv')

        #save out las
        # lasio_las.set_data(df)
        # lasio_las.write(las_path[:-4]+'_cleaned.las', version=2.0)
        return df


def plot_log(df, log_name=''):
    
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    for col in df.columns:
        fig.add_trace(
            go.Scatter(x=df[col], y=df.index*-1, name=col),
            secondary_y=False,)
        

    # Add figure title
    fig.update_layout(title_text=f"{log_name} Display")

    # Set x-axis title
    fig.update_xaxes(title_text="Log Limits")

    # Set y-axes titles
    fig.update_yaxes(title_text="Depth MD", secondary_y=False)

    fig.show()

def plot_dual_log(df, log_name=''):
    fig = make_subplots(rows=1, cols=2,
                        specs=[[{"secondary_y": True}, {"secondary_y": True}]])
    fig.update_layout(title_text=f"{log_name} Display")
    for col in df.columns:
        if df[col].max() < 10:
            # Top left
            fig.add_trace(go.Scatter(x=df[col], y=df.index*-1, name=col), row=1, col=1, secondary_y=False)
            fig.update_xaxes(title_text="Log Limits")
            fig.update_yaxes(title_text="Depth MD")
        else:
            fig.add_trace(go.Scatter(x=df[col], y=df.index*-1, name=col),row=1, col=2, secondary_y=False,)
            fig.update_xaxes(title_text="Log Limits")
            fig.update_yaxes(title_text="Depth MD")
    fig.show()

def main():
    print('lets go')
    path = 'C:\\Users\\muddy\\Documents\\Python Programming\\01 MyPythonScripts\\well docos\\royal oak\\Digital_Data\\'
    l = LogLoad()
    file_paths = l.load_las_paths(path)
    for files in file_paths:
        df = l.load_lasio(files)

        plot_log(df, files[:-4])
        plot_dual_log(df, files[:-4])



if __name__=='__main__':
    main()
