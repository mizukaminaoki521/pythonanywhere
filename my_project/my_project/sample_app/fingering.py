import pandas as pd

dic_note={}
dic_cost={}
fingering_list={}

throat_note=["G4","G#4","A4","A#4"]

def dijkstra(target_fingering):
    assert(len(target_fingering)>=2)
    #if throat_only
    throat_only_flag=1

    for note in target_fingering:
        if note not in throat_note:
            throat_only_flag=0

    if throat_only_flag==1:
        output_list=[]
        output_list_tmp=[]
        for i in target_fingering:
            output_list_tmp.append(0)
        output_list.append(output_list_tmp)
        return output_list
    else:
        distances={}
        max_cost=100000000
        for i, d in enumerate(target_fingering):
            #print(i,target_fingering[i],target_fingering[i+1],target_fingering[i+2])
            search_note=[]
            if i==0:
                notes1=dic_note[target_fingering[i]]
                notes2=dic_note[target_fingering[i+1]]
                for note1 in notes1:
                    for note2 in notes2:
                        if note1+note2 in dic_cost:
                            search_note.append(note1)
            elif i==len(target_fingering)-1:
                notes1=dic_note[target_fingering[i-1]]
                notes2=dic_note[target_fingering[i]]
                for note1 in notes1:
                    for note2 in notes2:
                        if note1+note2 in dic_cost:
                            search_note.append(note2)
            else:
                notes1=dic_note[target_fingering[i-1]]
                notes2=dic_note[target_fingering[i]]
                notes3=dic_note[target_fingering[i+1]]
                tmp_search_note1=[]
                tmp_search_note2=[]
                for note1 in notes1:
                    for note2 in notes2:
                        if note1+note2 in dic_cost:
                            tmp_search_note1.append(note2)
                for note2 in notes2:
                    for note3 in notes3:
                        if note2+note3 in dic_cost:
                            tmp_search_note2.append(note2)

                search_note = list(set(tmp_search_note1) | set(tmp_search_note2))
            search_note = list(set(search_note))
            #print(search_note)

            distances[i]={}
            #notes=dic_note[d]
            for note in search_note:
                #print(note,target_fingering[i])
                init_cost=max_cost
                init_route=[[]]
                if i ==0:
                    init_cost=0
                    init_route[0].append(note)
                distances[i][f"{note}"]={}
                distances[i][f"{note}"]["cost"]=init_cost
                distances[i][f"{note}"]["route"]=init_route

                if target_fingering[i] in throat_note:
                    distances[i][f"{note}rh"]={}
                    distances[i][f"{note}rh"]["cost"]=init_cost
                    distances[i][f"{note}rh"]["route"]=init_route

        for i in range(1,len(target_fingering)):
            for bkey, bvalue in distances[i-1].items():
                bkey_origin=bkey
                before_rh=0
                if "rh" in bkey:
                    bkey_origin=bkey[:bkey.find("rh")]
                    before_rh=1

                for akey, avalue in distances[i].items():
                    akey_origin=akey
                    after_rh=0
                    if "rh" in akey:
                        akey_origin=akey[:akey.find("rh")]
                        after_rh=1

                    if bkey_origin+akey_origin in dic_cost:
                        tmp_cost=dic_cost[bkey_origin+akey_origin]
                        rh_match=int(dic_cost[bkey_origin+akey_origin+"rh"])
                        #print(bkey,akey,tmp_cost,rh_match)
                        if before_rh==0:
                            if after_rh==1 and rh_match==0:
                                tmp_cost+=10000000
                            elif after_rh==0 and rh_match==1:
                                tmp_cost+=10000000
                            elif bkey_origin[:bkey_origin.find("_")] in throat_note and akey_origin[:akey_origin.find("_")] not in throat_note and rh_match==0:
                                tmp_cost+=10000000
                        if before_rh==1:
                            if after_rh==1 and rh_match==0:
                                assert(0)
                            #elif after_rh==0 and rh_match==0:
                            #    tmp_cost+=10000000

                        if avalue["cost"]>bvalue["cost"]+tmp_cost:
                            avalue["cost"]=bvalue["cost"]+tmp_cost
                            avalue["route"]=[]
                            route=bvalue["route"].copy()

                            for r in route:
                                avalue["route"].append([])
                                tmp_route=r.copy()
                                tmp_route.append(akey)
                                avalue["route"][-1]=tmp_route
                            assert(len(avalue["route"][0])==i+1)
                        elif avalue["cost"]==bvalue["cost"]+tmp_cost:
                            route=bvalue["route"].copy()
                            for r in route:
                                before_length=len(avalue["route"])
                                avalue["route"].append([])
                                tmp_route=r.copy()
                                tmp_route.append(akey)
                                avalue["route"][-1]=tmp_route
                                #print(avalue)
                                assert(before_length==len(avalue["route"])-1)
                                #print(len(avalue["route"][-1]),i+1)
                                assert(len(avalue["route"][-1])==i+1)

    i=len(target_fingering)-1
    min_cost=max_cost
    min_key=[]
    for key, value in distances[i].items():
        if min_cost>value["cost"]:
            min_cost=value["cost"]
            min_key=[]
            min_key.append(key)
        elif min_cost==value["cost"]:
            min_key.append(key)

    output_list=[]
    for key in min_key:
        print(key,distances[i][key]["cost"])
        for paths in distances[i][key]["route"]:
            output_list_tmp=[]
            for path in paths:
                path=path.replace("rh","")
                output_list_tmp.append(int(path.split("_", 1)[1]))
            output_list.append(output_list_tmp)
    return output_list

