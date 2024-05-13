# TIE-02101 Johdatus ohjelmointiin
# Ellinoora Vikman, 291597, ellinoora.vikman@tuni.fi
# Bussimaksulaskin, Graafisen käyttöliittymän yksinkertainen projektitehtävä 13.10:

# Bussilippujen ostopalvelu, joka laskee käyttäjän haluaminen
# lippujen kokonaissumman, pyytää maksutavan sekä käsittelee
# mahdolliset virhetilanteet

from tkinter import *

# Luodaan matkojen hinnat eri lipputyypeille
ADULT_PRICE = 3.50
CHILD_PRICE = 1.20
STUDENT_PRICE = 1.90
PENSIONER_PRICE = 2.50


class TicketShop:

    def __init__(self):
        """ Rakentaja-metodi, määrittelee käyttöliittymän
        tekstikenttiä, Entry-komponentteja ja painonappeja
        """
        self.__mainwindow = Tk()
        self.__mainwindow.title("Bus ticket shop")
        # Eri lipputyyppien tekstikentät
        self.__adults_text = Label(self.__mainwindow, text="Adults / 3.50 e :")
        self.__children_text = Label(self.__mainwindow, text="Children / 1.20 e :")
        self.__students_text = Label(self.__mainwindow, text="Students / 1.90 e :")
        self.__pensioners_text = Label(self.__mainwindow, text="Pensioners / 2.50 e :")
        # Lipputyyppien entry-komponentit
        self.__adults = Entry()
        self.__children = Entry()
        self.__students = Entry()
        self.__pensioners = Entry()

        self.__InfoLabel = Label(self.__mainwindow, text="Welcome to the online  ticket shop! \n"
                                                         "Here you can buy tickets for bus trips inside \n"
                                                         "of Tampere. Input the number of tickets you want \n"
                                                         "to buy to the fields below. Every field must \n"
                                                         "include something. \n"
                                                         "\n"
                                                         "Over 20 euros' orders we'll give 20 % discount. \n")
        # Tekstikenttä, joka ilmestyy, jos maksu on onnistunut
        self.__success_label = Label(self.__mainwindow, text="")
        self.__success_label.grid(row=10, column=1)
        # Tekstikenttä, joho tulostuu matkan kokonaishinta
        self.__result_text = Label(self.__mainwindow)
        # Tekstikenttä virheilmoituksia ym selityksiä varten
        self.__explanation_text = Label(self.__mainwindow)

        # Määritellään käyttöliittymän painonapit
        self.__calculate_button = Button(self.__mainwindow, text="calculate",
                                         background="white", foreground="blue", command=self.calculate_trip)

        self.__stop_button = Button(self.__mainwindow, text="Close",
                                    background="white", foreground="blue", command=self.stop)

        self.__reset_button = Button(self.__mainwindow, text="reset",
                                     background="white", foreground="blue", command=self.initialize_calculator)

        self.__price_list_button = Button(self.__mainwindow, text="reset",
                                          background="white", foreground="blue", command=self.initialize_calculator)
        # Muuttuja, jonka avulla lukitaan maksutapanapit, jos liittymä alustetaan
        self.__tester = False

        self.initialize_calculator()

    def initialize_calculator(self):
        """ Alustaa käyttöliittymän, kun painetaan 'reset' - nappia
        :return: none
        """
        self.__adults = Entry()
        self.__children = Entry()
        self.__students = Entry()
        self.__pensioners = Entry()

        self.__result_text.configure(text="")
        self.__explanation_text.configure(text="")

        self.__success_label.configure(text="")

        self.__calculate_button.configure(state=NORMAL)

        # Jos maksutapanapit on jo luotu 'calculate' - nappia painamalla, ne lukitaan
        if self.__tester is True:
            self.__card_button.configure(state=DISABLED)
            self.__cash_button.configure(state=DISABLED)

        self.make_grids()

    def make_grids(self):
        """ Sijoittaa käyttöliittymän komponentit oikeille paikoille grid - metodin avulla
        :return: none
        """
        self.__adults_text.grid(row=1, column=0)
        self.__children_text.grid(row=2, column=0)
        self.__students_text.grid(row=3, column=0)
        self.__pensioners_text.grid(row=4, column=0)
        self.__adults.grid(row=1, column=1)
        self.__children.grid(row=2, column=1)
        self.__students.grid(row=3, column=1)
        self.__pensioners.grid(row=4, column=1)
        self.__calculate_button.grid(row=7, column=0, sticky=E)
        self.__stop_button.grid(row=7, column=2, sticky=W)
        self.__result_text.grid(row=6, column=1)
        self.__explanation_text.grid(row=8, column=1)
        self.__InfoLabel.grid(row=0, column=1)
        self.__reset_button.grid(row=7, column=1)

    def entry_checker(self):
        """ Testaa sitä, onko kaikkiin syötekenttiin täytetty jotain ja jos ei,
        tulostaa virheilmoituksen metodia kutsuttaessa
        :return: none
        """
        # Muuttuja, joka säilyttää tiedon siitä, onko siirrytty expect-osioon
        self.__i = True
        try:
            if self.__adults.get() == "" or self.__children.get() == "" \
                    or self.__students.get() == "" or self.__pensioners.get() == "":
                raise ValueError
            else:
                self.__i = True
        except ValueError:
            self.__explanation_text.configure(text="Fill all fields above. "
                                                   "If you don't want a ticket, input 0. \n"
                                                   "Put 'reset' to continue.")
            self.__i = False

    def calculate_trip(self):
        """ Laskee matkan kokonaishinnan
        :return: none
        """

        self.entry_checker()

        if self.__i is True:
            try:
                adults = int(self.__adults.get())
                children = int(self.__children.get())
                students = int(self.__students.get())
                pensioners = int(self.__pensioners.get())

                try:
                    if adults < 0 or children < 0 or students < 0 or pensioners < 0:
                        raise ValueError

                    total_price = adults * ADULT_PRICE + children * CHILD_PRICE + \
                                  students * STUDENT_PRICE + pensioners * PENSIONER_PRICE
                    self.__result_text.configure(text="Total price is {:0.2f}".format(total_price))

                    if 0 < total_price < 20:
                        self.__explanation_text.configure(text="Choose the payment option")
                        self.payment_option()
                    elif total_price == 0:
                        self.__explanation_text.configure(text="The trip doesn't cost anything. \n"
                                                               "Put 'reset' to continue.")
                    else:
                        new_price = 0.8 * total_price
                        self.__explanation_text.configure(text="Your order costs more than 20 euros,\n"
                                                               " so you get 20 % discount. \n"
                                                               "\n"
                                                               "New price is {:0.2f} \n"
                                                               "\n"
                                                               "Choose the payment option: ".format(new_price))
                        self.payment_option()

                except ValueError:
                    self.__explanation_text.configure(text="Number of tickets must be positive. \n"
                                                           "Put 'reset' to continue.")

            except ValueError:
                self.__explanation_text.configure(text="Number of tickets must be integers. \n"
                                                       "Put 'reset' to continue.")

        # Calculate - nappi lukitaan käytön jälkeen, jonka jälkeen käyttäjän on painettava 'reset' jatkaakseen
        self.__calculate_button.configure(state=DISABLED)

    def payment_option(self):
        """ Luo hinnan laskemisen jälkeen uudet napit maksutavan valitsemista varten
        :return: none
        """
        self.__tester = True

        self.__cash_button = Button(self.__mainwindow, text="CASH",
                             background="red", foreground="white", command=self.payment_success, state=NORMAL)
        self.__cash_button.grid(row=9, column=1, sticky=W)
        self.__card_button = Button(self.__mainwindow, text="CARD",
                             background="red", foreground="white", command=self.payment_success, state=NORMAL)
        self.__card_button.grid(row=9, column=1, sticky=E)

    def payment_success(self):
        """ Tulostaa ilmoituksen maksun onnistumisesta metodia kutsuttaessa
        ja lukitsee maksutapanapit
        :return: none
        """
        self.__success_label.configure(text="Payment succeed!")
        self.__cash_button.configure(state=DISABLED)
        self.__card_button.configure(state=DISABLED)

    def stop(self):
        """ Lopettaa ohjelman
        """
        self.__mainwindow.destroy()

    def start(self):
        """ Aloittaa käyttöliittymän toiminnan
        """
        self.__mainwindow.mainloop()


def main():
    ui = TicketShop()
    ui.start()


main()
