import configparser
import os
from dataclasses import dataclass


@dataclass
class ConfigData:
    APP_COLOR: str
    TABLE_BACKGROUND_ITEM_COLOR_R: int
    TABLE_BACKGROUND_ITEM_COLOR_G: int
    TABLE_BACKGROUND_ITEM_COLOR_B: int
    TABLE_ITEM_TEXT_COLOR_R: int
    TABLE_ITEM_TEXT_COLOR_G: int
    TABLE_ITEM_TEXT_COLOR_B: int
    DIRECTORY_PATH: str
    FONT_STYLE: str


def read_config():
    path = "Test-Config.ini"

    config = configparser.ConfigParser()
    config.read(path)
    cfg = ConfigData(
        APP_COLOR=str(config.get('APP_BACKGROUND', 'APP_COLOR')),
        DIRECTORY_PATH=str(config.get('DIRECTORY_PATH', 'DIRECTORY_PATH')),
        FONT_STYLE=str(config.get('FONTS', 'FONT_STYLE')),
        TABLE_BACKGROUND_ITEM_COLOR_R=int(config.get('TABLE_BACKGROUND_COLOR', 'TABLE_BACKGROUND_ITEM_COLOR_R')),
        TABLE_BACKGROUND_ITEM_COLOR_G=int(config.get('TABLE_BACKGROUND_COLOR', 'TABLE_BACKGROUND_ITEM_COLOR_G')),
        TABLE_BACKGROUND_ITEM_COLOR_B=int(config.get('TABLE_BACKGROUND_COLOR', 'TABLE_BACKGROUND_ITEM_COLOR_B')),
        TABLE_ITEM_TEXT_COLOR_R=int(config.get('TEXT_COLOR', 'TABLE_ITEM_TEXT_COLOR_R')),
        TABLE_ITEM_TEXT_COLOR_G=int(config.get('TEXT_COLOR', 'TABLE_ITEM_TEXT_COLOR_G')),
        TABLE_ITEM_TEXT_COLOR_B=int(config.get('TEXT_COLOR', 'TABLE_ITEM_TEXT_COLOR_B'))
    )
    return cfg

