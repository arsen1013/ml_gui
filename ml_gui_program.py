from PyQt5.QtWidgets import *
import sys,pickle
from PyQt5 import uic, QtWidgets ,QtCore, QtGui
from data_visualise import data_ #data 로 시작하는거 다 가져올 수 있다는 코드 " _ "
from table_display import DataFrameModel
from add_steps import add_steps


class UI(QMainWindow):
    def __init__(self):
        super(UI,self).__init__()
        uic.loadUi('mainwindow.ui',self)

        global data,steps #global 변수 
        data = data_()
        steps = add_steps()

        # Qdesigner 에 넣었던 버튼을 인식하도록 지정해주기 
        self.Browse = self.findChild(QPushButton, "Browse")
        self.columns = self.findChild(QListWidget, "column_list")
        self.table = self.findChild(QTableView, "tableView")
        self.data_shape = self.findChild(QLabel, "shape")
        self.label_2 = self.findChild(QLabel, "label_2")
        self.Submit_btn = self.findChild(QPushButton, "Submit")
        self.target_col = self.findChild(QLabel, "target_col")
        self.cat_column = self.findChild(QComboBox, "cat_column") #여기엔 자동으로 뭔가가 채워져야 한다. 
        self.convert_btn = self.findChild(QPushButton, "convert_btn") #이걸 클릭했을떄 함수가 실행되도록 한다.
        self.dropcolumn = self.findChild(QComboBox, "dropcolumn") #여기엔 자동으로 뭔가가 채워져야 한다. 

        # 버튼 클릭
        self.Browse.clicked.connect(self.getCSV) #이런 함수 제작, 타겟이라는 함수 제작 -> target 이라는 함수를 만들자 
        self.columns.clicked.connect(self.target)
        self.Submit_btn.clicked.connect(self.set_target)
        self.convert_btn.clicked.connect(self.con_cat)




    def filldetails(self, flag = 1):
        #그냥 flag라는 명칭 주고 1을 줌 자동으로 인식하기 위함 
        if flag == 0:
            self.df = data.read_file(str(self.filePath))

        self.columns.clear() #columns안에 내용이 있으면 일단 지우고
        self.column_list = data.get_column_list(self.df) #data_visualise.py에서 만든 column_list 이용해 컬럼 리스트 추가
        # print(self.column_list)

        for i , j in enumerate(self.column_list):
            # print(i,j)
            stri = f'{j}------{str(self.df[j].dtype)}'
            # print(stri)
            self.columns.insertItem(i,stri)

        x,y = data.get_shape(self.df)
        self.data_shape.setText(f'({x},{y}') #shape 박스에 글씨 넣기  
        self.fill_combo_box() #콤보박스에 채워넣을 것을 실행시킨다. 




    #오른쪽에 집어넣는 테이블 
    def fill_combo_box(self):

        self.cat_column.clear()
        self.cat_column.addItems(self.column_list) #filldetails에서 만든 column_list내용 삽입 
        self.dropcolumn.clear()
        self.dropcolumn.addItems(self.dropcolumn) #filldetails에서 만든 column_list내용 삽입 

        #table_display 클래스를 실행해서 라이브러리 사용한다. 
        x = DataFrameModel(self.df) #함수 선언 
        self.table.setModel(x) #다른 class에도 set모델을 가지고 어떤 모델을 하나 만들어두고 던지면 그 모델을 보여준다. 
        # 데이터 프레임을 x라고 하고 setmodel에 넣으면 모델이 돌아간다. 
        #모델을 셋해준다. 
    



    def getCSV(self):
        self.filePath, _ = QtWidgets.QFileDialog.getOpenFileName(self,"Open file", "", "CSV(*.csv)") #""안에는 기본 위치가 들어간다 #CSV(*.csv)
        self.columns.clear() #클릭하면 지워준다. 
        # print(self.filePath)
        if self.filePath != "":
            #self.filepath가 빈 문자열이 아니면 
            self.filldetails(0) #데이터를 최초로 불러오니까 0을 줌 
    



    def target(self):
        self.item = self.columns.currentItem() #컬럼을 누르면 아이템이 self.item에 저장된다. 
    



    def set_target(self):
        self.target_value = str(self.item.text()).split()[0] #컬럼을 누른 아이템이 set_target()함수로 넘어가서 거기서 텍스트만 추출됨 
        # print(self.target_value)
        steps.add_code(f"target=data[{self.target_value}]") #add_steps.py에 있는 함수 실행 
        self.target_col.setText(self.target_value) #위에서 처리한 단어 저장
        # self.show()




    def con_cat(self):
        #컬럼 내용을 to categorical 해주는 함수 
        #콤보박스에 있는 내용을 
        selected = self.cat_column.currentText()
        # print(selected)
        self.df[selected], func_name = data.convert_category(self.df,selected)  #data_visualise.py의 convert_category 함수는 인자를 두개 리턴하므로 두개를 받아주는게 낫다. 
        
        #잘 들어갔는지 확인하기 위한.. 코드 필수 아님 
        steps.add_text("Column "+ selected + " converted using LabelEncoder")
        steps.add_pipeline("LabelEncoder",func_name)
        self.filldetails()




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = UI()
    window.show()
    sys.exit(app.exec_()) #시스템 빠져나갈때 하는 것 