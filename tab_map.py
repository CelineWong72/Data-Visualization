import sys
import pandas as pd
import seaborn as sns
from functools import reduce
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import geopandas as gpd


class MapWindow(QDialog):
    def __init__(self, parent=None):
        super(MapWindow, self).__init__(parent)
        self.resize(900, 900)
        sns.set(style="whitegrid", palette="pastel", color_codes=True)
        sns.mpl.rc("figure", figsize=(20, 10))

        self.fig, self.axis = plt.subplots(1, figsize=(20, 10), dpi=200)
        self.canv = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canv, self)
        self.axis.axis('off')

        self.button1 = QPushButton('Population')
        self.button2 = QPushButton('Death')
        self.button3 = QPushButton('Infant Mortality')
        self.button4 = QPushButton('Maternal Mortality')

        self.button1.clicked.connect(self.p_plot)
        self.button2.clicked.connect(self.d_plot)
        self.button3.clicked.connect(self.i_plot)
        self.button4.clicked.connect(self.m_plot)

        layout = QVBoxLayout()
        b_layout = QHBoxLayout()

        layout.addWidget(self.toolbar)
        b_layout.addWidget(self.button1)
        b_layout.addWidget(self.button2)
        b_layout.addWidget(self.button3)
        b_layout.addWidget(self.button4)

        layout.addWidget(self.canv)
        layout.addLayout(b_layout)
        self.setLayout(layout)

        self.map_df = gpd.read_file(r'C:\Users\User\sampleTutorial\map_data\polbnda_mys.shp')
        self.p_df = pd.read_csv(r'C:\Users\User\sampleTutorial\data\map_pop.csv')
        self.d_df = pd.read_csv(r'C:\Users\User\sampleTutorial\data\map_death.csv')
        self.i_df = pd.read_csv(r'C:\Users\User\sampleTutorial\data\map_infant.csv')
        self.m_df = pd.read_csv(r'C:\Users\User\sampleTutorial\data\map_maternal.csv')
        # print(self.p_df)
        # print(self.d_df)
        # print(self.i_df)
        # print(self.m_df)
        for_p_map = self.p_df.rename(index=str, columns={'State': 'nam', 'per 1000': 'pop'})
        for_d_map = self.d_df.rename(index=str, columns={'State': 'nam', 'Number of death': 'death'})
        for_i_map = self.i_df.rename(index=str, columns={'State': 'nam', 'Rate': 'rate'})
        for_m_map = self.m_df.rename(index=str, columns={'State': 'nam', 'Ratio': 'ratio'})

        all_data = [for_p_map, for_d_map, for_i_map, for_m_map]
        all_merge = reduce(lambda left, right: pd.merge(left, right, on=['nam'], how='outer'), all_data)
        # print(all_merge.head())
        self.map_df['state_lowerc'] = self.map_df['nam'].str.lower()
        all_merge['state_lowerc'] = all_merge['nam'].str.lower()
        self.merged = self.map_df.merge(all_merge, on='state_lowerc')
        # print(self.merged.columns)
        # print(self.merged.head())

    def p_plot(self):
        variable = 'pop_y'
        vmin, vmax = 120, 220
        self.merged.plot(column=variable, cmap='Greens', linewidth=0.8, ax=self.axis, edgecolor='0.8')
        # self.ax.axis('off')
        self.axis.set_title('Population', fontdict={'fontsize': '15', 'fontweight': '3'})

        # Create colorbar as a legend
        sm = plt.cm.ScalarMappable(cmap='Greens', norm=plt.Normalize(vmin=vmin, vmax=vmax))
        # empty array for the data range
        sm._A = []

        # add the colorbar to the figure
        # self.figure.colorbar(sm)

        # saving our map as .png file.
        # fig.savefig('map_export.png', dpi=300)

        self.canv.draw_idle()

    def d_plot(self):
        variable = 'death'
        vmin, vmax = 120, 220
        self.merged.plot(column=variable, cmap='Reds', linewidth=0.8, ax=self.axis, edgecolor='0.8')

        # self.ax.axis('off')
        self.axis.set_title('Death', fontdict={'fontsize': '15', 'fontweight': '3'})

        # Create colorbar as a legend
        sm = plt.cm.ScalarMappable(cmap='Reds', norm=plt.Normalize(vmin=vmin, vmax=vmax))
        # empty array for the data range
        sm._A = []
        # add the colorbar to the figure
        # cbar = self.figure.colorbar(sm)

        # saving our map as .png file.
        # fig.savefig('map_export.png', dpi=300)

        self.canv.draw_idle()

    def i_plot(self):
        variable = 'rate'
        vmin, vmax = 120, 220
        self.merged.plot(column=variable, cmap='Purples', linewidth=0.8, ax=self.axis, edgecolor='0.8')

        # self.ax.axis('off')
        self.axis.set_title('Infant Mortality', fontdict={'fontsize': '15', 'fontweight': '3'})

        # Create colorbar as a legend
        sm = plt.cm.ScalarMappable(cmap='Purples', norm=plt.Normalize(vmin=vmin, vmax=vmax))
        # empty array for the data range
        sm._A = []
        # add the colorbar to the figure
        # cbar = self.figure.colorbar(sm)

        # saving our map as .png file.
        # fig.savefig('map_export.png', dpi=300)

        self.canv.draw_idle()

    def m_plot(self):
        variable = 'ratio'
        vmin, vmax = 120, 220
        self.merged.plot(column=variable, cmap='Blues', linewidth=0.8, ax=self.axis, edgecolor='0.8')

        # self.ax.axis('off')
        self.axis.set_title('Maternal Mortality', fontdict={'fontsize': '15', 'fontweight': '3'})

        # Create colorbar as a legend
        sm = plt.cm.ScalarMappable(cmap='Blues', norm=plt.Normalize(vmin=vmin, vmax=vmax))
        # empty array for the data range
        sm._A = []
        # add the colorbar to the figure
        # cbar = self.figure.colorbar(sm)

        # saving our map as .png file.
        # fig.savefig('map_export.png', dpi=300)

        self.canv.draw_idle()


if __name__ == '__main__':
    # creating apyqt5 application
    app = QApplication(sys.argv)

    # creating a window object
    main = MapWindow()

    # showing the window
    main.show()

    # loop
    sys.exit(app.exec_())