def cal_cost(target_index,target_fingering,before_note,cost,min_cost,route,min_route):
    #print(target_index,len(target_fingering),target_index==len(target_fingering))
    if target_index==len(target_fingering):
        if min_cost>cost:
            min_route = []
            min_route.append(route.copy())
            min_cost=cost
        elif min_cost==cost:
            min_route.append(route.copy())
        return cost,min_cost,route,min_route
    else:
        #print(target_index)
        notes=dic_note[target_fingering[target_index]]
        for note in notes:
            if before_note=="":
                before_note=note
                route.append(note)
                cost,min_cost,route,min_route=cal_cost(target_index+1,target_fingering,before_note,cost,min_cost,route,min_route)
                before_note=""
                route.pop()
            else:
                save_before_note=before_note
                assert(before_note+note in dic_cost)
                tmp_cost=dic_cost[before_note+note]
                cost+=tmp_cost
                before_note=note
                route.append(note)
                cost,min_cost,route,min_route=cal_cost(target_index+1,target_fingering,before_note,cost,min_cost,route,min_route)
                before_note=save_before_note
                cost-=tmp_cost
                route.pop()
        return cost,min_cost,route,min_route

def get_finger_dic(finger_array):
    assert(len(finger_array)==24)
    finger_dic={}
    for i in ["lh0","lh1","lh2","lh3","lh4","rh1","rh2","rh3","rh4"]:
        finger_dic[i]=[]

    for i, d in enumerate(finger_array):
        if d==1:
            key=""
            hand=""
            if i<=11:
                key=f"L{i}"
            else:
                key=f"R{i-10}"

            if i==0 or i==1:
                hand="lh0"
            elif i==2 or i==5 or i==6:
                hand="lh1"
            elif i==3:
                hand="lh2"
            elif i==4 or i==7:
                hand="lh3"
            elif i==8 or i==9 or i==10 or i==11:
                hand="lh4"
            elif i==12 or i==20 or i==21 or i==22 or i==23:
                hand="rh1"
            elif i==13:
                hand="rh2"
            elif i==14 or i==15:
                hand="rh3"
            elif i==16 or i==17 or i==18 or i==19:
                hand="rh4"

            finger_dic[hand].append(key)
    return finger_dic

def remove_ng_list(fingering_list):
    ng_tone_list=["A#3_1","B3_4","C4_1","C4_2","C#4_1","D4_1","D4_2","D4_3","D#4_7","E4_2","E4_3","E4_4","F4_2","F4_3","F4_4","F4_5","F#4_2","G4_4","G#4_6","A4_6","A#4_4","C5_4","C#5_3","D5_1","D#5_1","F5_2","G5_3","G5_4","G#5_1","G#5_2","A#5_7","B5_3","B5_4","B5_6","C6_2","C6_5","C#6_3","C#6_4","C#6_5","D6_4","D6_5","D#6_3","E6_2","E6_3","E6_4","E6_5","E6_6","F6_4","F6_5","F6_6","F#6_5","F#6_7","G#6_5","B6_1","B6_4","C7_1"]

    tmp_list=[]
    for fingering in fingering_list:
        if fingering not in ng_tone_list:
            tmp_list.append(fingering)
    fingering_list=tmp_list
    return fingering_list

def get_sharp_note(note,number):
    if note=="Db":
        return "C#"+number
    elif note=="Eb":
        return "D#"+number
    elif note=="Gb":
        return "F#"+number
    elif note=="Ab":
        return "G#"+number
    elif note=="Bb":
        return "A#"+number
    elif note=="Cb":
        return "B"+str(int(number)-1)
    elif note=="B#":
        return "C"+str(int(number)+1)
    elif note=="Fb":
        return "E"+number
    elif note=="E#":
        return "F"+number
    return note+number

