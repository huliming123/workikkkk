import numpy as np
import pandas as pd
'''
json_data={"tar1":[1,23,4,3,2,45],"tar2":[12,354,43,324],"num":10,"parti_target":{'偿债能力': ['流动比率', '速动比率'], '营运能力': ['应收账款周转率', '存货周转率', '流动资产周转率'],
                  '盈利能力': ['销售毛利率', '净资产收益率', '总资产净利润'], '成长能力': ['营业收入同比增长率', '净利润同比增长率', '净资产同比增长率'],
                  '现金流量': ['资产的经营现金流量回报率', '经营现金净流量与净利润的比率']}}
'''
class Data_Deal():
    '''
    该类主要是用于对接收到的json数据进行数据处理，从而得到DataFrame格式的数据以及num,和上市公司的每个模块的具体指标。
    '''
    def __init__(self,data):
        self.data=data
    def data_deal(self):
        cols=list(self.data)[:-2]
        M=[]
        for key in list(self.data):
            if key=='num':
                num=self.data[key]
            if key=="parti_target":
                index_dict=self.data[key]
            if key!='num' and key!='parti_target':
                M.append(self.data[key])
        data=np.array(M).T
        data_pd=pd.DataFrame(data[:,:2],columns=cols[:2])
        count=1
        for col in cols[2:-1]:
            count+=1
            data_pd[col]=data[:,count].reshape(-1,1).astype('f4')
        data_pd[cols[-1]]=data[:,-1].reshape(-1,1)
        return data_pd,int(num),index_dict

if __name__=='__main__':
    data=json_data={"tar1":[1,23,4,3],"tar2":[12,354,43,324],"num":10,"parti_target":{'偿债能力': ['流动比率', '速动比率'], '营运能力': ['应收账款周转率', '存货周转率', '流动资产周转率'],
                  '盈利能力': ['销售毛利率', '净资产收益率', '总资产净利润'], '成长能力': ['营业收入同比增长率', '净利润同比增长率', '净资产同比增长率'],
                  '现金流量': ['资产的经营现金流量回报率', '经营现金净流量与净利润的比率']}}
    a=Data_Deal(data)
    data,num,index_dict=a.data_deal()
    print(data)
    print(num)
    print(index_dict)
