"""
FP-Labs - Analyzer HMC time-series

__date__ = '20210113'
__version__ = '1.0.0'
__author__ = 'Fabio Delogu (fabio.delogu@cimafoundation.org'
__library__ = 'fp-labs'

General command line:
python fp_labs_analyzer_hmc_timeseries.py -settings_file configuration.json

Version(s):
20210113 (1.0.0) --> Beta release
"""
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# Libraries
import argparse
import time
import os
import pandas as pd

from library.jupyter_generic.lib_jupyter_utils_io import update_json_file

# Import coupler and driver classes
from hmc.driver.configuration.drv_configuration_hmc_logging import ModelLogging
from hmc.coupler.cpl_hmc_manager import ModelInitializer, ModelCleaner
from hmc.coupler.cpl_hmc_builder import ModelBuilder
from hmc.coupler.cpl_hmc_runner import ModelRunner
from hmc.coupler.cpl_hmc_finalizer import ModelFinalizer
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Script Main
def main(script_time,
         script_settings_algorithm_default="fp_labs_runner_hmc_algorithm_default.json",
         script_settings_datasets_default='fp_labs_runner_hmc_datasets_default.json',
         script_settings_algorithm_defined="fp_labs_runner_hmc_algorithm_defined.json",
         script_settings_datasets_defined="fp_labs_runner_hmc_datasets_defined.json"):

    # -------------------------------------------------------------------------------------
    # Variable(s) environment
    folder_home_env = os.path.expanduser('~')
    time_env = script_time.strftime("%Y%m%d_%H")
    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Set environment variables to json settings file(s)
    update_json_file(script_settings_algorithm_default, script_settings_algorithm_defined,
                     update_dict={'$ENV_HOME': folder_home_env, '$ENV_TIME': time_env})

    update_json_file(script_settings_datasets_default, script_settings_datasets_defined,
                     update_dict={'$ENV_HOME': folder_home_env, '$ENV_TIME': time_env})
    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Set logging file
    driver_hmc_logging = ModelLogging(script_settings_algorithm_defined)
    log_stream = driver_hmc_logging.configure_logging()
    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Configure model initializer class
    driver_hmc_initializer = ModelInitializer(file_algorithm=script_settings_algorithm_defined,
                                              file_datasets=script_settings_datasets_defined, time=script_time)

    # Configure algorithm
    time_series_collections, time_info_collections, \
        run_info_collections, run_cline_collections = driver_hmc_initializer.configure_algorithm()

    # Configure ancillary datasets
    ancillary_datasets_collections = driver_hmc_initializer.configure_ancillary_datasets(time_info_collections)
    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Configure model builder class
    driver_hmc_builder = ModelBuilder(
        obj_geo_reference=driver_hmc_initializer.dset_ref_geo,
        obj_args=driver_hmc_initializer.obj_args,
        obj_run=driver_hmc_initializer.obj_run,
        obj_ancillary=driver_hmc_initializer.obj_ancillary)

    # Configure static datasets
    static_datasets_collections = driver_hmc_builder.configure_static_datasets(ancillary_datasets_collections)
    # Configure dynamic datasets
    forcing_datasets_collections = driver_hmc_builder.configure_dynamic_datasets(
        time_series_collections, time_info_collections, static_datasets_collections, ancillary_datasets_collections)
    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Configure model runner class
    driver_hmc_runner = ModelRunner(time_info=time_info_collections, run_info=run_info_collections,
                                    command_line_info=run_cline_collections,
                                    obj_args=driver_hmc_initializer.obj_args,
                                    obj_ancillary=driver_hmc_initializer.obj_ancillary)
    # Configure model execution
    driver_hmc_runner.configure_execution(ancillary_datasets_collections)
    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Configure model finalizer class
    driver_hmc_finalizer = ModelFinalizer(
        collection_dynamic=forcing_datasets_collections,
        obj_geo_reference=driver_hmc_initializer.dset_ref_geo,
        obj_args=driver_hmc_initializer.obj_args,
        obj_run=driver_hmc_initializer.obj_run,
        obj_ancillary=driver_hmc_initializer.obj_ancillary)

    # Configure outcome datasets
    outcome_datasets_collections = driver_hmc_finalizer.configure_dynamic_datasets(
        time_series_collections, time_info_collections, static_datasets_collections, ancillary_datasets_collections)
    # Configure summary datasets
    driver_hmc_finalizer.configure_summary_datasets(
        time_series_collections, time_info_collections, static_datasets_collections, outcome_datasets_collections)
    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Configure model cleaner class
    driver_hmc_cleaner = ModelCleaner(
        collections_ancillary=ancillary_datasets_collections,
        obj_args=driver_hmc_initializer.obj_args,
        obj_run=driver_hmc_initializer.obj_run,
    )
    # Configure cleaning tmp datasets
    driver_hmc_cleaner.configure_cleaner()
    # -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# Call script from external library
if __name__ == "__main__":
    time_run = pd.Timestamp('2021-01-22 06:00')

    file_name_algorithm_default = "fp_labs_runner_hmc_algorithm_default.json"
    file_name_datasets_default = "fp_labs_runner_hmc_datasets_default.json"

    main(time_run, file_name_algorithm_default, file_name_datasets_default)
# ----------------------------------------------------------------------------
