import time
import flet as ft
import model as md

class SpellChecker:

    def __init__(self, view):
        self._multiDic = md.MultiDictionary()
        self._view = view


    def handleSpellCheck(self, txtIn, language, modality):
        if not (language == "english" or language == "italian" or language == "spanish"):
            self._view.lv.controls.append(ft.Text(value="Errore: non hai selezionato una lingua", color="red"))
            self._view.page.add(self._view.lv)
            return
        if not (modality == "Default" or modality == "Linear" or modality == "Dichotomic"):
            self._view.lv.controls.append(ft.Text(value="Errore: non hai selezionato una modalità di ricerca", color="red"))
            self._view.page.add(self._view.lv)
            return
        if txtIn == "":
            self._view.lv.controls.append(ft.Text(value="Errore: non hai inserito una frase", color="red"))
            self._view.page.add(self._view.lv)
            return
        self._view.lv.controls.append(ft.Text(value=f"Frase inserita: {txtIn}"))
        self._view.page.add(self._view.lv)
        if self.handleSentence(txtIn, language, modality) != None:
            paroleErrate, tempo = self.handleSentence(txtIn, language, modality)
            self._view.lv.controls.append(ft.Text(value=f"Parole errate: {paroleErrate}", color="green"))
            self._view.lv.controls.append(ft.Text(value=f"Tempo richiesto dalla ricerca: {tempo}", color="green"))
            self._view.frase.value = ""
            self._view.page.add(self._view.lv)

    def handleSentence(self, txtIn, language, modality):
        txtIn = replaceChars(txtIn.lower())

        words = txtIn.split()
        paroleErrate = " - "

        match modality:
            case "Default":
                t1 = time.time()
                parole = self._multiDic.searchWord(words, language)
                for parola in parole:
                    if not parola.corretta:
                        paroleErrate = paroleErrate + str(parola) + " - "
                t2 = time.time()
                return paroleErrate, t2 - t1

            case "Linear":
                t1 = time.time()
                parole = self._multiDic.searchWordLinear(words, language)
                for parola in parole:
                    if not parola.corretta:
                        paroleErrate = paroleErrate + str(parola) + " "
                t2 = time.time()
                return paroleErrate, t2 - t1

            case "Dichotomic":
                t1 = time.time()
                parole = self._multiDic.searchWordDichotomic(words, language)
                for parola in parole:
                    if not parola.corretta:
                        paroleErrate = paroleErrate + str(parola) + " - "
                t2 = time.time()
                return paroleErrate, t2 - t1
            case _:
                return None


    def printMenu(self):
        print("______________________________\n" +
              "      SpellChecker 101\n"+
              "______________________________\n " +
              "Seleziona la lingua desiderata\n"
              "1. Italiano\n" +
              "2. Inglese\n" +
              "3. Spagnolo\n" +
              "4. Exit\n" +
              "______________________________\n")


def replaceChars(text):
    chars = "\\`*_{}[]()>#+-.!$?%^;,=_~"
    for c in chars:
        text = text.replace(c, "")
    return text
