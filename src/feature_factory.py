from features.raw import Raw
from features.altgor import Altgor
from features.nroman import Nroman
from features.magic import Magic
from utils.mylog import timer


class FeatureFactory:

    @timer
    def create(self, featurename):
        if featurename == 'raw':
            return Raw()
        elif featurename == 'altgor':
            return Altgor()
        elif featurename == 'nroman':
            return Nroman()
        elif featurename == 'magic':
            return Magic()
        else:
            raise ValueError(f'Feature {featurename} does not exist in factory menu')
