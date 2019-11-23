import gc
import warnings
from datetime import datetime
warnings.filterwarnings('ignore')
import traceback
import pathlib
from src.utils import seeder
from logging import getLogger

from configure import Config
from mylog import timer, create_logger
from experiment import Experiment


@timer
def main(config):
    experiment = Experiment(config)
    experiment.run()


if __name__ == "__main__":
    c = Config()
    c.set_parameter(config_dir=pathlib.Path('src/config'), use_option=True)
    gc.enable()
    seeder.seed_everything(c.runtime.RANDOM_SEED)
    create_logger('main', c.log)
    create_logger('train', c.log)
    logger = getLogger('main')
    logger.info(f':thinking_face: ============ {datetime.now():%Y-%m-%d %H:%M:%S} ============ :thinking_face:')
    try:
        main(c)
        logger.info(f':sunglasses: ============ {datetime.now():%Y-%m-%d %H:%M:%S} ============ :sunglasses:')
    except Exception:
        logger.critical(f':smiling_imp: Exception occured \n {traceback.format_exc()}')
        logger.critical(f':skull: ============ {datetime.now():%Y-%m-%d %H:%M:%S} ============ :skull:')
