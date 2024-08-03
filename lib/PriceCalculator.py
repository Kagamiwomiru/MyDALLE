# 消費金額を計算
import yfinance as yf
from lib import ConfigStore
from lib import LanguageKit
import logging


def calcPrice(model_id, size, quality, num_gen):
    '''
    画像生成にかかった金額を日本円で返します。
    REF:https://openai.com/api/pricing/
    '''
    ticker = "USDJPY=X"
    try:
        data = yf.Ticker(ticker).history(period="1d")
        crate = data.Close.iloc[0]
        usd_rate = round(crate, ConfigStore.SIG_DIGS)
        logging.info("[Token Rate]")
        logging.info(f"USD->YEN: {usd_rate}")

        if model_id == "dall-e-3":
            if quality == "standard":
                if size == "1024x1024":
                    return str(0.04 * usd_rate * num_gen)
                elif size == "1024x1792" or size == "1792x1024":
                    return str(0.08 * usd_rate * num_gen)
            elif quality == "hd":
                if size == "1024x1024":
                    return str(0.08 * usd_rate * num_gen)
                elif size == "1024x1792" or size == "1792x1024":
                    return str(0.12 * usd_rate * num_gen)
        elif model_id == "dall-e-2":
            if size == "1024x1024":
                return str(0.02 * usd_rate * num_gen)
            elif size == "512x512":
                return str(0.018 * usd_rate * num_gen)
            elif size == "256x256":
                return str(0.016 * usd_rate * num_gen)
        
        raise NotImplementedError(LanguageKit.CALC_ERROR_TEXT)


    except:
        return LanguageKit.CALC_ERROR_TEXT