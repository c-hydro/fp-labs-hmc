#!/bin/bash -e

#-----------------------------------------------------------------------------------------
# Script information
script_name='FP LABS - RUNNER JUPITER-LAB ENVIRONMENT - HMC'
script_version="1.0.0"
script_date='2021/01/12'

script_folder='$HOME/fp-labs-hmc/'
fp_virtualenv_folder='$HOME/fp_virtualenv_python3_hmc/'
fp_virtualenv_libs='fp_virtualenv_python3_hmc_libraries'

# Jupyter lab interactive graph:
# https://towardsdatascience.com/how-to-produce-interactive-matplotlib-plots-in-jupyter-environment-1e4329d71651
# NodeJS=12
# https://github.com/jupyterlab/jupyterlab/issues/7526
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Activate virtualenv
export PATH=$fp_virtualenv_folder/bin:$PATH
source activate $fp_virtualenv_libs

# Add path to pythonpath
export PYTHONPATH="${PYTHONPATH}:$script_folder"
#-----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# Info script start
echo " ==================================================================================="
echo " ==> "$script_name" (Version: "$script_version" Release_Date: "$script_date")"
echo " ==> START ..."
echo " ===> EXECUTION ..."

time_now=$(date -d "$time_now" +'%Y-%m-%d %H:00')
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# Cmd for runner jupyter lab
cmd_runner="jupyter-lab"

# Check jupyter-lab installation
echo " ====> CHECK JUPYTER-LAB INSTALLATION ..."
if ! type "$cmd_runner" > /dev/null; then
    echo " ====> CHECK JUPYTER-LAB INSTALLATION ... FAILED. TRY TO INSTALL THE JUPYTER-LAB IN THE VIRTUAL ENVIRONMENT"
    echo " =====> INSTALL JUPYTER-LAB ... "
    #conda install -y -n $fp_virtualenv_libs -c conda-forge cartopy=0.17
    conda install -y -n $fp_virtualenv_libs -c conda-forge jupyterlab
    conda install -y -n $fp_virtualenv_libs -c conda-forge ipywidgets
    conda install -y -n $fp_virtualenv_libs -c conda-forge ipympl
    conda install -y -n $fp_virtualenv_libs -c conda-forge nodejs=12
    jupyter labextension install @jupyter-widgets/jupyterlab-manager
    jupyter lab build
    echo " =====> INSTALL JUPYTER-LAB ... DONE"
else
    echo " ====> CHECK JUPYTER-LAB INSTALLATION ... DONE"
fi
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# Run jupiter-lab
echo " ====> RUN JUPYTER NOTEBOOK ... "
${cmd_runner}
echo " ====> RUN JUPYTER NOTEBOOK ... DONE"
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# Info script end
echo " ===> EXECUTION ... DONE"
echo " ==> "$script_name" (Version: "$script_version" Release_Date: "$script_date")"
echo " ==> Bye, Bye"
echo " ==================================================================================="
# ----------------------------------------------------------------------------------------



