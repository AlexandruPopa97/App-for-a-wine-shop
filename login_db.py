<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>211</width>
    <height>326</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <layout class="QGridLayout" name="gridLayout_2">
    <item row="0" column="0">
     <layout class="QGridLayout" name="gridLayout">
      <item row="0" column="0">
       <widget class="QLabel" name="label">
        <property name="text">
         <string>User</string>
        </property>
        <property name="alignment">
         <set>Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter</set>
        </property>
        <property name="wordWrap">
         <bool>false</bool>
        </property>
       </widget>
      </item>
      <item row="0" column="1">
       <widget class="QLineEdit" name="lineEdit">
        <property name="text">
         <string>root</string>
        </property>
        <property name="placeholderText">
         <string>Insert root name here</string>
        </property>
        <property name="clearButtonEnabled">
         <bool>false</bool>
        </property>
       </widget>
      </item>
      <item row="1" column="0">
       <widget class="QLabel" name="label_2">
        <property name="text">
         <string>Password</string>
        </property>
        <property name="alignment">
         <set>Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter</set>
        </property>
       </widget>
      </item>
      <item row="1" column="1">
       <widget class="QLineEdit" name="lineEdit_2">
        <property name="text">
         <string>root</string>
        </property>
        <property name="echoMode">
         <enum>QLineEdit::Password</enum>
        </property>
        <property name="placeholderText">
         <string>Insert password here</string>
        </property>
        <property name="clearButtonEnabled">
         <bool>false</bool>
        </property>
       </widget>
      </item>
      <item row="2" column="0">
       <widget class="QLabel" name="label_3">
        <property name="text">
         <string>Host</string>
        </property>
        <property name="alignment">
         <set>Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter</set>
        </property>
       </widget>
      </item>
      <item row="2" column="1">
       <widget class="QLineEdit" name="lineEdit_3">
        <property name="text">
         <string>127.0.0.1</string>
        </property>
        <property name="frame">
         <bool>true</bool>
        </property>
        <property name="dragEnabled">
         <bool>false</bool>
        </property>
        <property name="placeholderText">
         <string>Insert hostname here</string>
        </property>
        <property name="clearButtonEnabled">
         <bool>false</bool>
        </property>
       </widget>
      </item>
      <item row="3" column="0">
       <widget class="QLabel" name="label_4">
        <property name="text">
         <string>Port</string>
        </property>
        <property name="alignment">
         <set>Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter</set>
        </property>
       </widget>
      </item>
      <item row="3" column="1">
       <widget class="QLineEdit" name="lineEdit_4">
        <property name="text">
         <string>3307</string>
        </property>
        <property name="placeholderText">
         <string>Insert port here</string>
        </property>
        <property name="clearButtonEnabled">
         <bool>false</bool>
        </property>
       </widget>
      </item>
      <item row="4" column="0">
       <widget class="QLabel" name="label_5">
        <property name="text">
         <string>Database</string>
        </property>
        <property name="alignment">
         <set>Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter</set>
        </property>
       </widget>
      </item>
      <item row="4" column="1">
       <widget class="QLineEdit" name="lineEdit_5">
        <property name="text">
         <string>ferma_viticola</string>
        </property>
        <property name="readOnly">
         <bool>false</bool>
        </property>
        <property name="placeholderText">
         <string>Insert DB name here</string>
        </property>
        <property name="clearButtonEnabled">
         <bool>false</bool>
        </property>
       </widget>
      </item>
     </layout>
    </item>
    <item row="1" column="0">
     <widget class="QPushButton" name="pushButton">
      <property name="text">
       <string>Login to DB</string>
      </property>
     </widget>
    </item>
   </layout>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>211</width>
     <height>21</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
