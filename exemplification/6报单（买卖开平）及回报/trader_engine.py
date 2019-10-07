# -*- coding: utf-8 -*-

from datetime import datetime
from AlgoPlus.CTP.TraderApi import TraderApi
from AlgoPlus.CTP.ApiStruct import *
import time


class TraderEngine(TraderApi):
    def __init__(self, td_server, broker_id, investor_id, password, app_id, auth_code, md_queue=None
                 , page_dir='', private_resume_type=2, public_resume_type=2):
        self.order_ref = 0
        self.Join()

    # 报单
    def insert_order(self, exchange_ID, instrument_id, order_price, order_vol, order_ref, direction, offset_flag):
        pBuyOpen = InputOrderField(
            BrokerID=self.broker_id,
            InvestorID=self.investor_id,
            ExchangeID=exchange_ID,
            InstrumentID=instrument_id,
            UserID=self.investor_id,
            OrderPriceType="2",
            Direction=direction,
            CombOffsetFlag=offset_flag,
            CombHedgeFlag="1",
            LimitPrice=order_price,
            VolumeTotalOriginal=order_vol,
            TimeCondition="3",
            VolumeCondition="1",
            MinVolume=1,
            ContingentCondition="1",
            StopPrice=0,
            ForceCloseReason="0",
            IsAutoSuspend=0,
            OrderRef=str(order_ref),
        )
        l_retVal = self.ReqOrderInsert(pBuyOpen)

    # 买开仓
    def buy_open(self, exchange_ID, instrument_id, order_price, order_vol, order_ref):
        self.insert_order(exchange_ID, instrument_id, order_price, order_vol, order_ref, '0', '0')

    # 卖开仓
    def sell_open(self, exchange_ID, instrument_id, order_price, order_vol, order_ref):
        self.insert_order(exchange_ID, instrument_id, order_price, order_vol, order_ref, '1', '0')

    # 买平仓
    def buy_close(self, exchange_ID, instrument_id, order_price, order_vol, order_ref):
        if exchange_ID == "SHFE" or exchange_ID == "INE":
            self.insert_order(exchange_ID, instrument_id, order_price, order_vol, order_ref, '0', '3')
        else:
            self.insert_order(exchange_ID, instrument_id, order_price, order_vol, order_ref, '0', '1')

    # 卖平仓
    def sell_close(self, exchange_ID, instrument_id, order_price, order_vol, order_ref):
        if exchange_ID == "SHFE" or exchange_ID == "INE":
            self.insert_order(exchange_ID, instrument_id, order_price, order_vol, order_ref, '1', '3')
        else:
            self.insert_order(exchange_ID, instrument_id, order_price, order_vol, order_ref, '1', '1')

    def Join(self):
        while True:
            if self.status == 0:

                # ############################################################################# #
                # 涨停买开仓
                self.order_ref += 1
                self.buy_open(test_exchange_id, test_instrument_id, test_raise_limited, test_vol, self.order_ref)
                self._write_log(f"=>发出涨停买开仓请求！10秒后后进行卖平仓测试。")
                time.sleep(10)

                # 跌停卖平仓
                self.order_ref += 1
                self.sell_close(test_exchange_id, test_instrument_id, test_fall_limited, test_vol, self.order_ref)
                self._write_log(f"=>发出跌停卖平仓请求！10秒后进行卖开仓测试。")
                time.sleep(10)

                # ############################################################################# #
                # 跌停卖开仓
                self.order_ref += 1
                self.sell_open(test_exchange_id, test_instrument_id, test_fall_limited, test_vol, self.order_ref)
                self._write_log(f"=>发出跌停卖平仓请求！10秒后进行买平仓测试。")
                time.sleep(10)

                # 涨停买平仓
                self.order_ref += 1
                self.buy_close(test_exchange_id, test_instrument_id, test_raise_limited, test_vol, self.order_ref)
                self._write_log(f"=>发出涨停买平仓请求！")
                time.sleep(10)

                # ############################################################################# #
                print("老爷，这里的测试工作已经按照您的吩咐全部完成！")
                break

            time.sleep(1)


# ############################################################################# #
# 请在这里填写需要测试的合约数据
# 警告：该例子只支持上期所品种平今仓测试
test_exchange_id = 'SHFE'  # 交易所
test_instrument_id = 'rb2001'  # 合约代码
test_raise_limited = 3704  # 涨停板
test_fall_limited = 3285  # 跌停板
test_vol = 1  # 报单手数

if __name__ == "__main__":
    import sys

    sys.path.append("..")
    from account_info import my_future_account_info_dict

    future_account = my_future_account_info_dict['SimNow24']
    ctp_trader = TraderEngine(future_account.server_dict['TDServer']
                              , future_account.broker_id
                              , future_account.investor_id
                              , future_account.password
                              , future_account.app_id
                              , future_account.auth_code
                              , None
                              , future_account.td_page_dir)
