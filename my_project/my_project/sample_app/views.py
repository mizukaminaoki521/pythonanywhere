from django.shortcuts import render, get_object_or_404, redirect
from django.forms import ModelForm

from sample_app.models import Post
from .utils import dic_cost,dic_note,tone_range

import ast
import pandas as pd

fingering_list={}

throat_note=["G4","G#4","A4","A#4"]


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
        #print(key,distances[i][key]["cost"])
        for paths in distances[i][key]["route"]:
            output_list_tmp=[]
            for path in paths:
                path=path.replace("rh","")
                output_list_tmp.append(int(path.split("_", 1)[1]))
            output_list.append(output_list_tmp)
    output_list = list(map(list, set(map(tuple, output_list))))
    return output_list


def create_post(request):
    """
    新たなデータを作成する
    """
    # オブジェクトを新規作成する
    post = Post()
    # ページロード時
    if request.method == 'GET':
        # 新規作成オブジェクトにより form を作成
        form = PostForm(instance=post)
        # ページロード時は form を Template に渡す
        return render(request,
                      'sample_app/post_form.html',  # 呼び出す Template
                      {'form': form})  # Template に渡すデータ

    # 実行ボタン押下時
    if request.method == 'POST':
        # POST されたデータにより form を作成
        form = PostForm(request.POST, instance=post)

        # 入力されたデータのバリデーション
        if form.is_valid():
            # チェック結果に問題なければデータを作成する
            post = form.save(commit=False)

            delete_chars = "\"'[ ]:;()=-^&%$!@*`<>./"
            origin_text=post.name
            post.name = origin_text.translate(str.maketrans("", "", delete_chars))
            target_list=post.name.split(',')

            sharp_target_fingering=[]
            #print(target_fingering)

            for note in target_list:
                #print(note[:-1],note[-1])
                assert(note[-1]=="3" or note[-1]=="4" or note[-1]=="5" or note[-1]=="6")
                assert(note[0]=="A" or note[0]=="B" or note[0]=="C" or note[0]=="D" or note[0]=="E" or note[0]=="F" or note[0]=="G")

                sharp_note=get_sharp_note(note[:-1],note[-1])
                sharp_target_fingering.append(sharp_note)
            output_list=dijkstra(sharp_target_fingering)
            post.micropost=output_list

            post.save()

        return redirect('sample_app:read_post')


def read_post(request):
    """
    データの一覧を表示する
    """
    # 全オブジェクトを取得
    #posts = Post.objects.all().order_by('id')
    posts = Post.objects.all().order_by('-id').first()
    target_list=posts.name.split(',')
    index_list = ast.literal_eval(posts.micropost)
    sharp_target_fingering=[]

    for note in target_list:
        #print(note[:-1],note[-1])
        assert(note[-1]=="3" or note[-1]=="4" or note[-1]=="5" or note[-1]=="6")
        assert(note[0]=="A" or note[0]=="B" or note[0]=="C" or note[0]=="D" or note[0]=="E" or note[0]=="F" or note[0]=="G")

        sharp_note=get_sharp_note(note[:-1],note[-1])
        sharp_target_fingering.append(sharp_note)

    df=pd.read_csv("/home/MizukamiNaoki/mysite/pythonanywhere/my_project/my_project/sample_app/CL_Finger_mod.txt",header=None)
    dict_fingering = df.set_index(0).T.to_dict('list')

    output = {"name":posts.name,"target":[]}

    for j in range(len(index_list)):
        kouho_dic={"tone_index":[],"hole_list":[]}

        melody_list=[]
        for i, d in enumerate(sharp_target_fingering):
            tone_index=sharp_target_fingering[i]+"_"+str(index_list[j][i])
            tone_hole=[]
            for k, v in enumerate(dict_fingering[tone_index]):
                CO="O"
                if v==1:
                    CO="C"
                if k<=11:
                    CO="L"+str(k)+CO
                else:
                    CO="R"+str(k-10)+CO
                tone_hole.append(CO)
            assert(len(tone_hole)==24)
            melody_list.append(tone_hole)
            kouho_dic["tone_index"].append(target_list[i]+"_"+str(index_list[j][i]))
            kouho_dic["hole_list"].append(tone_hole)

        assert(len(melody_list)==len(sharp_target_fingering))

        output["target"].append(kouho_dic)
        #print(output)

    return render(request,
                  'sample_app/post_list.html',  # 呼び出す Template
                  {'posts': output}
                  )  # Template に渡すデータ


def edit_post(request, post_id):
    """
    対象のデータを編集する
    """
    # IDを引数に、対象オブジェクトを取得
    post = get_object_or_404(Post, pk=post_id)

    # ページロード時
    if request.method == 'GET':
        # 対象オブジェクトにより form を作成
        form = PostForm(instance=post)

        # ページロード時は form とデータIDを Template に渡す
        return render(request,
                      'sample_app/post_form.html',  # 呼び出す Template
                      {'form': form, 'post_id': post_id})  # Template に渡すデータ

    # 実行ボタン押下時
    elif request.method == 'POST':
        # POST されたデータにより form を作成
        form = PostForm(request.POST, instance=post)

        # 入力されたデータのバリデーション
        if form.is_valid():
            # チェック結果に問題なければデータを更新する
            post = form.save(commit=False)
            post.save()

        # 実行ボタン押下時は処理実行後、一覧画面にリダイレクトする
        return redirect('sample_app:read_post')


def delete_post(request, post_id):
    # 対象のオブジェクトを取得
    post = get_object_or_404(Post, pk=post_id)
    post.delete()

    # 削除リクエスト時は削除実行後、一覧表示画面へリダイレクトする
    return redirect('sample_app:read_post')


class PostForm(ModelForm):
    """
    フォーム定義
    """
    class Meta:
        model = Post
        # fields は models.py で定義している変数名
        fields = {'name', 'micropost'}
        #fields = {'name'}