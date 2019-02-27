#Import fisierele de UI ale ecranului principal si ale ferestrelor de dialog
#Aestea au fost create cu ajutorul programului QTDesigner, de aceea codul din astea nu vor fi comentate
from main import Ui_MainWindow
import add_vin_masa
import add_vin_regiune
import add_vin_DOC
import edit_vin_masa
import edit_vin_regiune
import edit_vin_DOC
import verifica_comanda
import sys


#Import toate clasele pe care e voi folosi in program
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QTabBar, QStackedWidget, QMessageBox, QTableWidgetItem, QTableWidget
from PyQt5 import QtGui
import mysql.connector
import time


#Clasa principala ce contine majoritatea functiilor definite de mine pe care le folosesc in program.
class MainApp(QMainWindow, Ui_MainWindow):

    #Functia de mai jos seteaza functionarea butoanelor din meniul principal, dar si apelarea functiei de initializare
    #a UI-ului
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)


        self.setupUi(self)
        self.pushButton.clicked.connect(self.connect_db)
        self.pushButton_2.clicked.connect(self.change_index_to_0)
        self.pushButton_3.clicked.connect(self.change_index_to_1)
        self.pushButton_4.clicked.connect(self.change_index_to_2)
        self.pushButton_6.clicked.connect(self.change_index_to_3)
        self.pushButton_7.clicked.connect(self.change_index_to_4)
        self.statusbar.showMessage("Not connected to DataBase")
        self.init_ui()


    #Functiile urmatoare descriu functionalitatile butoanelor din meniul principal
    def change_index_to_0(self):
        self.show_database_stats()
        self.stackedWidget.setCurrentIndex(0)

    def change_index_to_1(self):
        self.stackedWidget.setCurrentIndex(1)
        self.load_database()
        self.load_database_2()
        self.load_database_3()

    def change_index_to_2(self):
        self.stackedWidget.setCurrentIndex(2)
        self.show_comenzi()

    def change_index_to_3(self):
        self.stackedWidget.setCurrentIndex(3)
        self.interogare_simpla_1()
        self.interogare_simpla_2()
        self.interogare_simpla_3()
        self.interogare_simpla_4()
        self.interogare_simpla_5()
        self.interogare_simpla_6()

    def change_index_to_4(self):
        self.stackedWidget.setCurrentIndex(4)
        self.interogare_complexa_1()
        self.interogare_complexa_2()
        self.interogare_complexa_3()
        self.interogare_complexa_4()


    #Functia urmatoare este functia de initializare a user interface
    def init_ui(self):
        self.show()

        self.pushButton_8.clicked.connect(self.show_Add_Dialog_1)
        self.pushButton_10.clicked.connect(self.delete_data)
        self.pushButton_9.clicked.connect(self.show_edit_dialog_1)

        self.pushButton_11.clicked.connect(self.show_add_dialog_2)
        self.pushButton_12.clicked.connect(self.show_edit_dialog_2)
        self.pushButton_13.clicked.connect(self.delete_data_2)

        self.pushButton_14.clicked.connect(self.show_add_dialog_3)
        self.pushButton_15.clicked.connect(self.show_edit_dialog_3)
        self.pushButton_16.clicked.connect(self.delete_data_3)

        self.pushButton_5.clicked.connect(self.show_verifica)
        self.pushButton_17.clicked.connect(self.delete_comanda)

    #Functia urmatoare afiseaza dialogul de adaugare a primei categorii de vinuri
    def show_Add_Dialog_1(self):
        self.adding = AddDialog_1()
        self.adding.pushButton_11.clicked.connect(self.Add_Data_1)
        self.adding.pushButton_8.clicked.connect(self.clear_dialog_1)
        self.adding.exec()

    # Functia urmatoare afiseaza dialogul de adaugare a celei de a2-a categorii de vinuri
    def show_add_dialog_2(self):
        self.adding2 = AddDialog_2()
        self.adding2.pushButton_15.clicked.connect(self.add_data_2)
        self.adding2.pushButton_14.clicked.connect(self.clear_dialog_2)
        self.adding2.exec()

    # Functia urmatoare afiseaza dialogul de adaugare a celei de a 3-a categorii de vinuri
    def show_add_dialog_3(self):
        self.adding2 = AddDialog_3()
        self.adding2.pushButton_10.clicked.connect(self.add_data_3)
        self.adding2.pushButton_13.clicked.connect(self.clear_dialog_3)
        self.adding2.exec()


    # Functie urmatoare afiseaza verificarea comenzii
    def show_verifica(self):
        self.verifica = Dialog_verifica_comanda()
        self.verifica.pushButton.clicked.connect(self.rezerva_produsele)
        self.verifica.pushButton_2.clicked.connect(self.anuleaza_comanda)
        query = 'SELECT * FROM comanda'
        # Selectez toate comenzile din baza de date pentru a putea identifica comanda curenta (in functie de pozitia ei)
        cursor = self.con_db.cursor(buffered=True)
        cursor.execute(query)
        rezultat = cursor.fetchall()
        for row in enumerate(rezultat):
            if row[0] == self.tableWidget_5.currentRow():
                #Daca produsele pentru comanda curenta au fost deja rezervate nu mai apare optiunea de rezervarea
                if(row[1][3] == 1):
                    self.statusbar.showMessage("Produsele pentru aceasta comanda au fost deja rezervate")
                    self.verifica.pushButton.close()
                else:
                    self.verifica.pushButton_2.close()
                id_comanda = row[1][0]
                id_user = row[1][1]

                # Selectez informatiile despre clientul care a efectuat comanda pentru a le afisa
                cursor.execute("SELECT * FROM user WHERE id_user =%(id)s", {'id': id_user})
                rez = cursor.fetchall()
                self.verifica.lineEdit.setText(rez[0][1])
                self.verifica.lineEdit_2.setText(rez[0][2])
                self.verifica.lineEdit_3.setText(rez[0][4])
                self.verifica.lineEdit_4.setText(rez[0][5])
                if(rez[0][11] != None and rez[0][12] != None):
                    self.verifica.textEdit.setText(rez[0][6]+" "+rez[0][7]+" "+rez[0][8]+" "+ rez[0][9]+" "+ str(rez[0][10])+" "+ rez[0][11]+" "+ str(rez[0][12]) +" "+ str(rez[0][13]))
                else:
                    self.verifica.textEdit.setText(
                        rez[0][6] + " " + rez[0][7] + " " + rez[0][8] + " " + rez[0][9] + " " + str(rez[0][10]) + " " + str(rez[0][13]))

                #Calculez pretul total al produselor din comanda curenta
                suma = 0
                cursor.execute(
                    "SELECT pret, cantitate FROM vin_de_masa A, comanda_vin B, comanda C WHERE A.id_vin_masa = B.id_vin_masa AND C.id_comanda=B.id_comanda AND C.id_comanda=%(id)s",
                    {'id': id_comanda})
                rez = cursor.fetchall()
                for nr, pret in enumerate(rez):
                    suma = suma + pret[0] * pret[1]
                cursor.execute(
                    "SELECT pret, cantitate FROM vin_indicatie_geografica A, comanda_vin B, comanda C WHERE A.id_vin_indicatie_geografica = B.id_vin_IG AND C.id_comanda=B.id_comanda AND C.id_comanda=%(id)s",
                    {'id': id_comanda})
                rez = cursor.fetchall()
                for nr, pret in enumerate(rez):
                    suma = suma + pret[0] * pret[1]
                cursor.execute(
                    "SELECT pret, cantitate FROM vin_denumire_origine_controlata A, comanda_vin B, comanda C WHERE A.id_vin_denumire_origine_controlata = B.id_vin_DOC AND C.id_comanda=B.id_comanda AND C.id_comanda=%(id)s",
                    {'id': id_comanda})
                rez = cursor.fetchall()
                for nr, pret in enumerate(rez):
                    suma = suma + pret[0] * pret[1]

                #Determin daca stocul curent este suficient pentru a trimite comanda curenta
                #IN acelasi timp introduc in tabelul cu produsele comandate
                cursor.execute("SELECT tip_vin,id_vin_masa,id_vin_IG,id_vin_DOC,cantitate FROM comanda_vin WHERE id_comanda=%(id)s",{'id':id_comanda})
                rez1 = cursor.fetchall()
                disponibilitate_stoc = 1
                for raw_index, raw_data in enumerate(rez1):
                    self.verifica.tableWidget.insertRow(raw_index)
                    for colm_index, col_data in enumerate(raw_data):
                        if(colm_index == 0):
                            if(raw_data[0] == 1):
                                cursor.execute("SELECT denumire FROM vin_de_masa WHERE id_vin_masa=%(id)s", {'id':raw_data[1]})
                                vin = cursor.fetchall()
                                self.verifica.tableWidget.setItem(raw_index, colm_index, QTableWidgetItem(str(vin[0][0])))
                            elif(raw_data[0] == 2):
                                cursor.execute("SELECT denumire_generica  FROM vin_indicatie_geografica WHERE id_vin_indicatie_geografica=%(id)s",
                                               {'id': raw_data[2]})
                                vin = cursor.fetchall()
                                self.verifica.tableWidget.setItem(raw_index, colm_index, QTableWidgetItem(str(vin[0][0])))
                            elif (raw_data[0] == 3):
                                cursor.execute(
                                    "SELECT denumire_OC   FROM vin_denumire_origine_controlata WHERE id_vin_denumire_origine_controlata=%(id)s",
                                    {'id': raw_data[3]})
                                vin = cursor.fetchall()
                                self.verifica.tableWidget.setItem(raw_index, colm_index, QTableWidgetItem(str(vin[0][0])))
                        elif(colm_index == 1):
                            if (raw_data[0] == 1):
                                cursor.execute("SELECT pret FROM vin_de_masa WHERE id_vin_masa=%(id)s",
                                               {'id': raw_data[1]})
                                pret = cursor.fetchall()
                                self.verifica.tableWidget.setItem(raw_index, colm_index, QTableWidgetItem(str(pret[0][0])))
                            elif (raw_data[0] == 2):
                                cursor.execute(
                                    "SELECT pret  FROM vin_indicatie_geografica WHERE id_vin_indicatie_geografica=%(id)s",
                                    {'id': raw_data[2]})
                                pret = cursor.fetchall()
                                self.verifica.tableWidget.setItem(raw_index, colm_index, QTableWidgetItem(str(pret[0][0])))
                            elif (raw_data[0] == 3):
                                cursor.execute(
                                    "SELECT pret FROM vin_denumire_origine_controlata WHERE id_vin_denumire_origine_controlata=%(id)s",
                                    {'id': raw_data[3]})
                                pret = cursor.fetchall()
                                self.verifica.tableWidget.setItem(raw_index, colm_index, QTableWidgetItem(str(pret[0][0])))
                        elif(colm_index == 2):
                            self.verifica.tableWidget.setItem(raw_index, colm_index, QTableWidgetItem(str(raw_data[4])))
                        else:
                            if (raw_data[0] == 1):
                                cursor.execute("SELECT numar_unitati  FROM vin_de_masa WHERE id_vin_masa=%(id)s",
                                               {'id': raw_data[1]})
                                cantitate = cursor.fetchall()
                                if(cantitate[0][0] < raw_data[4]):
                                    disponibilitate_stoc = 0
                                self.verifica.tableWidget.setItem(raw_index, colm_index, QTableWidgetItem(str(cantitate[0][0])))
                            elif (raw_data[0] == 2):
                                cursor.execute(
                                    "SELECT numar_unitati   FROM vin_indicatie_geografica WHERE id_vin_indicatie_geografica=%(id)s",
                                    {'id': raw_data[2]})
                                cantitate = cursor.fetchall()
                                if (cantitate[0][0] < raw_data[4]):
                                    disponibilitate_stoc = 0
                                self.verifica.tableWidget.setItem(raw_index, colm_index, QTableWidgetItem(str(cantitate[0][0])))
                            elif (raw_data[0] == 3):
                                cursor.execute(
                                    "SELECT numar_unitati  FROM vin_denumire_origine_controlata WHERE id_vin_denumire_origine_controlata=%(id)s",
                                    {'id': raw_data[3]})
                                cantitate = cursor.fetchall()
                                if (cantitate[0][0] < raw_data[4]):
                                    disponibilitate_stoc = 0
                                self.verifica.tableWidget.setItem(raw_index, colm_index, QTableWidgetItem(str(cantitate[0][0])))

                #Afisez in chenarul corespunzator statusul de disponibilitate al comenzii curente
                self.verifica.lineEdit_5.setText(str(suma))
                if(disponibilitate_stoc):
                    self.verifica.lineEdit_6.setText("DA")
                else:
                    self.verifica.lineEdit_6.setText("NU")
        self.verifica.exec()

    #Functie de mai jos rezerva produsele din comanda curenta
    #Mai precis, verifica disponibilitatea stocului curent apoi updateaza stocul
    def rezerva_produsele(self):
        try:
            query = 'SELECT * FROM comanda'
            cursor = self.con_db.cursor(buffered=True)
            cursor.execute(query)
            rezultat = cursor.fetchall()
            for row in enumerate(rezultat):
                if row[0] == self.tableWidget_5.currentRow():
                    id_comanda = row[1][0]
                    id_user = row[1][1]

                    cursor.execute(
                        "SELECT tip_vin,id_vin_masa,id_vin_IG,id_vin_DOC,cantitate FROM comanda_vin WHERE id_comanda=%(id)s",
                        {'id': id_comanda})
                    rez1 = cursor.fetchall()
                    disponibilitate_stoc = 1
                    #Aici functia verifica, pe rand, disponibilitatea pentru fiecare tip de vin
                    for raw_index, raw_data in enumerate(rez1):
                        self.verifica.tableWidget.insertRow(raw_index)
                        for colm_index, col_data in enumerate(raw_data):
                            if(colm_index == 3):
                                if (raw_data[0] == 1):
                                    cursor.execute("SELECT numar_unitati  FROM vin_de_masa WHERE id_vin_masa=%(id)s",
                                                   {'id': raw_data[1]})
                                    cantitate = cursor.fetchall()
                                    if(cantitate[0][0] < raw_data[4]):
                                        disponibilitate_stoc = 0
                                    else:
                                        cursor.execute("UPDATE vin_de_masa SET numar_unitati=%s WHERE id_vin_masa=%s",(cantitate[0][0] - raw_data[4],raw_data[1]))
                                        self.con_db.commit()

                                elif (raw_data[0] == 2):
                                    cursor.execute(
                                        "SELECT numar_unitati   FROM vin_indicatie_geografica WHERE id_vin_indicatie_geografica=%(id)s",
                                        {'id': raw_data[2]})
                                    cantitate = cursor.fetchall()
                                    if (cantitate[0][0] < raw_data[4]):
                                        disponibilitate_stoc = 0
                                    else:
                                        cursor.execute("UPDATE vin_indicatie_geografica SET numar_unitati=%s WHERE id_vin_indicatie_geografica=%s",(cantitate[0][0] - raw_data[4],raw_data[2]))
                                        self.con_db.commit()
                                elif (raw_data[0] == 3):
                                    cursor.execute(
                                        "SELECT numar_unitati  FROM vin_denumire_origine_controlata WHERE id_vin_denumire_origine_controlata=%(id)s",
                                        {'id': raw_data[3]})
                                    cantitate = cursor.fetchall()
                                    if (cantitate[0][0] < raw_data[4]):
                                        disponibilitate_stoc = 0
                                    else:
                                        cursor.execute("UPDATE vin_denumire_origine_controlata SET numar_unitati=%s WHERE id_vin_denumire_origine_controlata=%s",(cantitate[0][0] - raw_data[4],raw_data[3]))
                                        self.con_db.commit()
                    #Daca stocul disponibil este suficient se afiseaza mesaj corespunzator si stocul de updateaza
                    if (disponibilitate_stoc):
                        self.statusbar.showMessage("Produsele pentru comanda au fost rezervate cu succes")
                        cursor.execute("UPDATE comanda SET status_expediere=%s WHERE id_comanda=%s",(1, id_comanda))
                        self.con_db.commit()
                        self.show_comenzi()
                        self.verifica.close()
                    else:
                        self.statusbar.showMessage("Nu exista suficiente produse in stoc")
                        self.verifica.lineEdit_6.setText("NU")
        except Exception as error:
            print(error)
            self.con_db.rollback()
            self.statusbar.showMessage("Eroare la rezervarea produselor")


    #Functia de mai jo, de anulare a comenzii, anuleaza rezervarea produselor cu adaptarea stocului curent.
    def anuleaza_comanda(self):
        try:
            query = 'SELECT * FROM comanda'
            cursor = self.con_db.cursor(buffered=True)
            cursor.execute(query)
            rezultat = cursor.fetchall()
            for row in enumerate(rezultat):
                if row[0] == self.tableWidget_5.currentRow():
                    id_comanda = row[1][0]
                    cursor.execute(
                        "SELECT tip_vin,id_vin_masa,id_vin_IG,id_vin_DOC,cantitate FROM comanda_vin WHERE id_comanda=%(id)s",
                        {'id': id_comanda})
                    rez1 = cursor.fetchall()
                    #Pentru fiecare tip de vin se updateaza separat stocul (sunt stocate in tabele diferite ale bazei de date)
                    for raw_index, raw_data in enumerate(rez1):
                        self.verifica.tableWidget.insertRow(raw_index)
                        for colm_index, col_data in enumerate(raw_data):
                            if(colm_index == 3):
                                if (raw_data[0] == 1):
                                    cursor.execute("SELECT numar_unitati  FROM vin_de_masa WHERE id_vin_masa=%(id)s",
                                                   {'id': raw_data[1]})
                                    cantitate = cursor.fetchall()
                                    cursor.execute("UPDATE vin_de_masa SET numar_unitati=%s WHERE id_vin_masa=%s",(cantitate[0][0] + raw_data[4],raw_data[1]))
                                    self.con_db.commit()

                                elif (raw_data[0] == 2):
                                    cursor.execute(
                                        "SELECT numar_unitati   FROM vin_indicatie_geografica WHERE id_vin_indicatie_geografica=%(id)s",
                                        {'id': raw_data[2]})
                                    cantitate = cursor.fetchall()
                                    cursor.execute("UPDATE vin_indicatie_geografica SET numar_unitati=%s WHERE id_vin_indicatie_geografica=%s",(cantitate[0][0] + raw_data[4],raw_data[2]))
                                    self.con_db.commit()
                                elif (raw_data[0] == 3):
                                    cursor.execute(
                                        "SELECT numar_unitati  FROM vin_denumire_origine_controlata WHERE id_vin_denumire_origine_controlata=%(id)s",
                                        {'id': raw_data[3]})
                                    cantitate = cursor.fetchall()
                                    cursor.execute("UPDATE vin_denumire_origine_controlata SET numar_unitati=%s WHERE id_vin_denumire_origine_controlata=%s",(cantitate[0][0] + raw_data[4],raw_data[3]))
                                    self.con_db.commit()

                    #Daca updatarea stocului pentru fiecare produs se executa fara erori se afiseaza mesajul corespunzator
                    self.statusbar.showMessage("Comanda a fost anulata cu succes")
                    cursor.execute("UPDATE comanda SET status_expediere=%s WHERE id_comanda=%s",(0, id_comanda))
                    self.con_db.commit()
                    self.show_comenzi()
                    self.verifica.close()
        except Exception as error:
            print(error)
            self.con_db.rollback()
            self.statusbar.showMessage("Eroare la anularea comenzii")

    #Functia de mai jos sterge toate campurile din fereastra dialog_1, setand fiecare camp cu nimic
    #Dialogul este de adaugare de vinuri de masa
    def clear_dialog_1(self):
        self.adding.denumire.setText("")
        self.adding.soi_struguri.setText("")
        self.adding.tara_origine.setText("")
        self.adding.producator.setText("")
        self.adding.procent_alcool.setText("")
        self.adding.cantitate_zahar.setText("")
        self.adding.culoare.setText("")
        self.adding.recipient.setText("")
        self.adding.volum_recipient.setText("")
        self.adding.numar_unitati.setText("")
        self.adding.pret.setText("")
        self.adding.an_productie.setText("")
        self.adding.timp_pastrare.setText("")
        self.adding.descriere.setText("")

    # Functia de mai jos sterge toate campurile din fereastra dialog_2, setand fiecare camp cu nimic
    #Dialogul este de adaugare de vinuri de origine controlata
    def clear_dialog_2(self):
        self.adding2.denumire_generica_2.setText("")
        self.adding2.soi_struguri_4.setText("")
        self.adding2.tara_origine_4.setText("")
        self.adding2.tara_origine_4.setText("")
        self.adding2.zona_geografica_2.setText("")
        self.adding2.producator_4.setText("")
        self.adding2.procent_alcool_4.setText("")
        self.adding2.cantitate_zahar_4.setText("")
        self.adding2.culoare_4.setText("")
        self.adding2.recipient_4.setText("")
        self.adding2.volum_2.setText("")
        self.adding2.numar_unitati_4.setText("")
        self.adding2.pret_4.setText("")
        self.adding2.an_productie.setText("")
        self.adding2.timp_pastrare.setText("")
        self.adding2.descriere_4.setText("")

    # Functia de mai jos sterge toate campurile din fereastra dialog_3, setand fiecare camp cu nimic
    # Dialogul este de adaugare de vinuri DOC
    def clear_dialog_3(self):
        self.adding2.denumire_oc.setText("")
        self.adding2.soi_struguri_3.setText("")
        self.adding2.tara_origine_3.setText("")
        self.adding2.regiune.setText("")
        self.adding2.producator_3.setText("")
        self.adding2.proces_producere.setText("")
        self.adding2.treapta_calitate.setText("")
        self.adding2.procent_alcool_3.setText("")
        self.adding2.cantitate_zahar_3.setText("")
        self.adding2.culoare_3.setText("")
        self.adding2.aspect_gustativ.setText("")
        self.adding2.aspect_olfactiv.setText("")
        self.adding2.aspect_vizual.setText("")
        self.adding2.temperatura_servire.setText("")
        self.adding2.timp_decantare.setText("")
        self.adding2.recipient_3.setText("")
        self.adding2.volum_recipient_2.setText("")
        self.adding2.numar_unitati_3.setText("")
        self.adding2.pret_3.setText("")
        self.adding2.an_productie.setText("")
        self.adding2.timp_decantare.setText("")
        self.adding2.descriere_3.setText("")


    #Functia de mai jos realizeaza stergerea textelor introduse in ferestra de editare dialog 1
    #Aceasta fereastra ete de editare a vinului de masa
    def clear_edit_dialog_1(self):
        self.edit.denumire.setText("")
        self.edit.soi_struguri.setText("")
        self.edit.tara_origine.setText("")
        self.edit.producator.setText("")
        self.edit.procent_alcool.setText("")
        self.edit.cantitate_zahar.setText("")
        self.edit.culoare.setText("")
        self.edit.recipient.setText("")
        self.edit.volum_recipient.setText("")
        self.edit.numar_unitati.setText("")
        self.edit.pret.setText("")
        self.edit.an_productie.setText("")
        self.edit.timp_pastrare.setText("")
        self.edit.descriere.setText("")

    # Functia de mai jos realizeaza stergerea textelor introduse in ferestra de editare dialog 2
    # Aceasta fereastra ete de editare a vinului de origine controlata
    def clear_edit_dialog_2(self):
        self.edit.denumire_generica_2.setText("")
        self.edit.soi_struguri_4.setText("")
        self.edit.tara_origine_4.setText("")
        self.edit.zona_geografica_2.setText("")
        self.edit.producator_4.setText("")
        self.edit.procent_alcool_4.setText("")
        self.edit.cantitate_zahar_4.setText("")
        self.edit.culoare_4.setText("")
        self.edit.recipient_4.setText("")
        self.edit.volum_2.setText("")
        self.edit.pret_4.setText("")
        self.edit.an_productie.setText("")
        self.edit.timp_pastrare.setText("")
        self.edit.descriere_4.setText("")

    # Functia de mai jos realizeaza stergerea textelor introduse in ferestra de editare dialog 3
    # Aceasta fereastra ete de editare a vinului DOC
    def clear_edit_dialog_3(self):
        self.edit.denumire_oc.setText("")
        self.edit.soi_struguri_3.setText("")
        self.edit.tara_origine_3.setText("")
        self.edit.regiune.setText("")
        self.edit.producator_3.setText("")
        self.edit.proces_producere.setText("")
        self.edit.treapta_calitate.setText("")
        self.edit.procent_alcool_3.setText("")
        self.edit.cantitate_zahar_3.setText("")
        self.edit.culoare_3.setText("")
        self.edit.aspect_gustativ.setText("")
        self.edit.aspect_olfactiv.setText("")
        self.edit.aspect_vizual.setText("")
        self.edit.temperatura_servire.setText("")
        self.edit.timp_decantare.setText("")
        self.edit.recipient_3.setText("")
        self.edit.volum_recipient_2.setText("")
        self.edit.numar_unitati_3.setText("")
        self.edit.pret_3.setText("")
        self.edit.an_productie.setText("")
        self.edit.timp_decantare.setText("")
        self.edit.descriere_3.setText("")


    #Functia de mai jos realizeaza afisarea ferestrei de dialog de editare a tipului de vin de masa
    def show_edit_dialog_1(self):
        self.edit = EditDialog_1()
        self.edit.pushButton_11.clicked.connect(self.edit_data_1)
        self.edit.pushButton_8.clicked.connect(self.clear_edit_dialog_1)
        self.statusbar.showMessage("")
        #Se executa operatie de interogare a bazei de date in care se aduce toate tipurile de vin de masa
        #Apoi in functie de pozitia curenta se determina vinul curent
        #Dupa, se completeaza casutele corespuzatoare cu textele preluate din baza de date
        query = 'SELECT * FROM vin_de_masa'
        cursor = self.con_db.cursor(buffered=True)
        cursor.execute(query)
        for row in enumerate(cursor):
            if row[0] == self.tableWidget.currentRow():
                self.edit.denumire.setText(row[1][1])
                self.edit.soi_struguri.setText(row[1][2])
                self.edit.tara_origine.setText(row[1][3])
                self.edit.producator.setText(row[1][4])
                self.edit.procent_alcool.setText(str(row[1][5]))
                self.edit.cantitate_zahar.setText(str(row[1][6]))
                self.edit.culoare.setText(row[1][7])
                self.edit.recipient.setText(row[1][8])
                self.edit.volum_recipient.setText(str(row[1][9]))
                self.edit.numar_unitati.setText(str(row[1][10]))
                self.edit.pret.setText(str(row[1][11]))
                self.edit.an_productie.setText(str(row[1][12]))
                self.edit.timp_pastrare.setText(str(row[1][13]))
                self.edit.descriere.setText(row[1][14])
        self.edit.exec_()

    # Functia de mai jos realizeaza afisarea ferestrei de dialog de editare a tipului de vin de indicatie geografica
    def show_edit_dialog_2(self):
        self.edit = EditDialog_2()
        self.edit.pushButton_15.clicked.connect(self.edit_data_2)
        self.edit.pushButton_14.clicked.connect(self.clear_edit_dialog_2)
        self.statusbar.showMessage("")
        # Se executa operatie de interogare a bazei de date in care se aduce toate tipurile de vin de indicatie geografica
        # Apoi in functie de pozitia curenta se determina vinul curent
        # Dupa, se completeaza casutele corespuzatoare cu textele preluate din baza de date
        query = 'SELECT * FROM vin_indicatie_geografica'
        cursor = self.con_db.cursor(buffered=True)
        cursor.execute(query)
        for row in enumerate(cursor):
            if row[0] == self.tableWidget_2.currentRow():
                self.edit.denumire_generica_2.setText(row[1][1])
                self.edit.soi_struguri_4.setText(row[1][2])
                self.edit.tara_origine_4.setText(row[1][3])
                self.edit.zona_geografica_2.setText(row[1][4])
                self.edit.producator_4.setText(row[1][5])
                self.edit.procent_alcool_4.setText(str(row[1][6]))
                self.edit.cantitate_zahar_4.setText(str(row[1][7]))
                self.edit.culoare_4.setText(row[1][8])
                self.edit.recipient_4.setText(row[1][9])
                self.edit.volum_2.setText(str(row[1][10]))
                self.edit.numar_unitati_4.setText(str(row[1][11]))
                self.edit.pret_4.setText(str(row[1][12]))
                self.edit.an_productie.setText(str(row[1][13]))
                self.edit.timp_pastrare.setText(str(row[1][14]))
                self.edit.descriere_4.setText(row[1][15])
        self.edit.exec_()

    # Functia de mai jos realizeaza afisarea ferestrei de dialog de editare a tipului de vin DOC
    def show_edit_dialog_3(self):
        self.edit = EditDialog_3()
        self.edit.pushButton_10.clicked.connect(self.edit_data_3)
        self.edit.pushButton_13.clicked.connect(self.clear_edit_dialog_3)
        self.statusbar.showMessage("")
        # Se executa operatie de interogare a bazei de date in care se aduce toate tipurile de vin DOC
        # Apoi in functie de pozitia curenta se determina vinul curent
        # Dupa, se completeaza casutele corespuzatoare cu textele preluate din baza de date
        query = 'SELECT * FROM vin_denumire_origine_controlata'
        cursor = self.con_db.cursor(buffered=True)
        cursor.execute(query)
        for row in enumerate(cursor):
            if row[0] == self.tableWidget_3.currentRow():
                self.edit.denumire_oc.setText(row[1][1])
                self.edit.soi_struguri_3.setText(row[1][2])
                self.edit.tara_origine_3.setText(row[1][3])
                self.edit.regiune.setText(row[1][4])
                self.edit.producator_3.setText(row[1][5])
                self.edit.proces_producere.setText(row[1][6])
                self.edit.treapta_calitate.setText(row[1][7])
                self.edit.procent_alcool_3.setText(str(row[1][8]))
                self.edit.cantitate_zahar_3.setText(str(row[1][9]))
                self.edit.culoare_3.setText(row[1][10])
                self.edit.aspect_gustativ.setText(row[1][11])
                self.edit.aspect_olfactiv.setText(row[1][12])
                self.edit.aspect_vizual.setText(row[1][13])
                self.edit.temperatura_servire.setText(str(row[1][14]))
                self.edit.timp_decantare.setText(str(row[1][15]))
                self.edit.recipient_3.setText(row[1][16])
                self.edit.volum_recipient_2.setText(str(row[1][17]))
                self.edit.numar_unitati_3.setText(str(row[1][18]))
                self.edit.pret_3.setText(str(row[1][19]))
                self.edit.an_productie.setText(str(row[1][20]))
                self.edit.timp_pastrare.setText(str(row[1][21]))
                self.edit.descriere_3.setText(row[1][22])
        self.edit.exec_()

    #Functia de mai jos sterge din baza de date vinul de masa curent selectat
    def delete_data(self):
        try:
            query = 'SELECT * FROM vin_de_masa'
            cursor = self.con_db.cursor(buffered=True)
            cursor.execute(query)
            for raw in enumerate(cursor):
                if raw[0] == self.tableWidget.currentRow():
                    ID_current = raw[1][0]
                    cursor.execute("DELETE FROM vin_de_masa WHERE id_vin_masa = '%s'"
                                   % ''.join(str(ID_current)))
                    self.con_db.commit()
                    self.load_database()
                    self.statusbar.showMessage("Produsul a fost sters cu succes din baza de date")
        except Exception as error:
            print(error)
            self.con_db.rollback()
            self.statusbar.showMessage("Stergerea din baza de date nu a reusit")

    # Functia de mai jos sterge din baza de date vinul de indicatie geografica curent selectat
    def delete_data_2(self):
        try:
            query = 'SELECT * FROM vin_indicatie_geografica'
            cursor = self.con_db.cursor(buffered=True)
            cursor.execute(query)
            for raw in enumerate(cursor):
                if raw[0] == self.tableWidget_2.currentRow():
                    ID_current = raw[1][0]
                    cursor.execute("DELETE FROM vin_indicatie_geografica WHERE id_vin_indicatie_geografica = '%s'"
                                   % ''.join(str(ID_current)))
                    self.con_db.commit()
                    self.load_database_2()
                    self.statusbar.showMessage("Produsul a fost sters cu succes din baza de date")
        except Exception as error:
            print(error)
            self.con_db.rollback()
            self.statusbar.showMessage("Stergerea din baza de date nu a reusit")

    # Functia de mai jos sterge din baza de date vinul DOC curent selectat
    def delete_data_3(self):
        try:
            query = 'SELECT * FROM vin_denumire_origine_controlata'
            cursor = self.con_db.cursor(buffered=True)
            cursor.execute(query)
            for raw in enumerate(cursor):
                if raw[0] == self.tableWidget_3.currentRow():
                    ID_current = raw[1][0]
                    cursor.execute("DELETE FROM vin_denumire_origine_controlata WHERE id_vin_denumire_origine_controlata = '%s'"
                                   % ''.join(str(ID_current)))
                    self.con_db.commit()
                    self.load_database_3()
                    self.statusbar.showMessage("Produsul a fost sters cu succes din baza de date")
        except Exception as error:
            print(error)
            self.con_db.rollback()
            self.statusbar.showMessage("Stergerea din baza de date nu a reusit")
    def delete_comanda(self):
        try:
            query = "SELECT * FROM comanda"
            cursor = self.con_db.cursor()
            cursor.execute(query)
            for raw in enumerate(cursor):
                if raw[0] == self.tableWidget_5.currentRow():
                    id_comanda = raw[1][0]
                    cursor.execute("DELETE FROM comanda_vin WHERE id_comanda='%s'" % ''.join(str(id_comanda)))
                    self.con_db.commit()
                    cursor.execute("DELETE FROM comanda WHERE id_comanda='%s'" % ''.join(str(id_comanda)))
                    self.con_db.commit()
                    self.show_comenzi()
                    self.statusbar.showMessage("Comanda a fost stearsa din baza de date")
        except Exception as error:
            print(error)
            self.con_db.rollback()
            self.statusbar.showMessage("Eroare la stergerea comenzii din baza de date")



    #Functia de mai jos realizeaza editarea vinului de masa selectat
    #Se modifica de catre utilizator fiecare camp ce se doreste modificat apoi prin apasarea de buton se
    #incearca modificarea in baza de date, daca se reuseste se afiseaza mesaj corespunzator
    def edit_data_1(self):
        try:

            query = 'SELECT * FROM vin_de_masa'
            cursor = self.con_db.cursor(buffered=True)
            cursor.execute(query)
            for raw in enumerate(cursor):
                if raw[0] == self.tableWidget.currentRow():
                    denumire = self.edit.denumire.text()
                    soi = self.edit.soi_struguri.text()
                    tara = self.edit.tara_origine.text()
                    producator = self.edit.producator.text()
                    procent_alcool = self.edit.procent_alcool.text()
                    cantitate = self.edit.cantitate_zahar.text()
                    culoare = self.edit.culoare.text()
                    recipient = self.edit.recipient.text()
                    volum = self.edit.volum_recipient.text()
                    numar_unitati = self.edit.numar_unitati.text()
                    pret = self.edit.pret.text()
                    an_productie = self.edit.an_productie.text()
                    timp_pastrare = self.edit.timp_pastrare.text()
                    descriere = self.edit.descriere.toPlainText()
                    ID_current = raw[1][0]
                    cursor.execute(
                        '''UPDATE vin_de_masa 
                        SET denumire = %s,soi_struguri = %s, tara_origine = %s,producator = %s,procent_alcool = %s, 
                        cantitate_zahar = %s,culoare = %s,recipient = %s, volum_recipient = %s, numar_unitati = %s,
                         pret = %s,an_productie = %s, timp_pastrare = %s, descriere = %s
                        WHERE id_vin_masa = %s ''', (denumire, soi, tara, producator, procent_alcool, cantitate, culoare, recipient, volum, numar_unitati, pret, an_productie, timp_pastrare, descriere, ID_current))
                    self.con_db.commit()
                    self.load_database()
                    self.statusbar.showMessage("Produsul a fost modificat cu succes in baza de date")
        except Exception as eroare:
            self.con_db.rollback()
            print(eroare)
            self.statusbar.showMessage("Eroare la modificarea produsului din baza de date")

    # Functia de mai jos realizeaza editarea vinului de indicatie geografica
    # Se modifica de catre utilizator fiecare camp ce se doreste modificat apoi prin apasarea de buton se
    # incearca modificarea in baza de date, daca se reuseste se afiseaza mesaj corespunzator
    def edit_data_2(self):
        try:
            query = 'SELECT * FROM vin_indicatie_geografica'
            cursor = self.con_db.cursor(buffered=True)
            cursor.execute(query)
            for raw in enumerate(cursor):
                if raw[0] == self.tableWidget_2.currentRow():
                    denumire = self.edit.denumire_generica_2.text()
                    soi = self.edit.soi_struguri_4.text()
                    tara = self.edit.tara_origine_4.text()
                    zona = self.edit.zona_geografica_2.text()
                    producator = self.edit.producator_4.text()
                    procent_alcool = self.edit.procent_alcool_4.text()
                    cantitate = self.edit.cantitate_zahar_4.text()
                    culoare = self.edit.culoare_4.text()
                    recipient = self.edit.recipient_4.text()
                    volum = self.edit.volum_2.text()
                    numar_unitati = self.edit.numar_unitati_4.text()
                    pret = self.edit.pret_4.text()
                    an_productie = self.edit.an_productie.text()
                    timp_pastrare = self.edit.timp_pastrare.text()
                    descriere = self.edit.descriere_4.toPlainText()
                    ID_current = raw[1][0]
                    cursor.execute(
                        '''UPDATE vin_indicatie_geografica 
                        SET denumire_generica=%s,soi_struguri=%s, tara_origine = %s,zona_geografica = %s, 
                        producator = %s,procent_alcool = %s, cantitate_zahar = %s,
                        culoare = %s,recipient = %s, volum_recipient = %s, numar_unitati = %s, 
                        pret = %s,an_productie = %s, timp_pastrare = %s, descriere = %s
                        WHERE id_vin_indicatie_geografica = %s ''', (denumire, soi, tara,zona, producator, procent_alcool, cantitate, culoare, recipient, volum, numar_unitati, pret, an_productie, timp_pastrare, descriere, ID_current))
                    self.con_db.commit()
                    self.load_database_2()
                    self.statusbar.showMessage("Produsul a fost modificat cu succes in baza de date")
        except Exception as eroare:
            self.con_db.rollback()
            print(eroare)
            self.statusbar.showMessage("Eroare la modificarea produsului din baza de date")

    # Functia de mai jos realizeaza editarea vinului DOC
    # Se modifica de catre utilizator fiecare camp ce se doreste modificat apoi prin apasarea de buton se
    # incearca modificarea in baza de date, daca se reuseste se afiseaza mesaj corespunzator
    def edit_data_3(self):
        try:
            query = 'SELECT * FROM vin_denumire_origine_controlata'
            cursor = self.con_db.cursor(buffered=True)
            cursor.execute(query)
            for raw in enumerate(cursor):
                if raw[0] == self.tableWidget_3.currentRow():
                    denumire = self.edit.denumire_oc.text()
                    soi = self.edit.soi_struguri_3.text()
                    tara = self.edit.tara_origine_3.text()
                    regiune = self.edit.regiune.text()
                    producator = self.edit.producator_3.text()
                    proces = self.edit.proces_producere.text()
                    treapta_calitate = self.edit.treapta_calitate.text()
                    procent_alcool = self.edit.procent_alcool_3.text()
                    cantitate = self.edit.cantitate_zahar_3.text()
                    culoare = self.edit.culoare_3.text()
                    aspect_gustativ = self.edit.aspect_gustativ.text()
                    aspect_vizual = self.edit.aspect_vizual.text()
                    aspect_olfactiv = self.edit.aspect_olfactiv.text()
                    temperatura = self.edit.temperatura_servire.text()
                    timp_decantare = self.edit.timp_decantare.text()
                    recipient = self.edit.recipient_3.text()
                    volum = self.edit.volum_recipient_2.text()
                    numar_unitati = self.edit.numar_unitati_3.text()
                    pret = self.edit.pret_3.text()
                    an_productie = self.edit.an_productie.text()
                    timp_pastrare = self.edit.timp_pastrare.text()
                    descriere = self.edit.descriere_3.toPlainText()
                    ID_current = raw[1][0]
                    cursor.execute(
                        '''UPDATE vin_denumire_origine_controlata 
                        SET denumire_OC=%s,soi_struguri=%s, tara_origine = %s,regiune_producere = %s, producator = %s, 
                        proces_cultura_si_vinificare = %s, treapta_calitate =%s, procent_alcool = %s, 
                        cantitate_zahar = %s,culoare = %s, aspect_gustativ = %s, aspect_olfactiv = %s, 
                        aspect_vizual =%s, temperatura_servire =%s, decantare =%s, recipient = %s, 
                        volum_recipient = %s, numar_unitati = %s, pret = %s,an_productie = %s, timp_pastrare = %s, descriere = %s
                        WHERE id_vin_denumire_origine_controlata = %s ''', (denumire, soi, tara,regiune, producator, proces,treapta_calitate, procent_alcool, cantitate, culoare,aspect_gustativ,aspect_olfactiv,aspect_vizual,temperatura,timp_decantare, recipient, volum, numar_unitati, pret, an_productie, timp_pastrare, descriere, ID_current))
                    self.con_db.commit()
                    self.load_database_3()
                    self.statusbar.showMessage("Produsul a fost modificat cu succes in baza de date")
        except Exception as eroare:
            self.con_db.rollback()
            print(eroare)
            self.statusbar.showMessage("Eroare la modificarea produsului din baza de date")

    #Functia de mai jos adauga in baza de date vin de masa, se citeste din casutele corespunzatoare ferestrei de
    #adaugare in baza de date iar acele date vor fi transmise catre baza de date
    #La final se afiseaza in bara de status mesajul corespunzator
    def Add_Data_1(self):
        try:
            cursor = self.con_db.cursor()
            cursor.execute("INSERT INTO vin_de_masa (denumire, soi_struguri, tara_origine,producator, procent_alcool,cantitate_zahar, culoare, recipient, volum_recipient, numar_unitati, pret, an_productie, timp_pastrare, descriere)"
                           "VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (''.join(self.adding.denumire.text()),
                                                                                                 ''.join(self.adding.soi_struguri.text()),
                                                                                                 ''.join(self.adding.tara_origine.text()),
                                                                                                 ''.join(self.adding.producator.text()),
                                                                                                 ''.join(self.adding.procent_alcool.text()),
                                                                                                 ''.join(self.adding.cantitate_zahar.text()),
                                                                                                 ''.join(self.adding.culoare.text()),
                                                                                                 ''.join(self.adding.recipient.text()),
                                                                                                 ''.join(self.adding.volum_recipient.text()),
                                                                                                 ''.join(self.adding.numar_unitati.text()),
                                                                                                 ''.join(self.adding.pret.text()),
                                                                                                 ''.join(self.adding.an_productie.text()),
                                                                                                 ''.join(self.adding.timp_pastrare.text()),
                                                                                                 ''.join(self.adding.descriere.toPlainText())))
            self.con_db.commit()
            self.load_database()
            self.statusbar.showMessage("Produsul a fost adaugat cu succes in baza de date")
        except Exception as eroare:
            self.con_db.rollback()
            print(eroare)
            self.statusbar.showMessage("Eroare la adaugarea produsului in baza de date")

    # Functia de mai jos adauga in baza de date vin indicatie geografica, se citeste din casutele corespunzatoare ferestrei de
    # adaugare in baza de date iar acele date vor fi transmise catre baza de date
    # La final se afiseaza in bara de status mesajul corespunzator
    def add_data_2(self):
        try:
            cursor = self.con_db.cursor()
            cursor.execute("INSERT INTO vin_indicatie_geografica (denumire_generica, soi_struguri, tara_origine,zona_geografica, producator, procent_alcool,cantitate_zahar, culoare, recipient, volum_recipient, numar_unitati, pret, an_productie, timp_pastrare, descriere)"
                           "VALUES('%s','%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (''.join(self.adding2.denumire_generica_2.text()),
                                                                                                 ''.join(self.adding2.soi_struguri_4.text()),
                                                                                                 ''.join(self.adding2.tara_origine_4.text()),
                                                                                                 ''.join(self.adding2.zona_geografica_2.text()),
                                                                                                 ''.join(self.adding2.producator_4.text()),
                                                                                                 ''.join(self.adding2.procent_alcool_4.text()),
                                                                                                 ''.join(self.adding2.cantitate_zahar_4.text()),
                                                                                                 ''.join(self.adding2.culoare_4.text()),
                                                                                                 ''.join(self.adding2.recipient_4.text()),
                                                                                                 ''.join(self.adding2.volum_2.text()),
                                                                                                 ''.join(self.adding2.numar_unitati_4.text()),
                                                                                                 ''.join(self.adding2.pret_4.text()),
                                                                                                 ''.join(self.adding2.an_productie.text()),
                                                                                                 ''.join(self.adding2.timp_pastrare.text()),
                                                                                                 ''.join(self.adding2.descriere_4.toPlainText())))

            self.con_db.commit()
            self.load_database_2()
            self.statusbar.showMessage("Produsul a fost adaugat cu succes in baza de date")
        except Exception as eroare:
            self.con_db.rollback()
            print(eroare)
            self.statusbar.showMessage("Eroare la adaugarea produsului in baza de date")

    # Functia de mai jos adauga in baza de date vin DOC, se citeste din casutele corespunzatoare ferestrei de
    # adaugare in baza de date iar acele date vor fi transmise catre baza de date
    # La final se afiseaza in bara de status mesajul corespunzator
    def add_data_3(self):
        try:
            cursor = self.con_db.cursor()
            denumire = self.adding2.denumire_oc.text()
            soi = self.adding2.soi_struguri_3.text()
            tara = self.adding2.tara_origine_3.text()
            regiune = self.adding2.regiune.text()
            producator = self.adding2.producator_3.text()
            proces = self.adding2.proces_producere.text()
            treapta_calitate = self.adding2.treapta_calitate.text()
            procent_alcool = self.adding2.procent_alcool_3.text()
            cantitate = self.adding2.cantitate_zahar_3.text()
            culoare = self.adding2.culoare_3.text()
            aspect_gustativ = self.adding2.aspect_gustativ.text()
            aspect_vizual = self.adding2.aspect_vizual.text()
            aspect_olfactiv = self.adding2.aspect_olfactiv.text()
            temperatura = self.adding2.temperatura_servire.text()
            timp_decantare = self.adding2.timp_decantare.text()
            recipient = self.adding2.recipient_3.text()
            volum = self.adding2.volum_recipient_2.text()
            numar_unitati = self.adding2.numar_unitati_3.text()
            pret = self.adding2.pret_3.text()
            an_productie = self.adding2.an_productie.text()
            timp_pastrare = self.adding2.timp_pastrare.text()
            descriere = self.adding2.descriere_3.toPlainText()
            cursor.execute(
                '''INSERT INTO vin_denumire_origine_controlata(denumire_OC, soi_struguri, tara_origine, regiune_producere,producator, proces_cultura_si_vinificare, treapta_calitate, procent_alcool, cantitate_zahar, culoare, aspect_gustativ, aspect_olfactiv, aspect_vizual, temperatura_servire, decantare, recipient, volum_recipient, numar_unitati, pret, an_productie, timp_pastrare, descriere)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s)''',
                (denumire, soi, tara, regiune, producator, proces, treapta_calitate, procent_alcool, cantitate, culoare,aspect_gustativ, aspect_olfactiv, aspect_vizual, temperatura, timp_decantare, recipient, volum,numar_unitati, pret, an_productie, timp_pastrare, descriere))
            self.con_db.commit()
            self.load_database_3()
            self.statusbar.showMessage("Produsul a fost adaugat cu succes in baza de date")
        except Exception as eroare:
            self.con_db.rollback()
            print(eroare)
            self.statusbar.showMessage("Eroare la adaugarea produsului in baza de date")

    #Functia de mai jos incarca din baza de date toate vinurile de masa
    def load_database(self):
        try:
            self.tableWidget.hideColumn(0)
            while self.tableWidget.rowCount() > 0:
                self.tableWidget.removeRow(0)
            query = 'SELECT * FROM vin_de_masa'
            cursor = self.con_db.cursor()
            cursor.execute(query)


            for raw_index, raw_data in enumerate(cursor):
                self.tableWidget.insertRow(raw_index)
                for colm_index, col_data in enumerate(raw_data):
                    if colm_index != 0:
                        self.tableWidget.setItem(raw_index, colm_index, QTableWidgetItem(str(col_data)))

        except:
            self.statusbar.showMessage("Eroare la afisarea vinurilor de masa")

    #Functia de mai jos incarca din baza de date toate vinurile cu indicatie geografica
    def load_database_2(self):
        try:
            self.tableWidget_2.hideColumn(0)
            while self.tableWidget_2.rowCount() > 0:
                self.tableWidget_2.removeRow(0)
            query = 'SELECT * FROM vin_indicatie_geografica'
            cursor = self.con_db.cursor()
            cursor.execute(query)


            for raw_index, raw_data in enumerate(cursor):
                self.tableWidget_2.insertRow(raw_index)
                for colm_index, col_data in enumerate(raw_data):
                    if colm_index != 0:
                        self.tableWidget_2.setItem(raw_index, colm_index, QTableWidgetItem(str(col_data)))

        except:
            self.statusbar.showMessage("Eroare la afisarea vinurilor cu indicatie geografica")

    #functia de mai jos incarca din baza de date toate vinurile DOC
    def load_database_3(self):
        try:
            self.tableWidget_3.hideColumn(0)
            while self.tableWidget_3.rowCount() > 0:
                self.tableWidget_3.removeRow(0)
            query = 'SELECT * FROM vin_denumire_origine_controlata'
            cursor = self.con_db.cursor()
            cursor.execute(query)


            for raw_index, raw_data in enumerate(cursor):
                self.tableWidget_3.insertRow(raw_index)
                for colm_index, col_data in enumerate(raw_data):
                    if colm_index != 0:
                        self.tableWidget_3.setItem(raw_index, colm_index, QTableWidgetItem(str(col_data)))

        except:
            self.statusbar.showMessage("Eroare la afisarea vinurilor cu indicatie geografica")


    #Functia de mai jos realizeaza conexiunea cu baza de date
    def connect_db(self):
        try:
            user = self.lineEdit.text()
            pwd = self.lineEdit_2.text()
            host = self.lineEdit_3.text()
            port = self.lineEdit_4.text()
            db_name = self.lineEdit_5.text()
            self.con_db = mysql.connector.connect(user=user, password=pwd, host=host, port=port, database=db_name)
            self.statusbar.showMessage("Connected to DB")
            self.show_database_stats()
        except mysql.connector.Error as err:
            self.statusbar.showMessage("Error connecting to DB")


    #Afisarea detaliilor despre baza de date, dupa ce a fost stabilita conexiunea catre aceasta
    def show_database_stats(self):
        try:
            cursor = self.con_db.cursor()
            stm = "SELECT table_name, table_rows" \
                  " FROM INFORMATION_SCHEMA.TABLES " \
                  "WHERE TABLE_SCHEMA = 'ferma_viticola'"
            cursor.execute(stm)
            while self.tableWidget_4.rowCount() > 0:
                self.tableWidget_4.removeRow(0)

            for raw_index, raw_data in enumerate(cursor):
                self.tableWidget_4.insertRow(raw_index)
                for colm_index, col_data in enumerate(raw_data):
                    self.tableWidget_4.setItem(raw_index, colm_index, QTableWidgetItem(str(col_data)))
        except:
            self.statusbar.showMessage("Eroare la afisarea statisticilor bazei de date")

    #Functia de mai jos realizezaza afisarea comenzilor
    def show_comenzi(self):
        try:
            self.tableWidget_5.hideColumn(0)
            cursor = self.con_db.cursor()
            stm = "SELECT * FROM comanda"
            cursor.execute(stm)
            while self.tableWidget_5.rowCount() > 0:
                self.tableWidget_5.removeRow(0)

            rezultat = cursor.fetchall()

            #Se parcurg toate comenzile, pentru fiecare in parte de afiseaza detaliile dorite
            for raw_index, raw_data in enumerate(rezultat):
                self.tableWidget_5.insertRow(raw_index)
                for colm_index, col_data in enumerate(raw_data):
                    if(colm_index == 0):
                        id_comanda = int(col_data)
                    elif(colm_index == 1):
                        cursor.execute("SELECT nume,prenume FROM user WHERE id_user= %(id)s", {'id': col_data})
                        id_user = col_data
                        rez = cursor.fetchall()
                        self.tableWidget_5.setItem(raw_index, colm_index, QTableWidgetItem(rez[0][0] + " " + rez[0][1]))
                    elif(colm_index == 2):
                        cursor.execute("SELECT * FROM user WHERE id_user = %(id)s", {'id': id_user})
                        adresa = cursor.fetchall()
                        print_adresa =  adresa[0][6] + " " + adresa[0][7] + " " + adresa[0][8] + " " + adresa[0][9] + " " + str(adresa[0][10])
                        self.tableWidget_5.setItem(raw_index, colm_index, QTableWidgetItem(print_adresa))
                        self.tableWidget_5.setItem(raw_index, colm_index + 1, QTableWidgetItem(str(col_data)))
                    elif(colm_index == 3):
                        self.tableWidget_5.setItem(raw_index, colm_index + 3, QTableWidgetItem(str(col_data)))
                        cursor.execute("SELECT * FROM comanda_vin WHERE id_comanda=%(id)s", {'id': id_comanda})
                        rez = cursor.fetchall()
                        numar_produse = 0
                        for numarul_produsului_curent,detalii in enumerate(rez):
                            numar_produse = numar_produse + detalii[6]
                        self.tableWidget_5.setItem(raw_index, colm_index + 1, QTableWidgetItem(str(numar_produse)))
                    else:
                      self.tableWidget_5.setItem(raw_index, colm_index, QTableWidgetItem(str(col_data)))

                suma = 0
                cursor.execute(
                    "SELECT pret, cantitate FROM vin_de_masa A, comanda_vin B, comanda C WHERE A.id_vin_masa = B.id_vin_masa AND C.id_comanda=B.id_comanda AND C.id_comanda=%(id)s", {'id': id_comanda})
                rez = cursor.fetchall()
                for nr, pret in enumerate(rez):
                    suma = suma + pret[0]*pret[1]
                cursor.execute(
                    "SELECT pret, cantitate FROM vin_indicatie_geografica A, comanda_vin B, comanda C WHERE A.id_vin_indicatie_geografica = B.id_vin_IG AND C.id_comanda=B.id_comanda AND C.id_comanda=%(id)s",
                    {'id': id_comanda})
                rez = cursor.fetchall()
                for nr, pret in enumerate(rez):
                    suma = suma + pret[0]*pret[1]
                cursor.execute(
                    "SELECT pret, cantitate FROM vin_denumire_origine_controlata A, comanda_vin B, comanda C WHERE A.id_vin_denumire_origine_controlata = B.id_vin_DOC AND C.id_comanda=B.id_comanda AND C.id_comanda=%(id)s",
                    {'id': id_comanda})
                rez = cursor.fetchall()
                for nr, pret in enumerate(rez):
                    suma = suma + pret[0]*pret[1]
                self.tableWidget_5.setItem(raw_index, 5, QTableWidgetItem(str(suma)))

        except Exception as error:
            print(error)
            self.statusbar.showMessage("Eroare la afisarea comenzilor")



    def interogare_simpla_1(self):
        self.listWidget.clear()
        #Afisati toate persoanele care au comandat vinul DOC numit 'Pomerol'
        cursor = self.con_db.cursor()
        cursor.execute('''SELECT CONCAT(C.Nume,' ',C.Prenume) as client
        FROM user C INNER JOIN Comanda com ON (C.id_user = com.id_user) INNER JOIN comanda_vin cv ON (com.id_comanda = cv.id_comanda) INNER JOIN vin_denumire_origine_controlata doc ON (doc.id_vin_denumire_origine_controlata = cv.id_vin_DOC)
        WHERE doc.denumire_OC = 'Pomerol'
        ''')
        rezultat = cursor.fetchall()
        for raw_index, raw_data in enumerate(rezultat):
            for colm_index, col_data in enumerate(raw_data):
                self.listWidget.addItem(col_data)

    def interogare_simpla_2(self):
        self.listWidget_2.clear()
        #Afisati toate vinurile de masa comandate in anul 2018
        cursor = self.con_db.cursor()
        cursor.execute('''SELECT DISTINCT  V.Denumire
        FROM vin_de_masa V INNER JOIN comanda_vin CV ON (V.id_vin_masa = CV.id_vin_masa) INNER JOIN comanda C ON (C.id_comanda = CV.id_comanda)
        WHERE year(C.data) = 2018 ''')
        rezultat = cursor.fetchall()
        for raw_index, raw_data in enumerate(rezultat):
            for colm_index, col_data in enumerate(raw_data):
                self.listWidget_2.addItem(col_data)
    def interogare_simpla_3(self):
        self.listWidget_3.clear()
        #Afisati toate vinurile de culoare rosie comandate de clientul Margineanu
        cursor = self.con_db.cursor()
        cursor.execute('''SELECT V.denumire
        FROM vin_de_masa V INNER JOIN comanda_vin cm ON (cm.id_vin_masa = V.id_vin_masa) INNER JOIN comanda c ON (c.id_comanda = cm.id_comanda) INNER JOIN user u ON (u.id_user = c.id_user)
        WHERE u.nume = 'Margineanu' AND V.culoare = 'rosu'
        UNION
        SELECT V.denumire_generica
        FROM vin_indicatie_geografica V INNER JOIN comanda_vin cm ON (cm.id_vin_IG = V.id_vin_indicatie_geografica) INNER JOIN comanda c ON (c.id_comanda = cm.id_comanda) INNER JOIN user u ON (u.id_user = c.id_user)
        WHERE u.nume = 'Margineanu' AND V.culoare = 'rosu'
        UNION
        SELECT V.denumire_OC
        FROM vin_denumire_origine_controlata V INNER JOIN comanda_vin cm ON (cm.id_vin_DOC = V.id_vin_denumire_origine_controlata) INNER JOIN comanda c ON (c.id_comanda = cm.id_comanda) INNER JOIN user u ON (u.id_user = c.id_user)
        WHERE u.nume = 'Margineanu' AND V.culoare = 'rosu' ''')
        rezultat = cursor.fetchall()
        for raw_index, raw_data in enumerate(rezultat):
            for colm_index, col_data in enumerate(raw_data):
                self.listWidget_3.addItem(col_data)


    def interogare_simpla_4(self):
        self.listWidget_4.clear()
        #Afisati numarul de tipuri de vin si pretul mediu pentru fiecare categorie de vin, vinurile trebuie sa fie continute in cel putin o comanda
        cursor = self.con_db.cursor()
        cursor.execute('''SELECT CONCAT(COUNT(V.id_vin_masa),' ', AVG(V.pret))
         FROM vin_de_masa V INNER JOIN comanda_vin CV ON (CV.id_vin_masa = V.id_vin_masa)
         UNION
         SELECT CONCAT(COUNT(V.id_vin_indicatie_geografica),' ', AVG(V.pret))
         FROM vin_indicatie_geografica V INNER JOIN comanda_vin CV ON (CV.id_vin_IG = V.id_vin_indicatie_geografica)
         UNION
         SELECT CONCAT(COUNT(V.id_vin_denumire_origine_controlata),' ', AVG(V.pret))
         FROM vin_denumire_origine_controlata V INNER JOIN comanda_vin CV ON (CV.id_vin_DOC = V.id_vin_denumire_origine_controlata)''')
        rezultat = cursor.fetchall()
        for raw_index, raw_data in enumerate(rezultat):
            for colm_index, col_data in enumerate(raw_data):
                self.listWidget_4.addItem(str(col_data))

    def interogare_simpla_5(self):
        self.listWidget_6.clear()
        #Afisati cel mai comandat tip de vin, numarul de comenzi in care apare si numarul de unitati comandate si pretul total din fiecare categorie
        cursor = self.con_db.cursor()
        cursor.execute('''
        (SELECT CONCAT(V.denumire,' ', COUNT(CV.id_vin_masa),' ',SUM(CV.cantitate),' ', SUM(CV.cantitate) * V.pret)
        FROM vin_de_masa V INNER JOIN comanda_vin CV ON (V.id_vin_masa = CV.id_vin_masa)
        GROUP BY CV.id_vin_masa
        ORDER BY SUM(CV.cantitate) DESC
        LIMIT 1 )
        
        UNION 
        
        (SELECT CONCAT(V.denumire_generica,' ', COUNT(CV.id_vin_IG),' ', SUM(CV.cantitate), ' ',SUM(CV.cantitate) * V.pret)
        FROM vin_indicatie_geografica V INNER JOIN comanda_vin CV ON (V.id_vin_indicatie_geografica = CV.id_vin_IG)
        GROUP BY CV.id_vin_IG
        ORDER BY SUM(CV.cantitate) DESC
        LIMIT 1)
        
        UNION
        
        (SELECT CONCAT(V.denumire_OC,' ', COUNT(CV.id_vin_DOC),' ',SUM(CV.cantitate),' ', SUM(CV.cantitate) * V.pret)
        FROM vin_denumire_origine_controlata V INNER JOIN comanda_vin CV ON (V.id_vin_denumire_origine_controlata = CV.id_vin_DOC)
        GROUP BY CV.id_vin_DOC
        ORDER BY SUM(CV.cantitate) DESC
        LIMIT 1)''')

        rezultat = cursor.fetchall()
        for raw_index, raw_data in enumerate(rezultat):
            for colm_index, col_data in enumerate(raw_data):
                self.listWidget_6.addItem(str(col_data))
    def interogare_simpla_6(self):
        self.listWidget_5.clear()
        #Afisati toate vinurile de tip DOC comandate de culoare rosu ale caror numar de unitati din stoc este mai mare de 50.
        cursor = self.con_db.cursor()
        cursor.execute('''SELECT DISTINCT V.denumire_OC
        FROM vin_denumire_origine_controlata V INNER JOIN comanda_vin cv ON (V.id_vin_denumire_origine_controlata = cv.id_vin_IG)
        WHERE (V.culoare = 'rosu') AND (V.numar_unitati >= 50)''')
        rezultat = cursor.fetchall()
        for raw_index, raw_data in enumerate(rezultat):
            for colm_index, col_data in enumerate(raw_data):
                self.listWidget_5.addItem(str(col_data))

    def interogare_complexa_1(self):
        self.listWidget_7.clear()
        #Afisati numele si pretul tuturor vinurilor din fiecare categorie a caror pret este mai mare decat pretul mediu al tuturor vinurilor
        cursor = self.con_db.cursor()
        cursor.execute('''SELECT CONCAT(V.denumire,' ', V.pret)
        FROM vin_de_masa V
        WHERE V.pret > (SELECT (AVG(V1.pret)+AVG(V2.pret)+AVG(V3.pret))/3
                        FROM vin_de_masa V1, vin_indicatie_geografica V2, vin_denumire_origine_controlata V3)
        
        UNION
        
        SELECT CONCAT(V.denumire_generica,' ', V.pret)
        FROM vin_indicatie_geografica V
        WHERE V.pret > (SELECT (AVG(V1.pret)+AVG(V2.pret)+AVG(V3.pret))/3
                        FROM vin_de_masa V1, vin_indicatie_geografica V2, vin_denumire_origine_controlata V3)
        UNION
        
        SELECT CONCAT(V.denumire_OC,' ', V.pret)
        FROM vin_denumire_origine_controlata V
        WHERE V.pret > (SELECT (AVG(V1.pret)+AVG(V2.pret)+AVG(V3.pret))/3
                        FROM vin_de_masa V1, vin_indicatie_geografica V2, vin_denumire_origine_controlata V3)''')
        rezultat = cursor.fetchall()
        for raw_index, raw_data in enumerate(rezultat):
            for colm_index, col_data in enumerate(raw_data):
                self.listWidget_7.addItem(str(col_data))

    def interogare_complexa_2(self):
        self.listWidget_8.clear()
        #Afisati lista tuturor vinurilor care nu au fost comandate niciodata
        cursor = self.con_db.cursor()
        cursor.execute('''SELECT V.denumire
        FROM vin_de_masa V
        WHERE V.id_vin_masa NOT IN (SELECT A.id_vin_masa
                                FROM vin_de_masa A INNER JOIN comanda_vin cv ON (A.id_vin_masa = cv.id_vin_masa))
        UNION
        SELECT V.denumire_generica
        FROM vin_indicatie_geografica V
        WHERE V.id_vin_indicatie_geografica NOT IN (SELECT A.id_vin_indicatie_geografica
                                FROM vin_indicatie_geografica A INNER JOIN comanda_vin cv ON (A.id_vin_indicatie_geografica = cv.id_vin_IG))
                                
        UNION
        SELECT V.denumire_OC
        FROM vin_denumire_origine_controlata V
        WHERE V.id_vin_denumire_origine_controlata NOT IN (SELECT A.id_vin_denumire_origine_controlata
                        FROM vin_denumire_origine_controlata A INNER JOIN comanda_vin cv ON (A.id_vin_denumire_origine_controlata = cv.id_vin_DOC))''')
        rezultat = cursor.fetchall()
        for raw_index, raw_data in enumerate(rezultat):
            for colm_index, col_data in enumerate(raw_data):
                self.listWidget_8.addItem(str(col_data))

    def interogare_complexa_3(self):
        self.listWidget_9.clear()
        #Afisati vinurile comandate din categoria DOC ale caror cantitate este mai mare decat media stocului tuturor vinurilor din acea categorie
        cursor = self.con_db.cursor()
        cursor.execute('''SELECT V.denumire_OC
        FROM vin_denumire_origine_controlata V INNER JOIN comanda_vin cv ON (V.id_vin_denumire_origine_controlata = cv.id_vin_DOC)
        WHERE V.numar_unitati > (SELECT AVG(v2.numar_unitati) 
                                FROM vin_denumire_origine_controlata v2)''')
        rezultat = cursor.fetchall()
        for raw_index, raw_data in enumerate(rezultat):
            for colm_index, col_data in enumerate(raw_data):
                self.listWidget_9.addItem(str(col_data))

    def interogare_complexa_4(self):
        self.listWidget_10.clear()
        #Afisati numele, numarul de unitati si pretul vinurilor din categoria vinurilor de masa produse din anul in care este produs cel mai vechi vin DOC
        cursor = self.con_db.cursor()
        cursor.execute('''SELECT CONCAT(v.denumire,' ', v.numar_unitati,' ', v.pret)
        FROM vin_de_masa v
        WHERE v.an_productie = (SELECT a.an_productie
                                FROM vin_denumire_origine_controlata a
                                ORDER BY a.an_productie ASC
                                LIMIT 1)''')
        rezultat = cursor.fetchall()
        for raw_index, raw_data in enumerate(rezultat):
            for colm_index, col_data in enumerate(raw_data):
                self.listWidget_10.addItem(str(col_data))

