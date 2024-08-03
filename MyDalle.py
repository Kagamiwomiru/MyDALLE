import streamlit as st
import openai
from openai import OpenAI
from lib import LanguageKit 
from lib import ImageGeneration
from lib import ConfigStore
from lib import PriceCalculator
import logging

# ページ設定
st.set_page_config(
    page_title=LanguageKit.APP_TITLE,
    page_icon="😊",
    layout="wide",
    initial_sidebar_state="auto",
)
st.title(LanguageKit.APP_TITLE)


# サイドバー
run_mode = st.sidebar.selectbox(
    LanguageKit.RUN_MODE_LABEL, ConfigStore.RUM_MODES
)

model_id = st.sidebar.selectbox(
    LanguageKit.MODEL_ID_LABEL, ConfigStore.MODELS
)
size = st.sidebar.selectbox(
    LanguageKit.SIZE_LABEL, ConfigStore.SIZES
)
quality = st.sidebar.selectbox(
    LanguageKit.QUALITY_LABEL, ConfigStore.QUALITIES
)
num_gen = st.sidebar.number_input(
    LanguageKit.NUM_GEN_LABEL, ConfigStore.NUM_GEN_MIN, ConfigStore.NUM_GEN_MAX
)


if st.secrets["DEBUG_MODE"] == "True":
    image_url = "http://www.mitsubishielectric.co.jp/news/2014/images/0109.jpg"
    logging.basicConfig(level=logging.INFO)
# 初期化(この中の処理は一回しか実行されません。)
if "messages" not in st.session_state:

	# 辞書形式で定義
    st.session_state["messages"] = []
	# 属性として定義
    # st.session_state.messages = []
    ## for debug
    
    logging.info("debug mode is enabeld.")
    openai.api_key = st.secrets["OPENAI_API_KEY"]


client = OpenAI()

# Streamlit UI


# これまでのチャット履歴を全て表示する
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ユーザーの入力が送信された際に実行される処理
if prompt := st.chat_input(LanguageKit.CHAT_INPUT_HINT_TEXT):
    if not prompt.strip():
        st.error(LanguageKit.NOT_INPUT_ERROR_TEXT)
    else:
        # ユーザの入力を表示する
        with st.chat_message("user"):
            st.markdown(prompt)
        # ユーザの入力をチャット履歴に追加する
        st.session_state.messages.append({"role": "user", "content": prompt})


        # 画像生成を実行
        if st.secrets["DEBUG_MODE"] != "True":
            status_code, image_url = ImageGeneration.runImageGenerate(client, prompt, model_id, size, quality, num_gen)
        logging.info(f"model_id:{model_id}, size:{size}, quality:{quality}, num_gen:{num_gen}")
        if status_code == 0:
            # 生成処理に成功した時
            # 生成結果を表示する
            price = PriceCalculator.calcPrice(model_id, size, quality, num_gen)
            with st.chat_message("assistant"):
                response = f'''![{prompt}]({image_url}) \n
                {LanguageKit.PRICE_TEXT}: {price}{LanguageKit.PRICE_EXTENTION}
                '''
                st.markdown(response)
        else:
            # 生成処理に失敗した時
            # エラーメッセージを表示
            with st.chat_message("assistant"):
                response = f'''{LanguageKit.GEN_ERROR_HEAD_TEXT} \n
                {image_url.message}
                '''
                st.markdown(response)
            
        # DALLEの返答をチャット履歴に追加する
        st.session_state.messages.append({"role": "assistant", "content": response})


