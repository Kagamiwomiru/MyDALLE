# 画像生成関数
import openai


def runImageGenerate(client, prompt, model_id, size, quality, num_gen):
    '''
    DALLEのAPIを叩いて、画像を生成して払い出されたURLを返す


    Parameters
    ---
    client  :   openai
        openaiオブジェクト

    prompt  :   str
        プロンプト
    model_id    :   str
        model_id
    size    :   str
        生成画像サイズ
    quality :   str
        生成画像の質
    num_gen :   int
        生成枚数

    Return
    ---
    status_code :   int
        0   :   正常
        -1   :   失敗
    image_url   :   str
        画像URL
    '''
    # APIを呼び出して画像を生成
    try:
        response = client.images.generate(
            model=model_id,
            prompt=prompt,
            size=size,
            quality=quality,
            n=num_gen
        )
        return 0, response.data[0].url
    except openai.OpenAIError as e:
        return 1, e