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
    
def rotate_3d(df, feat, save_file=True, **kwargs):
    """
    Creates a .gif file of the rotating 3d plot with gives axes
    
    Parameters
    ----------
    df        : pd.dataFrame : 
              dataframe of the results data taken from the prediciton study. Assumes
              results are in df['Predicted'] and there are 4 classes to predict
    feat      : [string] :
              [x, y, z] axis df label for 3d plot
    save_file : bool :
              save file or not
    
    kwargs include override parameter dicts for matplotlib.animation.FuncAnimation()
    and matplotlib.animation.FuncAnimation.save(). See API for both of these. 
    Label is 'anim_param' and 'save_param' respectively.
    
    Returns
    -------
    rot_animation : object :
        FuncAnimation object containing animation data
    """
    
    assert all([(i in df.columns) for i in feat]), "Feature(s) not in the dataframe"
    assert len(feat) == 3, "Inputed too many features"
    
    pred_list = df.predicted.unique()
    # Animation/Saving parameters:
    anim_param = {'frames':np.arange(0,407,2),
                  'interval':50,
                  'repeat':True
                 }
    save_param = {'filename':f'./gif_rotation_{feat[0]}_{feat[1]}_{feat[2]}.gif'.replace(' ', ''),
                  'writer':'imagemagick',
                  'fps':20
                 }
    # Override for making and saving animations
    if 'anim_param' in kwargs:
        anim_param.update(kwargs['anim_param'])
    if 'save_param' in kwargs:
        save_param.update(kwargs['save_param'])
        
    # Initial conditions
    def init():
        for cat in pred_list:
            ax.scatter(dict_list[cat][feat[0]], dict_list[cat][feat[1]], dict_list[cat][feat[2]], marker = 'o', alpha = 0.2)
        ax.set_xlabel(feat[0])
        ax.set_ylabel(feat[1])
        ax.set_zlabel(feat[2])
        leg = pl.legend(pred_list)
        for lh in leg.legendHandles: 
            lh.set_alpha(1)
        return fig,
    # Changing conditions
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
        dict_list = []
        for tag in pred_list:
            dict_list.append(df[df['predicted']==tag])
        rot_animation = animation.FuncAnimation(fig=fig, func=rotate, init_func=init, **anim_param)
        if save_file:
            rot_animation.save(**save_param)
        # Close plot if using %matplotlib inline
        pl.close()
    return rot_animation