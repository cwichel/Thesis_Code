# -*- coding: utf-8 -*-
# =============================================================================
# Modules
# =============================================================================
import sys
import argparse
from saccadeapp.app import ExperimentHandler


# =============================================================================
# Script
# =============================================================================
def check_args(args=None):
    parser = argparse.ArgumentParser(description=u"Execution Data")
    parser.add_argument(u"-db", u"--database", help=u"Database file path", required=False)
    parser.add_argument(u"-e", u"--experiment", help=u"Experiment code", required=True)
    parser.add_argument(u"-c", u"--configuration", help=u"Configuration profile name", required=True)
    parser.add_argument(u"-f", u"--frames", help=u"Set if the frames will be saved", required=False)
    results = parser.parse_args(args)
    return results.database, results.experiment, results.configuration, results.frames


if __name__ == u"__main__":
    database_path, experiment_code, configuration_name, frame_save = check_args(sys.argv[1:])
    database_path = u"" if database_path is None else database_path
    frame_save = True if frame_save is not None and frame_save == u"True" else False
    handler = ExperimentHandler()
    msg, op_ok = handler.prepare(db_path=database_path, conf_name=configuration_name, exp_code=experiment_code)
    if not op_ok:
        print msg
    else:
        msg, op_ok = handler.execute(frame_save=frame_save)
        print msg
