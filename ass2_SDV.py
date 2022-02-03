import sys
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
import seaborn as sns
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QPushButton, QTabWidget,\
    QVBoxLayout, QHBoxLayout, QSizePolicy, QTabBar, QLabel, QMainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from tab_map import MapWindow


class Container(QWidget):
    def __init__(self, text):
        super(Container, self).__init__()

        self.hbox = QHBoxLayout()
        self.hbox.setSpacing(0)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.hbox)

        self.button = QPushButton(text)
        self.hbox.addWidget(self.button)


class CustomWidget(QWidget):
    def __init__(self, parent=None):
        super(CustomWidget, self).__init__(parent)
        self.setWindowTitle("DATAWIZ - Data Visualization Application")
        self.setWindowIcon(QtGui.QIcon('icons/DW_icon.png'))
        self.tabs = QTabWidget()
        self.tabs.setTabBar(TabBar())
        self.tabs.setTabsClosable(False)
        self.tabs.setMovable(False)
        self.tabs.setDocumentMode(True)
        self.tabs.setElideMode(Qt.ElideRight)
        self.tabs.setUsesScrollButtons(True)

        self.tabs.addTab(HomeWin(), "HOME")
        self.tabs.addTab(MainDash(), "DASHBOARD")
        self.tabs.addTab(MapWindow(), "MAP")

        vbox = QVBoxLayout()
        # vbox.addWidget(self.button)
        vbox.addWidget(self.tabs)
        self.setLayout(vbox)

        self.resize(1800, 900)


class TabBar(QTabBar):
    def tabSizeHint(self, index):
        size = QTabBar.tabSizeHint(self, index)
        w = int(self.width()/self.count())
        return QSize(w, size.height())


class HomeWin(QMainWindow):
    def __init__(self):
        super(HomeWin, self).__init__()
        label = QLabel(self)
        pixmap = QPixmap('icons/DW_Home.png')
        label.setPixmap(pixmap)
        self.setCentralWidget(label)
        self.resize(pixmap.width(), pixmap.height())