def make_fingering_cost_csv():
    df=pd.read_csv("CL_Finger_mod.txt",header=None)

    dict_fingering = df.set_index(0).T.to_dict('list')
    fingering_list=remove_ng_list(df[0].to_list())
    #df.columns=["0","L0","L1","L2","L3","L4","L5","L6","L7","L8","L9","L10","L11","R2","R3","R4","R5","R6","R7","R8","R9","R10","R11","R12","R13"]
    #df=df[(df["L5"]==1) & (df["L6"]==1)]

    #使えない運指を除く
    tone_range = list(set(item.split('_')[0] for item in fingering_list))

    #初期化
    for tone in tone_range:
        dic_note[tone]=[]

    for tone in fingering_list:
        tone_key=tone.split('_')[0]
        dic_note[tone_key].append(tone)

    for i in range(len(fingering_list)):
        before_tone=fingering_list[i]
        before_finger_dic=get_finger_dic(dict_fingering[before_tone])
        #print(before_tone,before_finger_dic)

    #コスト計算
    for i in range(len(fingering_list)):
        for j in range(len(fingering_list)):
            before_tone=fingering_list[i]
            after_tone=fingering_list[j]

            before_finger_dic=get_finger_dic(dict_fingering[before_tone])
            after_finger_dic=get_finger_dic(dict_fingering[after_tone])

            #スロート音域を含むかどうか
            throat_note_flag=0
            rh_match=1
            if before_tone[:before_tone.find("_")] in throat_note or after_tone[:after_tone.find("_")] in throat_note:
                throat_note_flag=1
                #右手が完全一致するかどうか調べる
                for rh in ["rh1","rh2","rh3","rh4"]:
                    if before_finger_dic[rh]!=after_finger_dic[rh]:
                        rh_match=0

            #if throat_note_flag==0 or (throat_note_flag==1 and rh_match==1):
            if True:
                cost=0

                right_off=0
                right_on=0
                left_off=0
                left_on=0
                """
                flag=0
                if before_tone=="A#3_0" and after_tone=="B3_0":
                    print(before_finger_dic)
                    print(after_finger_dic)
                    flag=1
                """
                CORRECTION_VALUE=100

                for key, value in before_finger_dic.items():#各指毎にcostを計算し足し合わせる
                    Correction_value=CORRECTION_VALUE
                    if key=="lh3" or key=="rh3":
                        Correction_value=1.3*CORRECTION_VALUE
                    elif key=="lh4" or key=="rh4":
                        Correction_value=1.5*CORRECTION_VALUE
                    hand=key[:2]

                    if len(before_finger_dic[key])==0 and len(after_finger_dic[key])==0:#何もなし
                        cost+=0
                    elif len(before_finger_dic[key])>0 and len(after_finger_dic[key])==0:#離す
                        cost+=0
                        if hand=="lh":
                            left_off+=1
                        if hand=="rh":
                            right_off+=1
                    elif len(before_finger_dic[key])==0 and len(after_finger_dic[key])>0:#新たに抑える
                        cost+=1*Correction_value
                        if hand=="lh":
                            left_on+=1
                        if hand=="rh":
                            right_on+=1
                    elif value==after_finger_dic[key]:#抑え続ける
                        assert(len(before_finger_dic[key])>0 and len(after_finger_dic[key])>0)
                        cost+=0
                        if key=="lh3" or key=="rh3" or key=="lh4" or key=="rh4":
                            cost+=0.5*Correction_value
                    elif set(value).issubset(after_finger_dic[key]):#抑える箇所を増やす
                        cost+=2*Correction_value
                        if hand=="lh":
                            left_on+=1
                        if hand=="rh":
                            right_on+=1
                    elif set(after_finger_dic[key]).issubset(value):#抑えた箇所を減らす
                        cost+=2*Correction_value
                        if hand=="lh":
                            left_off+=1
                        if hand=="rh":
                            right_off+=1
                    else:#その他 例えば抑えた指を離して別のキーにを抑える
                        cost+=5*Correction_value
                        if hand=="lh":
                            left_off+=1
                            left_on+=1
                        if hand=="rh":
                            right_off+=1
                            right_on+=1

                if right_on==0 and left_on==0 and right_off==0 and left_off==0:#何も変わらない
                    cost+=0*CORRECTION_VALUE
                elif ((right_on==0)+(left_on==0)+(right_off==0)+(left_off==0))==3:#一つの手の押しor離すだけ
                    cost+=0*CORRECTION_VALUE
                elif (right_on==0 and left_on==0) or (right_off==0 and left_off==0):#2つの手の押しor離すだけ
                    cost+=0*CORRECTION_VALUE
                elif (right_on==0 and right_off==0) or (left_on==0 and left_off==0):#1つの手の押しかつ離す
                    cost+=2*CORRECTION_VALUE
                elif (right_on==0 and left_off==0) or (left_on==0 and right_off==0):#2つの手で押しと離すがバラバラ
                    cost+=3*CORRECTION_VALUE
                else:
                    cost+=5*CORRECTION_VALUE

                if before_tone[before_tone.find("_")+1:]=="0" and after_tone[after_tone.find("_")+1:]=="0":
                    cost=max(cost-1.5*CORRECTION_VALUE,0)

                dic_cost[before_tone+after_tone]=cost

    with open("fingering_cost.csv", 'w') as file:
        for key in sorted(dic_cost.keys()):
            print(key,dic_cost[key],file=file)

    #return tone_range

def check_fingering_and_cost(dict_fingering,target_fingering,answer):
    for i, tone in enumerate(target_fingering):
        finger_dic=get_finger_dic(dict_fingering[tone+"_"+str(answer[i])])
        print(tone+"_"+str(answer[i]),finger_dic)

    for i in range(1,len(target_fingering)):
        before=target_fingering[i-1]+"_"+str(answer[i-1])
        after=target_fingering[i]+"_"+str(answer[i])
        if target_fingering[i-1] in throat_note or target_fingering[i] in throat_note:
            cost=0
        else:
            cost=dic_cost[before+after]
        print(before,after,cost)
    return

