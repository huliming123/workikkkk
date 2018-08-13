import numpy as np
import pandas as pd


def my_sigmoid(x):
    return 1 / (1 + np.exp(-x))

# 打分函数

def my_scale(data):
    if data.mean() == 0:
        return pd.DataFrame(np.zeros(data.shape), columns=data.columns)
    else:
        return (data - data.mean()) / data.mean()

def method_scores(data, *args):
    '''
    :param data: DataFrame格式的数据
    :param num1: 每个行业取出的排名前num数量
    :param args: 元组,布尔类型的值，True表示相应的指标值越大，该指标越好;False表示相应的指标值越小越好。
    :return: 返回每个行业排名在前num1位置的好股票
    '''
    cols = data.columns
    final_data = pd.DataFrame()
    if len(cols) - 3 != len(args[0]):
        print('参数出错，重新输入')
        return
    # 根据行业进行分组
    for c_name, industry_data in data.groupby('c_name'):
        # 对每个行业各个指标，进行按照单个指标进行标准化以及对指标值越小指标越好的指标求负值
        M, num = [], 1
        for my_bool in args[0]:
            num += 1
            if my_bool == True:
                # 每个指标值进行标准化
                M.append(my_scale(industry_data.values[:, num]))
            if my_bool == False:
                M.append(-1 * (my_scale(industry_data.values[:, num])))
        # 最后得到的是标准化以及指标纠正后的numpy.adarray数据
        industry_data_scale = np.array(M).T.astype('f4')
        # 对每个指标值进行打分
        data_score = my_sigmoid(industry_data_scale)
        # 打分之后，修改industry_data的指标的值
        industry_data.values[:, 2:-1] = data_score
        # 做成DataFrame格式的数据
        new_data = pd.DataFrame(industry_data, columns=cols)
        # 计算分数等权重之和，添加新的列，列名为'scores'
        new_data['scores'] = data_score.sum(axis=1) / (len(cols) - 3)
        final_data = pd.concat((final_data, new_data))
    return final_data

class R_Handler():
    def __init__(self,data):
        self.data=data
    def final_score(self, num1, index_dict):
        '''
        :param data: DataFrame格式的数据
        :param num1: 每个行业取出的排名前num1数量
        :param index_dict: 不同维度的指标字典
        :param args: 元组,布尔类型的值，True表示相应的指标值越大，该指标越好;False表示相应的指标值越小越好。
        :return: 返回每个行业排名在前num1位置的好股票
        '''
        columns = self.data.columns
        final_df = pd.DataFrame()
        count = 0
        # 根据不同维度从DataFrame取值
        for key, value in index_dict.items():
            # 选取该维度列名
            cols = self.data.columns[:2].tolist()
            cols.extend(value)
            cols.extend([self.data.columns[-1]])
            tmp_df = self.data.loc[:, cols]
            # 计算该维度得分
            tmp_score = method_scores(tmp_df, [True] * len(value))
            tmp_score.rename(columns={'scores': key}, inplace=True)
            if count == 0:
                final_df = tmp_score.loc[:, [columns[0], key]]
            else:
                final_df = pd.merge(final_df, tmp_score.loc[
                                    :, [columns[0], key]], how='left', on=columns[0])
            count += 1
        # 各维度得分求均值
        final_df = pd.concat((final_df.iloc[:, 0], final_df.iloc[
                             :, 1:].mean(axis=1)), axis=1)
        final_df.rename(columns={0: 'score'}, inplace=True)
        score = pd.merge(self.data, final_df, on=columns[0])

        final_data = pd.DataFrame()
        # 根据行业进行分组，并按照得分排序
        for c_name, industry_data in score.groupby('c_name'):
            new_data = industry_data.sort_values(by='score', ascending=False)
            new_data = new_data.iloc[:num1]
            final_data = pd.concat((final_data, new_data))
        return final_data

    def return_data(self,num1,index_dict):
        data=self.final_score(num1,index_dict)
        cols=data.columns
        final_dict={}
        count=0
        for stock in data.values:
            count+=1
            row_dict={}
            num=-1
            for col in cols:
                num+=1
                row_dict[col]=stock[num]
            final_dict[str(count)]=row_dict
        return final_dict

if __name__ == '__main__':
    # 输入的是DataFrame格式的数据，以及index_dict(如下),以及num=20,就是取多少股票。
    Financial_data = pd.read_excel('Financial_data.xlsx', 'sheet1')
    index_dict = {'偿债能力': ['流动比率', '速动比率'], '营运能力': ['应收账款周转率', '存货周转率', '流动资产周转率'],
                  '盈利能力': ['销售毛利率', '净资产收益率', '总资产净利润'], '成长能力': ['营业收入同比增长率', '净利润同比增长率', '净资产同比增长率'],
                  '现金流量': ['资产的经营现金流量回报率', '经营现金净流量与净利润的比率']}
    a=final_score(Financial_data, 20, index_dict)
