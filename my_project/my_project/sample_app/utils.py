import pandas as pd

dic_cost={}
dic_note={}
tone_range=[]

def remove_ng_list(fingering_list):
    ng_tone_list=["A#3_1","B3_4","C4_1","C4_2","C#4_1","D4_1","D4_2","D4_3","E4_2","E4_3","E4_4","F4_2","F4_3","F4_4","F4_5","F#4_2","G4_4","G#4_6","A4_6","A#4_4","C5_4","C#5_3","D5_1","D#5_1","F5_2","G5_3","G5_4","G#5_1","G#5_2","A#5_7","B5_3","B5_4","B5_6","C6_5","C#6_5","D6_4","D#6_3","E6_3","E6_4","E6_5","E6_6","F6_4","F6_5","F6_6","F#6_5","F#6_7"]
    tmp_list=[]
    for fingering in fingering_list:
        if fingering not in ng_tone_list:
            tmp_list.append(fingering)
    fingering_list=tmp_list
    return fingering_list

def load_fingering_cost():
    global dic_cost
    global dic_note
    global tone_range

    df=pd.read_csv("/home/MizukamiNaoki/mysite/pythonanywhere/my_project/my_project/sample_app/fingering_cost.csv",header=None,sep=" ")
    dic_cost = df.set_index(0)[1].to_dict()
    df=pd.read_csv("/home/MizukamiNaoki/mysite/pythonanywhere/my_project/my_project/sample_app/CL_Finger_mod.txt",header=None)
    dict_fingering = df.set_index(0).T.to_dict('list')

    fingering_list=remove_ng_list(df[0].to_list())
    tone_range = list(set(item.split('_')[0] for item in fingering_list))

    for tone in tone_range:
        dic_note[tone]=[]

    for tone in fingering_list:
        tone_key=tone.split('_')[0]
        dic_note[tone_key].append(tone)
    return

