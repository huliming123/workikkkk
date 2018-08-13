from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpResponse,JsonResponse
# Create your views here.
from .datadeal import  Data_Deal
from .method_sub import *
import json
@api_view(['GET','POST'])
def index_views(request):
    if request.method=='GET':
        return HttpResponse('you are a good boy')
    if request.method=='POST':
        # 获取数据
        data_json=request.body
        data_decode=data_json.decode()
        # 将数据转换为dict格式
        final_data=json.loads(data_decode)
        # 对获取的数据进行转换为method_sub需要的参数格式,data(DataFrame格式的),num(取每个行业前10),index_dict(各模块具体指标)
        a = Data_Deal(final_data)
        data, num, index_dict = a.data_deal()
        print(data.values)
        print(index_dict)
        print(type(index_dict))
        # 将上一步传入的参数返回给模型，让模型进行计算
        b= R_Handler(data)
        final__dict=b.return_data(num,index_dict)
        return JsonResponse(final__dict)