#Clasele de mai jos sunt clasele ce contin ferestrele de dialog de adaugare, editare de produse si de verificare a comenzii
class AddDialog_1(QDialog, add_vin_masa.Ui_Dialog):
    def __init__(self, parent=None):
        super(AddDialog_1, self).__init__(parent)
        self.setupUi(self)

class AddDialog_2(QDialog, add_vin_regiune.Ui_Dialog):
    def __init__(self, parent = None):
        super(AddDialog_2, self).__init__(parent)
        self.setupUi(self)

class AddDialog_3(QDialog, add_vin_DOC.Ui_Dialog):
    def __init__(self, parent = None):
        super(AddDialog_3, self).__init__(parent)
        self.setupUi(self)


class EditDialog_1(QDialog, edit_vin_masa.Ui_Dialog):
    def __init__(self, parent=None):
        super(EditDialog_1, self).__init__(parent)
        self.setupUi(self)


class EditDialog_2(QDialog, edit_vin_regiune.Ui_Dialog):
    def __init__(self, parent=None):
        super(EditDialog_2, self).__init__(parent)
        self.setupUi(self)


class EditDialog_3(QDialog, edit_vin_DOC.Ui_Dialog):
    def __init__(self, parent=None):
        super(EditDialog_3, self).__init__(parent)
        self.setupUi(self)

class Dialog_verifica_comanda(QDialog, verifica_comanda.Ui_Dialog):
    def __init__(self, parent=None):
        super(Dialog_verifica_comanda, self).__init__(parent)
        self.setupUi(self)


sys._excepthook = sys.excepthook
def exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)
sys.excepthook = exception_hook

app = QApplication([])
win = MainApp()
win.setWindowIcon(QtGui.QIcon('ferma.png'))
app.setStyle('Fusion')
app.exec_()