from mpl_toolkits.mplot3d import axes3d
from matplotlib import animation
from matplotlib.animation import HTMLWriter
from mpl_toolkits.mplot3d import Axes3D   
import matplotlib.pyplot as pl
import numpy as np
import warnings
import sys, os

def blockPrint():
    """
    Blocks print output for io
    """
    sys.stdout = open(os.devnull, 'w')


def enablePrint():
    """
    Enables print output for io
    """
    sys.stdout = sys.__stdout__
    
def rotate_3d(df, x, y, z, save_file=True):
    """
    Creates a .gif file of the rotating 3d plot with gives axes
    
    Parameters
    ----------
    df : pd.dataFrame : 
        dataframe of the results data taken from the prediciton study. Assumes
        results are in df['Predicted'] and there are 4 classes to predict
    x : string :
        x axis df label for 3d plot
    y : string : 
        y axis df label for 3d plot
    z : string :
        z axis df label for 3d plot
    Returns
    -------
    rot_animation : object :
        FuncAnimation object containing animation data
    """
    
    def init():
        ax.scatter(df_P14_pred[x], df_P14_pred[y], df_P14_pred[z], marker = 'o', alpha = 0.2)
        ax.scatter(df_P21_pred[x], df_P21_pred[y], df_P21_pred[z], marker = 'o', alpha = 0.2)
        ax.scatter(df_P28_pred[x], df_P28_pred[y], df_P28_pred[z], marker = 'o', alpha = 0.2)
        ax.scatter(df_P35_pred[x], df_P35_pred[y], df_P35_pred[z], marker = 'o', alpha = 0.2)

        ax.set_xlabel(x)
        ax.set_ylabel(y)
        ax.set_zlabel(z)
        leg = pl.legend(['P14', 'P21', 'P28', 'P35'])
        for lh in leg.legendHandles: 
            lh.set_alpha(1)
        return fig,

    def rotate(angle):
        ax.view_init(azim=angle)
        return fig,
    
    # Disable matplotlib interaction
    pl.ioff()
    # Disable warnings that FuncAnimation() gives
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        
        fig = pl.figure()
        ax = Axes3D(fig)
        df_P14_pred = df[df['predicted'] == 0]
        df_P21_pred = df[df['predicted'] == 1]
        df_P28_pred = df[df['predicted'] == 2]
        df_P35_pred = df[df['predicted'] == 3]

        rot_animation = animation.FuncAnimation(fig, rotate, init_func=init, frames=np.arange(0,407,2),interval=50, repeat=True)
        if save_file:
            rot_animation.save(f'./gif_rotation_{x}_{y}_{z}.gif'.replace(' ', ''), writer='imagemagick', fps=20)
        # Close plot if using %matplotlib inline
        pl.close()
    return rot_animation