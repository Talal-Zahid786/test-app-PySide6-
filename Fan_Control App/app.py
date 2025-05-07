import math, sys
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtUiTools import *
from PySide6.QtGui import *

from modules.main import *
import threading
import time

loader = QUiLoader()

app = QApplication(sys.argv)

angle1 = 360 
angle2 = 0
previous_angle2 = angle2
decrement_flag = False
interval_ms = 200
error = 0
blade = QPixmap("assests/fan_blade.png")
arc1_val = QPixmap("assests/arc-rotor_down.png")
arc_needle = QPixmap("assests/arc_needle.png")

def show_error_popup(message="An error occurred"):
    error_box = QMessageBox()
    error_box.setIcon(QMessageBox.Critical)
    error_box.setWindowTitle("Error")
    error_box.setText(message)
    error_box.setStandardButtons(QMessageBox.Ok)
    error_box.exec()

def rotate_fan_blade():
    global angle1
    print(angle1)
    print("Entered")
    transform = QTransform().rotate(angle1)
    rotated_pixmap = blade.transformed(transform, Qt.SmoothTransformation)
    MainWindow.fan_blade.setPixmap(rotated_pixmap)
    angle1 = (angle1 - 20) % 360 


def fan_button_click():
    global error
    print("Button Clicked")
    [fan_status,error] = toggle_fan_status()
    if (error == 0):
        MainWindow.fan_body.setEnabled(fan_status)
        MainWindow.fan_blade.setEnabled(fan_status)
        if fan_status:
            timer1.start(1000-(MainWindow.dial.value()*0.45))
        else:
            timer1.stop()
    elif (error == -1):
        show_error_popup(f"Error: Device Not Found! Please Scan Device First.")
        print("Device Not Found! Please Scan Device First.")
    else:
        show_error_popup(f"Error: Unable to Communicating with Device! Check Your Device.")
        print("Error Communicating with Device! Check Your Device.")
    
def fan_speed_control():
    global interval_ms,error
    interval_ms = MainWindow.dial.value()
    timer1.setInterval(135-(interval_ms*0.45))
    error = setFanSpeed(interval_ms)

def get_ip():
    ip = nslookup("fan-controller")
    if (ip!=""):
        MainWindow.ip_label.setText(ip)
    else:
        MainWindow.ip_label.setText("")
        show_error_popup("Error: Unable to find Device")