def test():

    test_list=[
                ["F#3","C4","F4"],
                ["G3","A#3","D#4"],
                ["G3", "C4", "D#4"],
                ["G#3", "C4", "D#4"],
                ["G#3", "B3", "E4"],
                ["G#3", "C4", "D#4"],
                ["G#3", "C#4", "F4"],
                ["G3", "A#3", "D#4"],
                ["G#3", "C4", "D#4"],
                ["G#3", "C#4", "F4"],
                ["G#3", "C4" ,"F4"],
                ["A#3", "C#4", "F#4"],
                ["F#3", "A#3", "C#4"],
                ["F3", "G#3", "C#4"],
                ["F#5","B5","F#5","C#5","G#4","B4","G#5","C#5"],
                ["A#4","A4"],
                ["G4","B4","D5","E5","D5","B4","G4","A#4","C#5","D#5","C#5","A#4","G4","C#5","B4","C#5","B4"],
                ["C4","D#4","G#4","C5","C5","D#4","A#4","D#5","C5","A#4","G#4","F4","G#4","C#5","F5","F5","G#4","D#5","G#5","F5","D#5","C#5"],
                ["E4","D#4","A4","G#4","G4"],
                ["D#4","D4","E4","A#3","B3","C4","B3"],
                ["D#4","D4","G#4","A4","A#3","B3","F4","E4","D#5","D5"],

                #scale
                ["C4","D4","E4","F4","G4","A4","B4","C5","D5","E5","F5","G5","A5","B5","C6","D6","E6","F6","G6"],
                ["G6","F6","E6","D6","C6","B5","A5","G5","F5","E5","D5","C5","B4","A4","G4","F4","E4","D4","C4","B3","A3","G3","F3","E3","F3","G3","A3","B3","C4","D4","C4"],
                ["G3","A3","B3","C4","D4","E4","F#4","G4","A4","B4","C5","D5","E5","F#5","G5","A5","B5","C6","D6","E6","F#6","G6"],
                ["G6","F#6","E6","D6","C6","B5","A5","G5","F#5","E5","D5","C5","B4","A4","G4","F#4","E4","D4","C4","B3","A3","G3","F#3","E3","F#3","G3","A3","G3"],
                ["G3","A3","B3","C4","D4","E4","F#4","G4","A4","B4","C5","D5","E5","F#5","G5","A5","B5","C6","D6","E6","F#6","G6"],
                ["G6","F#6","E6","D6","C6","B6","A6","G5","F#5","E5","D5","C5","B4","A4","G4","F#4","E4","D4","C4","B3","A3","G3","F#3","E3","F#3","G3","A3","G3"],
                ["D4","E4","F#4","G4","A4","B4","C#5","D5","E5","F#5","G5","A5","B5","C#6","D6","E6","F#6","G6"],
                ["G6","F#6","E6","D6","C6","B5","A5","G5","F#5","E5","D5","C#5","B4","A4","G4","F#4","E4","D4","C#4","B3","A3","G3","F#3","E3","F#3","G3","A3","B3","C#4","D4","E4","D4"],
                ["A3","B3","C4","D4","E4","F#4","G#4","A4","B4","C#5","D5","E5","F#5","G#5","A5","B5","C#6","D6","E6","F#6","G#6","A6"],
                ["A6","G#6","F#6","E6","D6","C6","B5","A5","G#5","F#5","E5","D5","C#5","B4","A4","G#4","F#4","E4","D4","C#4","B3","A3","G#3","F#3","E3","F#3","G#3","A3"],
                ["E3","F#3","G#3","A3","B3","C4","D#4","E4","F#4","G#4","A4","B4","C#5","D#5","E5","F#5","G#5","A5","B5","C#6","D#6","E6","F#6","G#6"],
                ["G#6","F#6","E6","D#6","C6","B5","A5","G#5","F#5","E5","D#5","C#5","B4","A4","G#4","F#4","E4","D#4","C#4","B3","A3","G#3","F#3","E3","F#3","E3"],
                ["B3","C4","D#4","E4","F#4","G#4","A#4","B4","C#5","D#5","E5","F#5","G#5","A#5","B5","C#6","D#6","E6","F#6","G#6"],
                ["G#6","F#6","E6","D#6","C6","B5","A#5","G#5","F#5","E5","D#5","C#5","B4","A#4","G#4","F#4","E4","D#4","C#4","B3","A#3","G#3","F#3","E3","F#3","G#3","A#3","B3","C#4","B3"],
                ["F#3","G#3","A#3","B3","C4","D#4","F4","F#4","G#4","A#4","B4","C#5","D#5","F5","F#5","G#5","A#5","B5","C#6","D#6","F6","F#6","G#6"],
                ["G#6","F#6","F6","D#6","C6","B5","A#5","G#5","F#5","F5","D#5","C#5","B4","A#4","G#4","F#4","F4","D#4","C#4","B3","A#3","G#3","F#3","F3","F#3","G#3","A#3"],
                ["Db4","Eb4","F4","Gb4","Ab4","Bb4","C5","Db5","Eb5","F5","Gb5","Ab5","Bb5","C6","Db6","Eb6","F6","Gb6","Ab6"],
                ["Ab6","Gb6","F6","Eb6","Db6","C6","Bb5","Ab5","Gb5","F5","Eb5","Db5","C5","Bb4","Ab4","Gb4","F4","Eb4","Db4","C4","Bb3","Ab3","Gb3","F3","Gb3","Ab3","Bb3","C4","Db4","Eb4","Db4"],
                ["Ab3","Bb3","C4","Db4","Eb4","F4","G4","Ab4","Bb4","C5","Db5","Eb5","F5","G5","Ab5","Bb5","C6","Db6","Eb6","F6","G6","Ab6"],
                ["Ab6","G6","F6","Eb6","Db6","C6","Bb5","Ab5","G5","F5","Eb5","Db5","C5","Bb4","Ab4","G4","F4","Eb4","Db4","C4","Bb3","Ab3","G3","F3","Gb3","Ab3","Bb3","Ab3"],
                ["Eb4","F4","G4","Ab4","Bb4","C5","D5","Eb5","F5","G5","Ab5","Bb5","C6","D6","Eb6","F6","G6","Ab6"],
                ["Ab6","G6","F6","Eb6","D6","C6","Bb5","Ab5","G5","F5","Eb5","D5","C5","Bb4","Ab4","G4","F4","Eb4","D4","C4","Bb3","Ab3","G3","F3","Gb3","Ab3","Bb3","C4","D4","Eb4","F4","Eb4"],
                ["Bb3","C4","Eb4","F4","G4","A4","Bb4","C5","D5","Eb5","F5","G5","A5","Bb5","C6","D6","Eb6","F6","G6","A6"],
                ["A6","G6","F6","Eb6","D6","C6","Bb5","A5","G5","F5","Eb5","D5","C5","Bb4","A4","G4","F4","Eb4","D4","C4","Bb3","A3","G3","F3","Gb3","A3","Bb3","C4","Bb3"],
                ["F3","G3","A3","Bb3","C4","E4","F4","G4","A4","Bb4","C5","D5","Eb5","F5","G5","A5","Bb5","C6","D6","E6","F6","G6","A6"],
                ["A6","G6","F6","E6","D6","C6","Bb5","A5","G5","F5","E5","D5","C5","Bb4","A4","G4","F4","E4","D4","C4","Bb3","A3","G3","F3","E3","F3"],

                ["E3","F3","E3","F3","E3"],
                ["E3","F#3","E3","F#3","E3"],
                ["E3","G3","E3","G3","E3"],
                ["E3","G#3","E3","G#3","E3"],
                ["E3","A3","E3","A3","E3"],
                ["E3","A#3","E3","A#3","E3"],
                ["E3","B3","E3","B3","E3"],
                ["E3","C4","E3","C4","E3"],
                ["E3","C#4","E3","C#4","E3"],
                ["E3","D4","E3","D4","E3"],
                ["E3","D#4","E3","D#4","E3"],
                ["E3","E4","E3","E4","E3"],

                ["F3","F#3","F3","F#3","F3"],
                ["F3","G3","F3","G3","F3"],
                ["F3","G#3","F3","G#3","F3"],
                ["F3","A3","F3","A3","F3"],
                ["F3","A#3","F3","A#3","F3"],
                ["F3","B3","F3","B3","F3"],
                ["F3","C4","F3","C4","F3"],
                ["F3","C#4","F3","C#4","F3"],
                ["F3","D4","F3","D4","F3"],
                ["F3","D#4","F3","D#4","F3"],
                ["F3","E4","F3","E4","F3"],
                ["F3","F4","F3","F4","F3"],

                ["F#3","G3","F#3","G3","F#3"],
                ["F#3","G#3","F#3","G#3","F#3"],
                ["F#3","A3","F#3","A3","F#3"],
                ["F#3","A#3","F#3","A#3","F#3"],
                ["F#3","B3","F#3","B3","F#3"],
                ["F#3","C4","F#3","C4","F#3"],
                ["F#3","C#4","F#3","C#4","F#3"],
                ["F#3","D4","F#3","D4","F#3"],
                ["F#3","D#4","F#3","D#4","F#3"],
                ["F#3","E4","F#3","E4","F#3"],
                ["F#3","F4","F#3","F4","F#3"],
                ["F#3","F#4","F#3","F#4","F#3"],

                ["G3","G#3","G3","G#3","G3"],
                ["G3","A3","G3","A3","G3"],
                ["G3","A#3","G3","A#3","G3"],
                ["G3","B3","G3","B3","G3"],
                ["G3","C4","G3","C4","G3"],
                ["G3","C#4","G3","C#4","G3"],
                ["G3","D4","G3","D4","G3"],
                ["G3","D#4","G3","D#4","G3"],
                ["G3","E4","G3","E4","G3"],
                ["G3","F4","G3","F4","G3"],
                ["G3","F#4","G3","F#4","G3"],
                ["G3","G4","G3","G4","G3"],

                ["G#3","A3","G#3","A3","G#3"],
                ["G#3","A#3","G#3","A#3","G#3"],
                ["G#3","B3","G#3","B3","G#3"],
                ["G#3","C4","G#3","C4","G#3"],
                ["G#3","C#4","G#3","C#4","G#3"],
                ["G#3","D4","G#3","D4","G#3"],
                ["G#3","D#4","G#3","D#4","G#3"],
                ["G#3","E4","G#3","E4","G#3"],
                ["G#3","F4","G#3","F4","G#3"],
                ["G#3","F#4","G#3","F#4","G#3"],
                ["G#3","G4","G#3","G4","G#3"],
                ["G#3","G#4","G#3","G#4","G#3"],

                ["A3","A#3","A3","A#3","A3"],
                ["A3","B3","A3","B3","A3"],
                ["A3","C4","A3","C4","A3"],
                ["A3","C#4","A3","C#4","A3"],
                ["A3","D4","A3","D4","A3"],
                ["A3","D#4","A3","D#4","A3"],
                ["A3","E4","A3","E4","A3"],
                ["A3","F4","A3","F4","A3"],
                ["A3","F#4","A3","F#4","A3"],
                ["A3","G4","A3","G4","A3"],
                ["A3","G#4","A3","G#4","A3"],
                ["A3","A4","A3","A4","A3"],

                ["A#3","B3","A#3","B3","A#3"],
                ["A#3","C4","A#3","C4","A#3"],
                ["A#3","C#4","A#3","C#4","A#3"],
                ["A#3","D4","A#3","D4","A#3"],
                ["A#3","D#4","A#3","D#4","A#3"],
                ["A#3","E4","A#3","E4","A#3"],
                ["A#3","F4","A#3","F4","A#3"],
                ["A#3","F#4","A#3","F#4","A#3"],
                ["A#3","G4","A#3","G4","A#3"],
                ["A#3","G#4","A#3","G#4","A#3"],
                ["A#3","A4","A#3","A4","A#3"],
                ["A#3","A#4","A#3","A#4","A#3"],

                ["B3","C4","B3","C4","B3"],
                ["B3","C#4","B3","C#4","B3"],
                ["B3","D4","B3","D4","B3"],
                ["B3","D#4","B3","D#4","B3"],
                ["B3","E4","B3","E4","B3"],
                ["B3","F4","B3","F4","B3"],
                ["B3","F#4","B3","F#4","B3"],
                ["B3","G4","B3","G4","B3"],
                ["B3","G#4","B3","G#4","B3"],
                ["B3","A4","B3","A4","B3"],
                ["B3","A#4","B3","A#4","B3"],
                ["B3","B4","B3","B4","B3"],

                ["C4","C#4","C4","C#4","C4"],
                ["C4","D4","C4","D4","C4"],
                ["C4","D#4","C4","D#4","C4"],
                ["C4","E4","C4","E4","C4"],
                ["C4","F4","C4","F4","C4"],
                ["C4","F#4","C4","F#4","C4"],
                ["C4","G4","C4","G4","C4"],
                ["C4","G#4","C4","G#4","C4"],
                ["C4","A4","C4","A4","C4"],
                ["C4","A#4","C4","A#4","C4"],
                ["C4","B4","C4","B4","C4"],
                ["C4","C5","C4","C5","C4"],

                ["C#4","D4","C#4","D4","C#4"],
                ["C#4","D#4","C#4","D#4","C#4"],
                ["C#4","E4","C#4","E4","C#4"],
                ["C#4","F4","C#4","F4","C#4"],
                ["C#4","F#4","C#4","F#4","C#4"],
                ["C#4","G4","C#4","G4","C#4"],
                ["C#4","G#4","C#4","G#4","C#4"],
                ["C#4","A4","C#4","A4","C#4"],
                ["C#4","A#4","C#4","A#4","C#4"],
                ["C#4","B4","C#4","B4","C#4"],
                ["C#4","C5","C#4","C5","C#4"],
                ["C#4","C#5","C#4","C#5","C#4"],

                ["D4","D#4","D4","D#4","D4"],
                ["D4","E4","D4","E4","D4"],
                ["D4","F4","D4","F4","D4"],
                ["D4","F#4","D4","F#4","D4"],
                ["D4","G4","D4","G4","D4"],
                ["D4","G#4","D4","G#4","D4"],
                ["D4","A4","D4","A4","D4"],
                ["D4","A#4","D4","A#4","D4"],
                ["D4","B4","D4","B4","D4"],
                ["D4","C5","D4","C5","D4"],
                ["D4","C#5","D4","C#5","D4"],
                ["D4","D5","D4","D5","D4"],

                ["D#4","E4","D#4","E4","D#4"],
                ["D#4","F4","D#4","F4","D#4"],
                ["D#4","F#4","D#4","F#4","D#4"],
                ["D#4","G4","D#4","G4","D#4"],
                ["D#4","G#4","D#4","G#4","D#4"],
                ["D#4","A4","D#4","A4","D#4"],
                ["D#4","A#4","D#4","A#4","D#4"],
                ["D#4","B4","D#4","B4","D#4"],
                ["D#4","C5","D#4","C5","D#4"],
                ["D#4","C#5","D#4","C#5","D#4"],
                ["D#4","D5","D#4","D5","D#4"],
                ["D#4","D#5","D#4","D#5","D#4"],

                ["E4","F4","E4","F4","E4"],
                ["E4","F#4","E4","F#4","E4"],
                ["E4","G4","E4","G4","E4"],
                ["E4","G#4","E4","G#4","E4"],
                ["E4","A4","E4","A4","E4"],
                ["E4","A#4","E4","A#4","E4"],
                ["E4","B4","E4","B4","E4"],
                ["E4","C5","E4","C5","E4"],
                ["E4","C#5","E4","C#5","E4"],
                ["E4","D5","E4","D5","E4"],
                ["E4","D#5","E4","D#5","E4"],
                ["E4","E5","E4","E5","E4"],

                ["F4","F#4","F4","F#4","F4"],
                ["F4","G4","F4","G4","F4"],
                ["F4","G#4","F4","G#4","F4"],
                ["F4","A4","F4","A4","F4"],
                ["F4","A#4","F4","A#4","F4"],
                ["F4","B4","F4","B4","F4"],
                ["F4","C5","F4","C5","F4"],
                ["F4","C#5","F4","C#5","F4"],
                ["F4","D5","F4","D5","F4"],
                ["F4","D#5","F4","D#5","F4"],
                ["F4","E5","F4","E5","F4"],
                ["F4","F5","F4","F5","F4"]
                ]

    answer=[
        [[0, 0, 0]],
        [[0, 0, 2]],
        [[0, 0, 1]],
        [[0, 0, 1]],
        [[0, 0, 0]],
        [[0, 0, 1]],
        [[0, 0, 0]],
        [[0, 0, 2]],
        [[0, 0, 1]],
        [[0, 0, 0]],
        [[0, 0, 0]],
        [[0, 0, 0]],
        [[0, 0 ,0]],
        [[1, 0, 0]],
        [[1,0,1,1,0,1,0,1]],
        [[0,0]],

        [[0,0,0,0,0,0,0,0,4,0,4,0,0,1,5,1,5]],
        [[0,1,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,4]],
        [[0,0,0,0,0]],
        [[0,0,0,0,1,0,0]],
        [[0,0,0,0,0,1,0,0,0,0]],

        #scale
        [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
        [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
        [[0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0]],
        [[0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,1,0,0,0]],
        [[0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0]],
        [[0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,1,0,0,0]],
        [[0,0,0,0,0,5,1,0,0,1,0,0,0,0,0,0,0,0]],
        [[0,0,0,0,0,0,0,0,1,0,0,1,5,0,0,0,0,0,0,0,0,0,1,2,1,0,0,0,0,0,0,0]],
        [[0,0,0,0,0,0,0,0,5,1,0,0,1,0,0,0,0,0,0,0,1,0]],
        [[0,1,0,0,0,0,0,0,0,1,0,0,1,5,0,0,0,0,0,0,0,0,0,2,2,2,0,0]],
        [[2,2,0,0,0,0,1,0,0,0,0,1,4,0,0,1,0,0,0,0,2,0,0,0]],
        [[0,0,0,2,0,0,0,0,0,0,0,4,1,0,0,0,0,1,0,0,0,0,2,2,2,2]],
        [[0,0,1,0,0,0,0,1,4,0,0,1,0,1,0,0,2,0,0,0]],
        [[0,0,0,2,0,0,1,0,1,0,0,4,1,0,0,0,0,1,0,0,0,0,2,2,2,0,0,0,0,0]],
        [[2,0,0,1,0,1,0,0,0,0,1,4,0,0,0,0,1,0,0,2,0,0,0]],
        [[0,0,0,2,0,0,1,0,0,0,0,4,1,0,0,0,0,1,0,2,0,0,2,0,2,0,0]],
        [[0,1,0,0,0,0,0,4,0,0,0,0,1,0,0,2,0,0,0]],
        [[0,0,0,2,0,0,1,0,0,0,0,4,0,0,0,0,0,1,0,0,0,0,2,0,2,0,0,0,0,1,0]],
        [[0,0,0,0,1,0,0,0,0,0,4,0,0,0,0,1,0,0,0,2,0,0]],
        [[0,0,2,0,0,0,1,0,0,0,0,4,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0]],
        [[0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0]],
        [[0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
        [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
        [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
        [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
        [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],

        #E3
        [[0,0,0,0,0]],
        [[2,1,2,1,2]],
        [[1,0,1,0,1],[0, 0, 0, 0, 0]],
        [[2,0,2,0,2]],
        [[2,0,2,0,2],[0, 0, 0, 0, 0]],
        [[2,0,2,0,2],[0, 0, 0, 0, 0]],
        [[2,0,2,0,2],[0, 0, 0, 0, 0]],
        [[2,0,2,0,2],[0, 0, 0, 0, 0]],
        [[1,0,1,0,1]],
        [[2,0,2,0,2]],
        [[1,2,1,2,1],[2, 3, 2, 3, 2]],
        [[2,0,2,0,2]],
        #F3
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[1,0,1,0,1]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,2,0,2,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        #F#3
        [[1,0,1,0,1],[0, 0, 0, 0, 0]],
        [[2,0,2,0,2]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[1,0,1,0,1]],
        [[0,0,0,0,0]],
        [[0,2,0,2,0],[1, 2, 1, 2, 1]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        #G3
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,2,0,2,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        #G#3
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,2,0,2,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        #A3
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,2,0,2,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        #A#3
        [[0,1,0,1,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,2,0,2,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        #B3
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,9,0,9,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        #C4
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,1,0,1,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        #C#4
        [[0,4,0,4,0],[0, 0, 0, 0, 0]],
        [[0,1,0,1,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,1,0,1,0]],
        [[0,0,0,0,0]],
        [[0,1,0,1,0]],
        #D4
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        #D#4
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[1,0,1,0,1]],
        [[1,0,1,0,1]],
        [[1,0,1,0,1],[3, 5, 3, 5, 2]],
        [[1,0,1,0,1],[2, 0, 2, 0, 2]],
        [[1,0,1,0,1],[4, 2, 4, 2, 4]],
        [[1,0,1,0,1],[2, 0, 2, 0, 2]],
        [[1,0,1,0,1],[2, 0, 2, 0, 2]],
        #E4
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0],[0, 3, 0, 3, 0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        #F4
        [[0,1,0,1,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0],[0, 3, 0, 3, 0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        [[0,0,0,0,0]],
        ]

    df=pd.read_csv("CL_Finger_mod.txt",header=None)
    dict_fingering = df.set_index(0).T.to_dict('list')

    num=0
    correct=0

    for index,target_fingering in enumerate(test_list):

        sharp_target_fingering=[]
        #print(target_fingering)

        for note in target_fingering:
            #print(note[:-1],note[-1])
            assert(note[-1]=="3" or note[-1]=="4" or note[-1]=="5" or note[-1]=="6")
            assert(note[0]=="A" or note[0]=="B" or note[0]=="C" or note[0]=="D" or note[0]=="E" or note[0]=="F" or note[0]=="G")

            sharp_note=get_sharp_note(note[:-1],note[-1])
            sharp_target_fingering.append(sharp_note)

        assert(len(target_fingering)==len(answer[index][0]))

        output_list=dijkstra(sharp_target_fingering)

        is_included=False
        for answer_index in range(len(answer[index])):
            for output in output_list:
                tmp_is_included=True
                for i in range(len(output)):
                    if sharp_target_fingering[i] in throat_note:
                        continue
                    elif output[i] != answer[index][answer_index][i]:
                        tmp_is_included=False
                if tmp_is_included==True:
                    is_included=True

        num+=1

        if is_included==False:
            print(target_fingering)
            print(sharp_target_fingering)
            print(answer[index])

            for answer_index in range(len(answer[index])):
                for aaa in range(len(target_fingering)):
                    if sharp_target_fingering[aaa]+"_"+str(answer[index][answer_index][aaa]) not in dict_fingering:
                        print("not found ",sharp_target_fingering[aaa]+"_"+str(answer[index][answer_index][aaa]))
                check_fingering_and_cost(dict_fingering,sharp_target_fingering,answer[index][answer_index])

            #print(output_list)
            for output_list_tmp in output_list:
                print(output_list_tmp)
                check_fingering_and_cost(dict_fingering,sharp_target_fingering,output_list_tmp)
            print("=====")
        else:
            correct+=1
    print(num,correct,correct/num)

def get_all_list():
    left_list=[
    [1,0,0,0,0,1,0,0,0,0,0,0],
    [1,0,0,0,1,1,0,0,0,0,0,1],
    [1,0,0,1,1,1,0,0,0,0,0,0],
    [0,0,0,0,0,1,0,0,0,0,0,0],
    [0,1,1,1,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,1,0,0,0,0,0,0]
    ]

    right_list=[
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,0,0,1,1],
    [0,0,0,0,0,0,0,0,0,1,0,0],
    [0,0,0,0,0,0,0,0,1,0,0,0],
    [0,0,0,0,0,0,0,0,1,1,0,0],
    [0,0,0,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,1,0,0,0,0,0,0,0],
    [0,0,0,0,1,0,0,0,0,0,0,1],
    [0,0,0,0,1,0,0,0,0,1,0,0],
    [0,0,0,0,1,0,0,0,1,1,0,0],
    [0,0,0,1,0,0,0,0,0,0,0,0],
    [0,0,0,1,0,0,0,0,0,1,0,0],
    [0,0,0,1,1,0,0,0,0,0,0,0],
    [0,0,0,1,1,0,0,0,0,0,0,1],
    [0,0,1,0,0,0,0,0,0,0,0,0],
    [0,0,1,0,0,0,1,0,0,0,0,0],
    [0,0,1,0,1,0,0,0,0,0,0,0],
    [0,0,1,0,1,0,0,0,0,0,1,1],
    [0,0,1,0,1,0,0,0,1,1,0,0],
    [0,0,1,1,1,0,0,0,0,0,0,0],
    [0,1,0,0,0,0,0,0,0,0,0,0],
    [0,1,0,0,0,0,0,0,0,0,0,1],
    [0,1,0,0,1,0,0,0,0,0,0,0],
    [0,1,1,0,0,0,0,0,0,0,0,0],
    [0,1,1,0,0,0,0,0,1,1,0,0],
    [0,1,1,0,0,0,0,1,0,0,0,0],
    [0,1,1,0,0,0,0,1,0,0,1,1],
    [0,1,1,0,0,0,1,0,0,0,0,0],
    [0,1,1,0,0,1,0,0,0,0,0,0],
    [0,1,1,0,0,1,0,0,0,1,0,0],
    [0,1,1,0,1,0,0,0,0,0,0,0],
    [0,1,1,0,1,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,1,0,0,0,0,0],
    [1,0,0,0,1,0,0,0,0,0,0,0],
    [1,0,0,1,0,0,0,0,0,0,0,0],
    [1,0,0,1,1,0,0,0,0,0,0,0],
    [1,0,1,0,0,0,0,0,0,0,0,0],
    [1,0,1,0,0,0,1,0,0,0,0,0],
    [1,0,1,0,0,1,0,0,0,0,0,0],
    [1,0,1,0,1,0,0,0,0,0,0,0],
    [1,1,0,0,0,0,0,0,0,0,0,0],
    [1,1,0,0,0,0,0,1,0,0,0,0],
    [1,1,0,0,1,0,0,0,0,0,0,0],
    [1,1,0,0,1,0,0,0,0,0,1,1],
    [1,1,0,1,0,0,0,0,0,0,0,0],
    [1,1,1,0,0,0,0,0,0,0,0,0],
    [1,1,1,0,0,0,0,0,0,1,0,0],
    [1,1,1,0,0,0,0,1,0,0,0,0],
    [1,1,1,0,0,0,0,1,0,0,0,1],
    [1,1,1,0,0,0,1,0,0,0,0,0],
    [1,1,1,0,0,1,0,0,0,0,0,0],
    [1,1,1,0,0,1,0,0,1,1,0,0],
    [1,1,1,0,1,0,0,0,0,0,0,0],
    [1,1,1,1,0,0,0,0,0,0,0,0],
    [1,1,1,1,1,0,0,0,0,0,0,0],]

    index=0
    for l in left_list:
        for r in right_list:
            print(f"A#4_{index},"+','.join(map(str, l+r)))
            index+=1

def load_fingering_cost():
    df=pd.read_csv("sample_app/fingering_cost.csv",header=None,sep=" ")
    dic_cost = df.set_index(0)[1].to_dict()

    df=pd.read_csv("sample_app/CL_Finger_mod.txt",header=None)
    dict_fingering = df.set_index(0).T.to_dict('list')

    fingering_list=remove_ng_list(df[0].to_list())
    tone_range = list(set(item.split('_')[0] for item in fingering_list))

    for tone in tone_range:
        dic_note[tone]=[]

    for tone in fingering_list:
        tone_key=tone.split('_')[0]
        dic_note[tone_key].append(tone)

    return dic_cost,dic_note,tone_range


def start(target_fingering):
    dic_cost,dic_note,tone_range=load_fingering_cost()
    return dijkstra(target_fingering)
