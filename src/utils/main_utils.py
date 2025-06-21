import sys
import logging
import json
from src.exception import NerException


# initiatlizing logger
logger = logging.getLogger(__name__)


class MainUtils:

    def read_json_file(self, json_data_path:str) -> dict:
        try:
            logger.info("Entered the read_json_file method of Main utils class")

            with open(json_data_path) as fp:
                data = json.load(fp)

            logger.info("Exited the read_json_file method of Main utils class")
            return data
        except Exception as e:
            raise NerException(e, sys) from e