def rotate_arc_bar():
    global angle2,previous_angle2,decrement_flag
    transform2 = QTransform().rotate(angle2)
    rotated_pixmap2 = arc1_val.transformed(transform2, Qt.SmoothTransformation)
    rotated_needle = arc_needle.transformed(transform2, Qt.SmoothTransformation)
    MainWindow.arc1_val1.setPixmap(rotated_pixmap2)
    if (angle2>0.7*270):
        MainWindow.arc1_current_value.setStyleSheet("color: rgba(255, 57, 57, 210);")
    elif(angle2<0.7*270 and not(angle2<0.4*270)):
        MainWindow.arc1_current_value.setStyleSheet("color: rgba(255, 130 ,0, 210);")
    else:
        MainWindow.arc1_current_value.setStyleSheet("color: rgba(85, 255, 127, 210);")
    MainWindow.arc1_current_value.setText(str(100*angle2//270))
    set_arc_value(MainWindow.arc5_needle,MainWindow.arc5_current_value,MainWindow.arc5_min_value,MainWindow.arc5_mid_value,MainWindow.arc5_max_value,100*angle2//270,0,100)
    set_arc_value(MainWindow.arc4_needle,MainWindow.arc4_current_value,MainWindow.arc4_min_value,MainWindow.arc4_mid_value,MainWindow.arc4_max_value,150*angle2//270,0,150)
    set_arc_value(MainWindow.arc3_needle,MainWindow.arc3_current_value,MainWindow.arc3_min_value,MainWindow.arc3_mid_value,MainWindow.arc3_max_value,180*angle2//270,0,180)
    set_arc_value(MainWindow.arc2_needle,MainWindow.arc2_current_value,MainWindow.arc2_min_value,MainWindow.arc2_mid_value,MainWindow.arc2_max_value,1000*angle2//270,50,1000)
    if (angle2 <=90):
        MainWindow.arc1_val3.setPixmap(rotated_pixmap2)
    else:
        transform2 = QTransform().rotate(90)
        rotated_pixmap2 = arc1_val.transformed(transform2, Qt.SmoothTransformation)
        MainWindow.arc1_val3.setPixmap(rotated_pixmap2)
    if (angle2 <=180):
        MainWindow.arc1_val2.setPixmap(rotated_pixmap2)
    else:
        transform2 = QTransform().rotate(180)
        rotated_pixmap2 = arc1_val.transformed(transform2, Qt.SmoothTransformation)
        MainWindow.arc1_val2.setPixmap(rotated_pixmap2)
    if(angle2<270 and not(decrement_flag)):
        angle2 = (angle2 +0.5) % 271
        decrement_flag = False
    else:
        angle2 = (angle2 -0.5) % 271
        decrement_flag = True
        if(angle2 <= 0):
            decrement_flag = False
    previous_angle2 = angle2

def set_arc_value(arc,arc_current_value,arc_min_label,arc_mid_label,arc_max_label,current_val,min_val,max_val):
    if current_val<min_val:
        current_val=min_val
    percent = ((current_val-min_val)/(max_val-min_val))
    mid_point = (max_val-min_val)//2
    angle = int(270*percent)%270
    transform2 = QTransform().rotate(angle)
    rotated_needle = arc_needle.transformed(transform2, Qt.SmoothTransformation)
    arc.setPixmap(rotated_needle)
    arc_min_label.setText(str(min_val))
    arc_max_label.setText(str(max_val))
    arc_mid_label.setText(str(mid_point))
    if (current_val>0.7*max_val):
        arc_current_value.setStyleSheet("color: rgba(255, 57, 57, 210);")
    elif(current_val<0.7*max_val and not(current_val<0.4*max_val)):
        arc_current_value.setStyleSheet("color: rgba(255, 130, 0, 210);")
    else:
        arc_current_value.setStyleSheet("color: rgba(85, 255, 127, 210);")
    arc_current_value.setText(str(int(current_val)))


MainWindow = loader.load("ui/app.ui",None)

position = 0
right = True
left = False

def go_next():
    global current_page, next_page, previous_page
    next_page.show()
    current_page.hide()
    current_page = next_page

def go_back():
    global current_page, next_page, previous_page, position, right, left
    position = 0
    right = True
    left = False
    previous_page.show()
    timer3.start(1)
    # previous_page.scroll(-805,0)
    # for i in range(previous_page.width()):
    #     print(-i)
    #     previous_page.scroll(-1,0)
    current_page.hide()
    current_page = previous_page

def move_screen():
    global position, right , left
    if(left):
        if (position>0):
            position -= 5
            previous_page.scroll(-5,0)
        else:
            timer3.stop()
    if(right):
        if (position<=previous_page.width()):
            position = previous_page.width()+1
            previous_page.scroll(previous_page.width(),0)
            print(position)
        else:
            right = False
            left = True
            # timer3.stop()

MainWindow.setWindowTitle("Fan Control and Power Monitor App")
MainWindow.fan_body.setPixmap(QPixmap("assests/fan_body.png"))
MainWindow.fan_blade.setPixmap(blade)
MainWindow.fan_button.clicked.connect(fan_button_click)
MainWindow.ip_scan.clicked.connect(get_ip)
MainWindow.dial.valueChanged.connect(fan_speed_control)
MainWindow.next_page.setIcon(QIcon.fromTheme("go-next"))
MainWindow.next_page.clicked.connect(lambda: MainWindow.stackedWidget.setCurrentIndex(1))
timer1 = QTimer()
timer1.timeout.connect(rotate_fan_blade)

MainWindow.arc1_body.setPixmap(QPixmap("assests/arc_body.png"))
MainWindow.arc1_val1.setPixmap(arc1_val)
MainWindow.arc1_val2.setPixmap(arc1_val)
MainWindow.arc1_val3.setPixmap(arc1_val)
MainWindow.arc5_body.setPixmap(QPixmap("assests/arc_body_simple.png"))
MainWindow.arc4_body.setPixmap(QPixmap("assests/arc_body_brown.png"))
MainWindow.arc3_body.setPixmap(QPixmap("assests/arc_body_purple.png"))
MainWindow.arc2_body.setPixmap(QPixmap("assests/arc_body_black.png"))
MainWindow.arc5_needle.setPixmap(arc_needle)
MainWindow.arc4_needle.setPixmap(arc_needle)
MainWindow.arc3_needle.setPixmap(arc_needle)
MainWindow.arc2_needle.setPixmap(arc_needle)
MainWindow.previous_page.setIcon(QIcon.fromTheme("go-previous"))
MainWindow.previous_page.clicked.connect(lambda: MainWindow.stackedWidget.setCurrentIndex(0))
MainWindow.show()

timer2 = QTimer()
timer2.start(5)
timer2.timeout.connect(rotate_arc_bar)

timer3 = QTimer()
timer3.timeout.connect(move_screen)

app.exec()