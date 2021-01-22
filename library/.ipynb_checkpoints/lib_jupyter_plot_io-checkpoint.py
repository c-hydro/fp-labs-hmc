"""
Library Features:

Name:          lib_jupyter_plot_io
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20210113'
Version:       '1.0.0'
"""
#######################################################################################
# Libraries
import os
#######################################################################################


# -------------------------------------------------------------------------------------
# Method to save ts plot
def save_ts(file_name, fig_handle, fig_dpi=120):
    if not os.path.exists(file_name):
        make_folder(file_name)
    fig_handle.savefig(file_name, dpi=fig_dpi)
# -------------------------------------------------------------------------------------
