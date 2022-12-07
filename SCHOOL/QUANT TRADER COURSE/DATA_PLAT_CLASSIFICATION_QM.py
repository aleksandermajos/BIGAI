from ENGINE.DATA_PLAT_CLASSIFICATION_QM import MT4_CSV_TO_CLASSIFICATION
from ENGINE.DATA_PLAT_CLASSIFICATION_QM import MT5_CSV_TO_CLASSIFICATION
from ENGINE.DATA_PLAT_CLASSIFICATION_QM import cTRADER_CSV_TO_CLASSIFICATION
from os import fspath
from pathlib import Path

data_path = Path(Path(__file__).resolve().parent)
data_path_last = fspath(data_path)

data_MT4 = data_path_last+"\\DATA\\QM_MT4_CSV/EURUSD.30.csv"
MT4_CSV_TO_CLASSIFICATION(data_MT4, 16)

data_MT5 = data_path_last+"\\DATA\\QM_MT5_CSV/EURUSD_M30_202001020600_202207181600.csv"
MT5_CSV_TO_CLASSIFICATION(data_MT5,16)

data_cTRADER = data_path_last+"\\DATA\\cTRADER/EURUSD_Candlestick_30_M_BID_01.01.2021-16.07.2022.csv"
cTRADER_CSV_TO_CLASSIFICATION(data_cTRADER,16)
