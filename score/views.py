from django.shortcuts import render

# Create your views here.
from django.views.generic import (
    FormView,
    )
from .models import Score
from .forms import UploadForm
from django.http import HttpResponse

import csv
import os
import pandas as pd
import numpy as np

class ScoreListView(FormView):
    model = Score
    template_name = "score/home.html" #後でtemplateを作成
    context_object_name = 'scores'
    ordering = ['-date'] #最新投稿を頭にする
    form_class = UploadForm

    def form_valid(self, form):
    #csvをインポート
        SCORE_ROOT = os.path.dirname(os.path.abspath(__file__))
        target = os.path.join(SCORE_ROOT, 'models/')

    #スコアcsvをオープン
        csvfile = open(target + 'total.csv', 'r')
        reader = csv.reader(csvfile)
        csv_data = [row for row in reader]

    #Location csvをオープン
        location_file = open(target + 'location_all.csv', 'r')
        reader = csv.reader(location_file)
        location_data = [row for row in reader]

    #Stations csvをオープン
        station_file = open(target + 'stations.csv', 'r')
        reader = csv.reader(station_file)
        station_data = [row for row in reader]


    #複数選択した項目をリスト化
        items = []
        for item in form.cleaned_data['choice']:
            items.append(item)

        items = items

    #駅名を拾う。
        name = form.cleaned_data['name']
        name_sub = form.cleaned_data['name_sub']

    #主駅の各項目(items)の点数(scores)を拾う。
        scores = []
        for i in range(len(items)):
            for data in csv_data:
                if data[1] == form.cleaned_data['name'] and data[3] == items[i]:
                    score = data[0]
                    scores.append(score)
                    
        scores = scores
        #項目の合計点を計算
        inter_sum = [float(s) for s in scores]
        sum_scores = sum(inter_sum)

    #651駅をリストに入れる。
        stations = []
        for data in csv_data[1:651]:
            stations.append(data[1])

        stations = stations

    #比較駅の各項目(items)の点数(scores)を拾う。
        scores_sub = []
        for i in range(len(items)):
            for data in csv_data:
                if data[1] == form.cleaned_data['name_sub'] and data[3] == items[i]:
                    score = data[0]
                    scores_sub.append(score)
                    
        scores_sub = scores_sub
        #項目の合計点を計算
        inter_sum = [float(s) for s in scores_sub]
        sum_scores_sub = sum(inter_sum)

    #各項目(items)の平均値(averages)を拾う。
        averages = []
        for i in range(len(items)):
            total = 0
            for data in csv_data:
                if data[3] == items[i]:
                    total += float(data[0])
            total = round(total/650, 0)
            averages.append(total)

        averages = averages
        #項目の合計点nを計算
        sum_averages = sum(averages)
    
    #zippledリストを作成しておく。
        zipped = zip(items, scores, scores_sub, averages)

    #各項目の上位15駅とその点数を拾う。
        top_cities = []
        top_scores = []
    
        for i in range(len(items)):
            n = 0
            inter_cities = []
            inter_scores = []
            top_cities.append(inter_cities)
            top_scores.append(inter_scores)
            for data in csv_data:
                if data[3] == items[i]:
                    if n <= 14:
                        top_city = data[1]
                        top_score = float(data[0])
                        inter_cities.append(top_city)
                        inter_scores.append(top_score)
                        n+=1

        top_cities = top_cities
        top_scores = top_scores

    #各項目の下位15駅とその点数を拾う。
        bottom_cities = []
        bottom_scores = []

        for i in range(len(items)):
            n = 0
            inter_cities = []
            inter_scores = []
            bottom_cities.append(inter_cities)
            bottom_scores.append(inter_scores)

            #[::-1]とすることで、逆からループを回す。
            for data in csv_data[::-1]:
                 if data[3] == items[i]:
                     if n <= 14:
                        city = data[1]
                        score = float(data[0])
                        inter_cities.append(city)
                        inter_scores.append(score)
                        n+=1


    #上位15駅、下位15駅を拾って、一つにまとめる。
        total_cities = []
        total_scores = []

        for i in range(len(items)):
            total_city = top_cities[i] + list(reversed(bottom_cities[i]))  
            #↑下位駅は順番を逆にしてから入れる。
            total_score = top_scores[i] + sorted(bottom_scores[i], reverse=True)
            #↑下位駅は点数を高い順から入れる。
            total_cities.append(total_city)
            total_scores.append(total_score)

        total_cities = total_cities
        total_scores = total_scores


    #総合点：駅ごとの各項目(items)合計値を計算
        select_item_scores = []

        for i in range(len(items)):
            each_score = []
            select_item_scores.append(each_score)
            for x in stations:
                for data in csv_data:
                    if items[i] == data[3] and x == data[1]:
                        each_score.append(float(data[0]))

    #総合点：each_scoreの2次元リストを列ごとに合計
        select_item_scores = [sum(column) for column in zip(*select_item_scores)]
        
    #総合点：駅とスコアを合体。
        scores_and_stations= []

        for n in range(len(stations)):
            station = stations[n]
            select_item_score = select_item_scores[n]
            scores_and_stations.append((select_item_score,station)) 

        #高い順のリストと低い順のリスト２つ作成する。
        scores_top_ranking = sorted(scores_and_stations, reverse=True)
        scores_bottom_ranking = sorted(scores_and_stations)

        #その駅の総合点における順位を拾う
        station_only = []
        for i in scores_top_ranking:
            station_only.append(i[1])

        ranking = station_only.index(name) + 1 
        ranking_sub = station_only.index(name_sub) + 1

    
    #ロケーションを地図上にプロット
        location_name = []
        location_address = []
        location_latitude = []
        location_longitude = []
        location_category = []

        for i in range(len(items)):
            for data in location_data[1:]:
                if data[4] == items[i]:
                    a = data[0]
                    b = data[1]
                    c = data[2]
                    d = data[3]
                    e = data[4]
                    location_name.append(a)
                    location_address.append(b)
                    location_latitude.append(c)
                    location_longitude.append(d)
                    location_category.append(e)
        
        location_zipped = zip(location_name, location_address, location_latitude,location_longitude,location_category)

    #洗濯した駅のロケーションを拾う。
        station_1_lat = []
        station_1_lng = []
        station_2_lat = []
        station_2_lng = []

        for data in station_data[1:]:
            if data[0] == name:
                x = data[1]
                y = data[2]
                station_1_lat.append(x)
                station_1_lng.append(y)
            elif data[0] == name_sub:
                x = data[1]
                y = data[2]
                station_2_lat.append(x)
                station_2_lng.append(y)

        station_1 = zip(station_1_lat, station_1_lng)
        station_2 = zip(station_2_lat, station_2_lng)


    #選択した駅が各項目において何位なのかを拾う。
        ranking_each_items = []
    
        #駅名を拾う
        for i in range(len(items)):
            cities = []
            ranking_each_items.append(cities)
            for data in csv_data:
                if data[3] == items[i]:
                    city = data[1] 
                    cities.append(city)

        #すでに駅名は点数順に並んでいるので、indexで何番目か取得する。
        ranking_by_items = []
        ranking_by_items_sub = []
        for i in range(len(items)):
            x = ranking_each_items[i].index(name) + 1
            y = ranking_each_items[i].index(name_sub) + 1
            ranking_by_items.append(x)
            ranking_by_items_sub.append(y)

        ranking_zipped = zip(ranking_by_items, ranking_by_items_sub)

    #結果をブラウザに表示させたいときはこちら
        return self.render_to_response(self.get_context_data(
            scores=scores, 
            scores_sub=scores_sub,
            sum_scores=sum_scores,
            sum_scores_sub=sum_scores_sub,
            items=items, 
            name=name,
            name_sub=name_sub, 
            stations=stations,
            zipped=zipped,
            
            station_1=station_1,
            station_2=station_2,
            location_zipped=location_zipped,

            ranking_zipped=ranking_zipped,

            averages=averages,
            sum_averages=sum_averages,

            total_cities=total_cities,
            total_scores=total_scores,

            scores_and_stations=scores_and_stations,
            scores_top_ranking=scores_top_ranking,
            scores_bottom_ranking=scores_bottom_ranking,

            ranking=ranking,
            ranking_sub=ranking_sub,
            
            ))