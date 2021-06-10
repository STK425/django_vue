import paddlehub as ph

senta = ph.Module(name="senta_bilstm")

def get_emotion(list, emo_list):
    dic = {'positive' : emo_list[0], 'neutral': emo_list[1], 'negative' : emo_list[2]}
    input_dict = {"text": list}
    results = senta.sentiment_classify(data = input_dict)
    for index, result in enumerate(results):
        if result['positive_probs'] < 0.65 and result['positive_probs'] >= 0.35:
            dic['neutral'] += 1
        else:
            dic[result['sentiment_key']] += 1

    res = []
    for item in dic.values():
        res.append(item)

    return res
