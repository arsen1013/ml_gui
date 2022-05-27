from PyQt5.QtWidgets import *
import sys,pickle
from PyQt5 import uic, QtWidgets ,QtCore, QtGui
from data_visualise import data_ #data 로 시작하는거 다 가져올 수 있다는 코드 _ 
from table_display import DataFrameModel


class UI(QMainWindow):
    def __init__(self):
        super(UI,self).__init__()
        uic.loadUi('mainwindow.ui',self)

        global data,steps
        data = data_()

        self.Browse = self.findChild(QPushButton, "Browse")
        self.columns = self.findChild(QListWidget, "column_list")
        self.table = self.findChild(QTableView, "tableView")
        self.data_shape = self.findChild(QLabel, "shape")
        self.label_2 = self.findChild(QLabel, "label_2")
        self.Submit_btn = self.findChild(QPushButton, "Submit")
        self.target_col = self.findChild(QLabel, "target_col")

        self.Browse.clicked.connect(self.getCSV) #이런 함수 제작, 타겟이라는 함수 제작 -> target 이라는 함수를 만들자 
        
        #컬럼을 클릭했단 소리 
        self.columns.clicked.connect(self.target)
        self.Submit_btn.clicked.connect(self.set_target)


    def filldetails(self, flag = 1):
        if flag == 0:
            self.df = data.read_file(str(self.filePath))

        self.columns.clear() #columns안에 내용이 있으면 일단 지우고
        self.column_list = data.get_column_list(self.df) #리스트에 컬럼 리스트 추가
        print(self.column_list)

        for i , j in enumerate(self.column_list):
            # print(i,j)
            stri = f'{j}------{str(self.df[j].dtype)}'
            # print(stri)
            self.columns.insertItem(i,stri )

        x,y = data.get_shape(self.df)
        self.data_shape.setText(f'({x},{y}') #shape 박스에 글씨 넣기  
        self.fill_combo_box() #콤보박스에 채워넣을 것을 실행시킨다. 

    #오른쪽에 집어넣는 테이블 
    def fill_combo_box(self):
        #table_display 클래스를 실행해서 라이브러리 사용한다. 
        x = DataFrameModel(self.df) #함수 선언 
        self.table.setModel(x) #다른 class에도 set모델을 가지고 어떤 모델을 하나 만들어두고 던지면 그 모델을 보여준다. 
        # 데이터 프레임을 x라고 하고 setmodel에 넣으면 모델이 돌아간다. 
        #모델을 셋해준다. 
    
    def getCSV(self):
        self.filePath, _ = QtWidgets.QFileDialog.getOpenFileName(self,"Open file", "", "CSV(*.csv)") #""안에는 기본 위치가 들어간다 #CSV(*.csv)
        self.columns.clear() #클릭하면 지워준다. 
        print(self.filePath)
        if self.filePath != "":
            #self.filepath가 빈 문자열이 아니면 
            self.filldetails(0) 
    
    def target(self):
        self.item = self.columns.currentItem() #컬럼을 누르면 아이템이 self.item에 저장된다. 
    
    def set_target(self):
        self.target_value = str(self.item.text()).split()[0] #컬럼을 누른 아이템이 set_target()함수로 넘어가서 거기서 텍스트만 추출됨 
        print(self.target_value)
        self.target_col.setText(self.target_value) #위에서 처리한 단어 저장


        
        # self.show()
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = UI()
    window.show()
    sys.exit(app.exec_()) #시스템 빠져나갈때 하는 것 