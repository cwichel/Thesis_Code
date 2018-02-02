import os
import codecs
import time
import yaml
from saccadeApp import SaccadeDB, Master, Experiment


def generate_experiment_files(db, mas, exp):
    if isinstance(db, SaccadeDB):
        mas_data = Master()
        mas_data.set_database(db=db)
        mas_check = mas_data.load(name=mas)

        exp_data = Experiment()
        exp_data.set_database(db=db)
        exp_check = exp_data.load(code=exp)

        if mas_check and exp_check:
            timestamp = unicode(int(time.time()))
            mas_conf = mas_data.get_iohub(unixstamp=timestamp)
            exp_conf = exp_data.get_iohub(unixstamp=timestamp)
            exp_log = exp_data.get_configuration(unixstamp=timestamp)

            with codecs.open('out.yaml', mode="w", encoding="utf-8") as outfile:
                yaml.dump(exp_log, outfile, default_flow_style=False)

            print u'Hola'
        else:
            print u'Nara'

        return None
    else:
        return None