class MainDash(QDialog):
    def __init__(self, parent=None):
        super(MainDash, self).__init__(parent)
        self.resize(1000, 900)
        self.figure = matplotlib.figure.Figure()
        self.canvas = FigureCanvas(self.figure)

        self.toolbar = NavigationToolbar(self.canvas, self)

        self.button1 = QPushButton('1')
        self.button2 = QPushButton('2')
        self.button1.clicked.connect(self.plot_m)
        self.button2.clicked.connect(self.plot_o)

        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()

        hlayout.addWidget(self.button1)
        hlayout.addWidget(self.button2)

        vlayout.addWidget(self.toolbar)
        vlayout.addWidget(self.canvas)
        vlayout.addLayout(hlayout)

        # setting layout to the main window
        self.setLayout(vlayout)

        # import data (excel)
        excelfile = r'C:\Users\User\sampleTutorial\data\AllData.xlsx'
        self.population = pd.read_excel(excelfile, sheet_name='Population')
        self.death = pd.read_excel(excelfile, sheet_name='Death')
        self.death_rate_state = pd.read_excel(excelfile, sheet_name='Death Rate State')
        self.death_rate_gender = pd.read_excel(excelfile, sheet_name='Death Rate Gender')
        self.death_ethnic = pd.read_excel(excelfile, sheet_name='Death Ethnic')
        self.df_immune = pd.read_excel(excelfile, sheet_name='Propotional of infant Immused')
        self.i_mortality = pd.read_excel(excelfile, sheet_name='Infant Mortality')
        self.m_mortality = pd.read_excel(excelfile, sheet_name='Maternal Mortality')
        self.life_e = pd.read_excel(excelfile, sheet_name='Life Expectacy')
        self.refuse_vaccine = pd.read_excel(excelfile, sheet_name='Vaccine-refusal')

    def plot_m(self):
        self.figure.clf()
        ax1 = self.figure.add_subplot(231)
        pop_state = self.population.groupby(['State']).sum()
        pop_state = pop_state.sort_values(by='per 1000', ascending=True)
        pop_state = pd.DataFrame(pop_state.to_records())
        sumPop_state = pop_state['per 1000']
        state = pop_state['State']
        ax1.barh(state, sumPop_state, color='green')
        ax1.set_title('Population')

        ax2 = self.figure.add_subplot(234)
        death_state = self.death_rate_state.sort_values(by='Death rate', ascending=True)
        state_ = death_state['State']
        d_by_state = death_state['Death rate']
        ax2.barh(state_, d_by_state, color='red')
        ax2.set_title('Death')

        ax5 = self.figure.add_subplot(232)
        pop_ethnic = self.population.groupby(['Ethnic Group']).sum()
        pop_ethnic = pd.DataFrame(pop_ethnic.to_records())
        sumPop_ethnic = pop_ethnic['per 1000']
        ethnic = pop_ethnic['Ethnic Group']
        ax5.bar(ethnic, sumPop_ethnic, color='green')
        ax5.set_title('Ethnics')

        ax6 = self.figure.add_subplot(235)
        death_ethnic = self.death_ethnic.groupby(['Ethnic Group']).sum()
        death_ethnic = pd.DataFrame(death_ethnic.to_records())
        sumDeath_ethnic = death_ethnic['Rate']
        ethnic = death_ethnic['Ethnic Group']
        ax6.bar(ethnic, sumDeath_ethnic, color='red')
        ax6.set_title('Ethnics')

        ax7 = self.figure.add_subplot(233)
        gender_population = self.population.groupby(["Sex"]).sum()
        sumPop_gender = gender_population["per 1000"]
        color = sns.color_palette('dark:g')[2:12]
        ax7.pie(sumPop_gender, labels=sumPop_gender.index, autopct='%1.2f%%', shadow=True, colors=color)
        ax7.axis('equal')
        ax7.set_title('Gender')

        ax8 = self.figure.add_subplot(236)
        death_g = self.death_rate_gender['Death rate']
        gg = self.death_rate_gender['Sex']
        color = sns.color_palette('dark:r')[2:12]
        ax8.pie(death_g, labels=gg, autopct='%1.2f%%', shadow=True, colors=color)
        ax8.axis('equal')
        ax8.set_title('Gender')

        self.canvas.draw_idle()

    def plot_o(self):
        self.figure.clf()

        ax3 = self.figure.add_subplot(231)
        sum_i_rate = self.i_mortality.groupby(['State']).sum()
        sum_i_rate = sum_i_rate.sort_values(by='Rate', ascending=True)
        sum_i_rate = pd.DataFrame(sum_i_rate.to_records())
        # print(sum_i_rate)
        i_state = sum_i_rate['State']
        i_rate = sum_i_rate['Rate']
        ax3.barh(i_state, i_rate, color='steelblue')
        ax3.set_title('Rate of Infant Mortality')

        ax4 = self.figure.add_subplot(234)
        mat_rate = self.m_mortality.sort_values(by='Ratio', ascending=True)
        mat_rate = pd.DataFrame(mat_rate.to_records())
        m_rate = mat_rate['Ratio']
        m_state = mat_rate['State']
        ax4.barh(m_state, m_rate, color='steelblue')
        ax4.set_title('Ratio of Maternal Mortality')
        # print(mat_rate)

        ax11 = self.figure.add_subplot(233)
        v_refuse = self.refuse_vaccine.sort_values(by='Refuse', ascending=True)
        v_refuse = pd.DataFrame(v_refuse.to_records())
        v_refuses = v_refuse['Refuse']
        v_state = v_refuse['State']
        ax11.barh(v_state, v_refuses, color='steelblue')
        ax11.set_title('Number of Vaccine Refusal')

        ax9 = self.figure.add_subplot(235)
        pivot_table = self.life_e.pivot('Sex', 'Ethnic Group', 'Life expectancy')
        # ax9.set_xlabel('Ethnic Group')
        # ax9.set_ylabel('Sex')
        ax9.set_title('Life Expectancy')
        sns.heatmap(pivot_table, ax=ax9, annot=True, fmt=".1f", linewidths=.5, square=True, cmap='Blues_r')
        # print(pivot_table)

        ax10 = self.figure.add_subplot(232)
        category = self.df_immune['Immunised category']
        percent = self.df_immune['Percentage']
        color = sns.color_palette('Blues_r')[0:5]
        ax10.pie(percent, labels=category, autopct='%1.2f%%', shadow=True, colors=color)
        ax10.axis('equal')
        ax10.set_title('Percentage of Malaysian Immunised')
        self.canvas.draw_idle()

        ##############################__RANKING__#############################
        i_mortality_by_states = self.i_mortality.groupby(['State']).sum()
        p_by_states = self.population.groupby(['State']).sum()
        death_rate = self.death_rate_state.groupby(['State']).mean()
        m_mortality = self.m_mortality.groupby(['State']).mean()
        refuse_vaccine = self.refuse_vaccine.groupby(['State']).mean()
        refuse_vaccine['Refuse vaccine rank'] = refuse_vaccine['Refuse'].rank(ascending=True)
        vr_rank = refuse_vaccine['Refuse vaccine rank']
        i_mortality_by_states['Infant mortality rank'] = i_mortality_by_states['Rate'].rank(ascending=True)
        im_rank = i_mortality_by_states['Infant mortality rank']
        m_mortality['Maternal mortality rank'] = m_mortality['Ratio'].rank(ascending=True)
        mm_rank = m_mortality['Maternal mortality rank']
        p_by_states['Population rank'] = p_by_states['per 1000'].rank(ascending=False)
        p_rank = p_by_states['Population rank']
        death_rate['Death rank'] = death_rate['Death rate'].rank(ascending=True)
        d_rank = death_rate['Death rank']
        rankk = pd.merge(p_rank, im_rank, on='State')
        rankk.reset_index(drop=False, inplace=True)
        rankk = pd.merge(rankk, mm_rank, on='State')
        rankk = pd.merge(rankk, d_rank, on='State')
        rankk = pd.merge(rankk, vr_rank, on='State')
        rankk['mean'] = rankk.mean(axis=1)
        rankk = rankk.sort_values(by=['mean'], ascending=True)
        rankk['Rank'] = rankk['mean'].rank(ascending=True).astype(int)

        ax12 = self.figure.add_subplot(236)
        x = rankk['State']
        y = rankk['Rank']
        ax12.barh(x, y, color='steelblue')
        ax12.bar_label(ax12.containers[0])
        ax12.set_title('States Ranking')
        # sns.heatmap(ranking_table, ax=ax12, annot=True, fmt="d", linewidths=.5, square=True, cmap='Blues_r')
        # print(ranking_table)

        self.canvas.draw_idle()

app = QApplication([])

app.setStyleSheet("""
    QTabBar::tab {
        background: lightgray;
        color: black;
        border: 0;
        /* min-width: 100px; */
        max-width: 200px;
        /* width: 150px; */
        height: 20px;
        padding: 5px;
    }

    QTabBar::tab:selected {
        background: gray;
        color: white;
    }
""")

widget = CustomWidget()
widget.show()

sys.exit(app.exec_())
