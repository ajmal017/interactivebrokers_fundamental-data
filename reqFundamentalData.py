# TODO: Error handling for connecting, see https://bit.ly/3dkTqj5
# TODO: get fundamental data, see https://bit.ly/3nH5rUF
# import pandas as pd
import time

from ib.ext.EClientSocket import EClientSocket
from IBWrapper import IBWrapper, contract

# from ib.ext.ScannerSubscription import ScannerSubscription
# import re


stocks = [
    '5'
]

for x in stocks:
    callback = IBWrapper()
    tws = EClientSocket(callback)
    host = "127.0.0.1"
    port = 7496
    clientId = 25
    tws.eConnect(host, port, clientId)
    create = contract()
    callback.initiate_variables()
    contract_Details = create.create_contract(x, 'STK', 'SEHK', 'HKD')
    tickerId = 8001

    tws.reqFundamentalData(tickerId,
                           contract_Details,
                           "ReportSnapshot"
                           )
    time.sleep(5)

    print(callback.fundamental_Data_data)
    print(callback.fundamental_Data_data.find("AATCA"))
    print(callback.fundamental_Data_data.find("ACFSHR"))
    print(callback.fundamental_Data_data.find("ADIV5YAVG"))
    print(callback.fundamental_Data_data.find("MKTCAP"))
    print(callback.fundamental_Data_data.find("QTANBVPS"))
    print(callback.fundamental_Data_data.find("REVCHNGYR"))
    print(callback.fundamental_Data_data.find("REVTRENDGR"))
    tws.eDisconnect()
    time.sleep(5)

tws.eDisconnect()
