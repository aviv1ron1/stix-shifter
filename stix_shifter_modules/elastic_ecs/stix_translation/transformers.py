from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer
from stix_shifter_utils.utils import logger

LOGGER = logger.set_logger(__name__)

class EcsRegistryTransformer(ValueTransformer):
    """A value transformer to convert Arcsight Registry root key to windows-registry-key STIX"""

    @staticmethod
    def transform(registry):
        LOGGER.debug("EcsRegistryTransformer", registry)
        stix_root_keys_mapping = {"HKLM": "HKEY_LOCAL_MACHINE", "HKCU": "HKEY_CURRENT_USER",
                                  "HKCR": "HKEY_CLASSES_ROOT", "HKCC": "HKEY_CURRENT_CONFIG",
                                  "HKPD": "HKEY_PERFORMANCE_DATA", "HKU": "HKEY_USERS", "HKDD": "HKEY_DYN_DATA"}
        try:
            splited = registry['path'].split("\\")
            map_root_key = stix_root_keys_mapping[splited[0]]
            splited[0] = map_root_key
            value = splited[-1]
            splited = splited[:-1]
            key = '\\'.join(splited)
            d = {
                "type": "windows-registry-key",
                "key": key,
                "values": []
            }
            if registry['data'] is not None:
                for rd in registry['data']['strings']:
                    d['values'].append({
                            "name": value,
                            "data": rd,
                            "data_type": registry['data']['type']
                        })
            return d
        except ValueError:
            LOGGER.error("Cannot convert root key to Stix formatted windows registry key")
