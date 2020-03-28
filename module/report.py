"""
レポートを作成する.
"""
import os
import glob
import datetime
import pandas as pd
import matplotlib.pyplot as plt

TODAY = datetime.date.today().strftime('%Y年%m月%d日')
ONTIME = 460


class CreateCommon:
    """
    共通クラス.
    """

    def actual_worktime(self, time):
        """
        稼働時間を分単位に変換する.

        @param:
            time 稼働時間(時間単位)
        @return:
            work_time 稼働時間(分単位)
        """
        hour, minute = map(int, time.split(':'))
        work_time = hour*60 + minute

        return work_time

    def delta_worktime(self, time):
        """
        残業時間を算出する.

        @param:
            time 稼働時間
        @return:
            残業時間
        """
        return round((self.actual_worktime(time) - ONTIME)/60, 1)


class CreateWorkReport(CreateCommon):
    """
    レポート作成クラス.
    """

    def __init__(self):
        """
        コンストラクタ.
        """
        self.csv_path = ''.join(glob.glob('**/*.csv', recursive=True))

    def extraction_worktime(self, data_frame):
        """
        年月日、実働時間を抽出する.

        @param:
            data_frame DataFrame形式の勤務情報
        @return:
            info 年月日、実働時間
        """
        workday = data_frame[data_frame['日付形式(名称)'] == '出勤日']
        info = workday.loc[:, ['年月日', '実働時間']]

        return info

    def preprocessing(self, data_frame):
        """
        レポート用に整形する.

        @param:
            data_frame DataFrame形式の勤務情報
        @return:
            work_info 年月日、実働時間、残業時間のDataFrame
            work_sum_info 実働時間(計)、残業時間(計)のDataFrame
        """
        # 次週以降の実働時間は'07:40'として換算
        work_info = self.extraction_worktime(data_frame).fillna('07:40')
        work_info = work_info.set_index('年月日')

        work_info.loc[:, '残業時間'] = \
            work_info.loc[:, '実働時間'].apply(super().delta_worktime)

        worktime_sum = \
            work_info.loc[:, '実働時間'].apply(super().actual_worktime).sum()

        data = [[round(worktime_sum/60, 1), work_info.loc[:, '残業時間'].sum()]]
        work_sum_info = pd.DataFrame(data=data, index=['合計'],
                                     columns=['実働時間', '残業時間'])

        return work_info, work_sum_info

    def create(self):
        """
        レポートを作成する.

        @return:
            True 作成成功
        @raise:
            'CSVが見つかりませんでした'
        """
        if self.csv_path:
            data_frame = pd.read_csv(self.csv_path, encoding='cp932', parse_dates=[1])
            work_info, work_sum_info = self.preprocessing(data_frame)

            plt.rcParams['font.family'] = 'IPAexGothic'
            fig, axs = plt.subplots(2, 1, figsize=(10, 10), dpi=300)
            fig.suptitle(TODAY, fontsize=16)

            bbox = [0, 0, 1, 1]
            col_colours = ['#ffe6b3', '#ffe6b3']

            axs[0].axis('off')
            axs[0].table(cellText=work_info.values,
                         bbox=bbox,
                         colLabels=work_info.columns,
                         rowLabels=work_info.index,
                         colColours=col_colours)

            axs[1].axis('off')
            axs[1].table(cellText=work_sum_info.values,
                         bbox=bbox,
                         colLabels=work_sum_info.columns,
                         rowLabels=work_sum_info.index,
                         colColours=col_colours)

            plt.savefig('./module/report.png')
            os.remove(self.csv_path)
            return True

        return 'CSVが見つかりませんでした'
