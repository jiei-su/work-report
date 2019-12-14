# -*- coding: utf-8 -*-
"""
レポートを作成する.
"""
import pandas as pd
import matplotlib.pyplot as plt
import datetime

TODAY = datetime.date.today().strftime('%Y年%m月%d日')
ONTIME = 460


class CreateCommon:
    """
    共通クラス.
    """

    def __init__(self, csv):
        """
        コンストラクタ.

        param:
          csv CSVファイル名
        """
        self.csv = csv

    def actual_worktime(self, time):
        """
        稼働時間を分単位に変換し算出する.

        param:
          time 稼働時間(時間単位)

        return:
          work_time 稼働時間(分単位)
        """
        hour, minute = map(int, time.split(':'))
        work_time = hour*60 + minute

        return work_time

    def delta_worktime(self, time):
        """
        残業時間を算出する.

        param:
          time 稼働時間

        return:
          残業時間
        """
        return round((self.actual_worktime(time) - ONTIME)/60, 1)


class CreateWorkReport(CreateCommon):
    """
    レポート作成.
    """

    def __init__(self, csv):
        """
        コンストラクタ.

        param:
          csv CSVファイル名
        """
        super().__init__(csv)

    def extraction_worktime_from_csv(self):
        """
        年月日、実働時間を抽出する.

        return:
          info 年月日、実働時間のデータ
        """
        df = pd.read_csv(self.csv, encoding='cp932', parse_dates=[1])
        workday = df[df['日付形式(名称)'] == '出勤日']
        info = workday.loc[:, ['年月日', '実働時間']]

        return info

    def preprocessing(self):
        """
        レポート用に整形.

        return:
          work_info 年月日、実働時間、残業時間のDataFrame
          work_sum_info 実働時間(計)、残業時間(計)のDataFrame
        """
        # 来週以降の実働時間は'07:40'として換算
        work_info = self.extraction_worktime_from_csv().fillna('07:40')
        work_info = work_info.set_index('年月日')

        work_info.loc[:, '残業時間'] = \
            work_info.loc[:, '実働時間'].apply(self.delta_worktime)

        worktime_sum = \
            work_info.loc[:, '実働時間'].apply(self.actual_worktime).sum()

        data = [[round(worktime_sum/60, 1), work_info.loc[:, '残業時間'].sum()]]
        index = ['合計']
        columns = ['実働時間', '残業時間']
        work_sum_info = pd.DataFrame(data=data,
                                     index=index,
                                     columns=columns)

        return work_info, work_sum_info

    def create_report(self):
        """
        レポート作成.
        """
        work_info, work_sum_info = self.preprocessing()

        plt.rcParams['font.family'] = 'IPAexGothic'
        fig, ax = plt.subplots(2, 1, figsize=(10, 10), dpi=300)
        fig.suptitle(TODAY, fontsize=16)

        bbox = [0,0,1,1]
        colColours = ['#ffe6b3','#ffe6b3']

        ax[0].axis('off')
        ax[0].table(cellText=work_info.values,
                    bbox=bbox,
                    colLabels=work_info.columns,
                    rowLabels=work_info.index,
                    colColours=colColours)

        ax[1].axis('off')
        ax[1].table(cellText=work_sum_info.values,
                    bbox=bbox,
                    colLabels=work_sum_info.columns,
                    rowLabels=work_sum_info.index,
                    colColours=colColours)

        plt.savefig('./module/report.png')