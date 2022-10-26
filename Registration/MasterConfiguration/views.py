# Create your views here.
from ConfigurationValues import ConfigurationValues
from MasterConfiguration.models import MasterConfigurationModels
import json


class MasterConfiguration:

    def get_master_conf(config_value, product_id):

        try:
            result = MasterConfigurationModels.objects.filter(config_code=config_value,
                                                              config_product_rid=product_id,
                                                              config_valid=1).values()
            return dict(result[0])

        except Exception as err:
            return None

