from otree.api import *
import random
import time
import numpy as np
import pandas as pd
from copy import deepcopy

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'WPT_contract'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


def creating_session(subsession):

    session_code = subsession.get_players()[0].session.code

    for player in subsession.get_players():
        #print( player)
        if subsession.session.config['treatment_order'] == 1:
            player.treatment_type = 'conventional'

        elif subsession.session.config['treatment_order'] == 2:
            player.treatment_type = 'identity'

    for player in subsession.get_players():
        import random
        player.contract1Type = random.choice(['expectation', 'specific'])

        if player.contract1Type == 'expectation':
            player.contract2Type = 'specific'
        elif player.contract1Type == 'specific':
            player.contract2Type = 'expectation'
        else:
            print('exception: ', player.first_vignette)
    return



### compare random price with the willingness to pay and see if the contract is concluded
def contract_conclusion(group):
    import random
    random_price = round(random.uniform(0.01, 5), 2)
    contractPayoffRelevant = random.choice(['expectation', 'specific'])
    for player in group.get_players():
        player.payoffRelevantContract = contractPayoffRelevant
        player.randomPrice = random_price
        if player.contract1Type == contractPayoffRelevant:
            player.WTP_forChosenContract = player.WTP_contract1
            if player.WTP_contract1 >= random_price:
                player.TradeResult = "success"
            elif player.WTP_contract1 < random_price:
                player.TradeResult = "fail"
            else:
                raise ValueError("There is problem in TradeResult variable")
        elif player.contract2Type == contractPayoffRelevant:
            player.WTP_forChosenContract = player.WTP_contract2
            if player.WTP_contract1 >= random_price:
                player.TradeResult = "success"
            elif player.WTP_contract1 < random_price:
                player.TradeResult = "fail"
            else:
                raise ValueError("There is problem in TradeResult variable")
    return


def contract_performance(group):
    for player in group.get_players():
        contract_peformance_options = ['performed', 'breach']
        probabilities = [0.75, 0.25]
        player_chosen_contract_peformance = random.choices(contract_peformance_options, weights=probabilities, k=1)[0]
        if player.TradeResult == "success":
            player.contractPerformance = player_chosen_contract_peformance
        elif player.TradeResult == "fail":
            player.contractPerformance = "notrelevant"
        else:
            raise ValueError("There is problem in contractPerformance variable")

    return



def avgcal(group):
    import numpy as np

    WTP_specific = np.array([])
    WTP_expection = np.array([])
    for player in group.get_players():
        if player.contract1Type == "specific":
            WTP_specific = np.append(WTP_specific, player.WTP_contract1)
        elif player.contract1Type == "expectation":
            WTP_expection = np.append(WTP_expection, player.WTP_contract1)

    for player in group.get_players():
        if player.contract1Type == "specific":
            WTP_specific = np.append(WTP_specific, player.WTP_contract2)
        elif player.contract1Type == "expectation":
            WTP_expection = np.append(WTP_expection, player.WTP_contract2)

    for player in group.get_players():
        player.avgSpecific = WTP_specific.mean()
        player.avgExpectation = WTP_expection.mean()

    return





def payoffCal(subsession):
    for player in subsession.get_players():

        if player.payoffRelevantContract == "specific":
            if (player.TradeResult == "fail"):
                pass
            elif (player.TradeResult == "success"):
                player.payOff =  player.payOff - player.randomPrice
        elif player.payoffRelevantContract == "expectation":
            if player.TradeResult == "fail":
                pass
            elif (player.TradeResult == "success") and (player.TradeResult == "breach"):
                player.payOff = player.payOff - player.randomPrice + player.WTP_expection
            elif (player.TradeResult == "success") and (player.TradeResult == "performed"):
                player.payOff = player.payOff - player.randomPrice
            else:
                raise ValueError("There is problem in TradeResult or randomPrice")
        else:
            raise ValueError("There is problem in payoffRelevantContract")

    return



class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Treatment
    treatment_type = models.StringField()

    ###################################
    #contract type
    contract1Type = models.StringField()
    contract2Type = models.StringField()

    ###################################
    #willingness to pay

    WTP_contract1 = models.FloatField()
    WTP_contract2 = models.FloatField()
    WTP_forChosenContract = models.FloatField()

    #################################
    randomPrice = models.FloatField()
    payoffRelevantContract = models.StringField()

    #################################

    TradeResult = models.StringField()

    #################################


    contractPerformance = models.StringField()

    #### Pay off ####
    #################################
    avgSpecific = models.FloatField()
    avgExpectation = models.FloatField()


    #### Pay off ####
    #################################
    payOff = models.FloatField(initial=12.5)


    ###### Salience of identity #####
    #################################
    choiceUni = models.LongStringField()
    memoryUni = models.LongStringField()


    control_ques_sum_of_wrong_ans = models.IntegerField(initial=0)

    control_ques_1 = models.IntegerField(
        label='1. Wie viel Geld können Sie Maximal ausgeben, um einen Vertrag zum Kauf eines Bechers abzuschließen?',
    )

    control_ques_2 = models.IntegerField(
        label='2. Wie viele Becher können Sie am Ende des Experiments erhalten',
    )

    control_ques_3 = models.IntegerField(
        label='3. Mit welcher Wahrscheinlichkeit kann das Geschäft seinen Vertrag nicht erfüllen?',
    )

    control_ques_4 = models.StringField(
        label='4. Bei welchem Vertragstyp ist sichergestellt, dass Sie den Becher so erhalten, wie Sie ihn bestellt haben?',
        choices=[
            'Typ A',
            'Typ B'
        ], widget=widgets.RadioSelect
    )

    control_ques_5 = models.FloatField(
    label='5. Mit welchem Geldbetrag werden Sie das Labor unter folgenden Bedingungen verlassen: \n'
          'a. Vertragstyp B wird zufällig als zahlungswirksam ausgewählt. \n'
          'b. Der zufällige Produktpreis beträgt 3,22 Euro.\n'
          'c. Ihre maximale Zahlungsbereitschaft für Vertragstyp B beträgt 4,67 Euro.\n'
          'd. Das Geschäft beabsichtigt, den Vertrag zu brechen.\n',
    )



    # Screen: Demographics
    age = models.IntegerField(initial=None, min=16, max=120, label="Wie alt sind Sie?")

    gender = models.IntegerField(
        choices=[
            [1, "weiblich"],
            [2, "männlich"],
            [3, "divers"]
        ], widget=widgets.RadioSelect
        , label="Welchem Geschlecht ordnen Sie sich zu?")

    geschwister = models.IntegerField(initial=None, min=0, max=99, label="Wie viele Geschwister haben Sie?")

    previous_participation = models.IntegerField(
        choices=[
            [1, "Noch nie"],
            [2, "1 bis 2 mal"],
            [3, "3 bis 5 mal"],
            [4, "öfter"]
        ], widget=widgets.RadioSelect
        , label="Wie häufig haben Sie schon an einem verhaltensökonomischen Experiment teilgenommen?")


    currently_employed = models.IntegerField(
        choices=[
            [1, 'Ja'],
            [2, 'Nein'],
        ]
        , label="Stehen Sie in einem festen Arbeitsverhältnis mit mehr als 10 Arbeitsstunden in der Woche?")



    currently_studying = models.IntegerField(
        choices=[
            [1, 'Ja'],
            [2, 'Nein'],
        ],
        label="Studieren Sie?"
    )

    study_semester = models.IntegerField(min=0, max=100,
                                         label="Wenn ja, in welchem Hochschulsemester befinden Sie sich? (Wenn Sie nicht studieren, geben Sie bitte „0“ ein.)")

    study_course = models.IntegerField(
        choices=[
            [1, "Ich studiere nicht"],
            [2, "Kulturwissenschaften"],
            [3, "Sprachwissenschaften"],
            [4, "Philosophie/Sonstige Geisteswissenschaften"],
            [5, "Pädagogik/Erziehungswissenschaften"],
            [6, "Rechtswissenschaften"],
            [7, "Wirtschaftswissenschaften"],
            [8, "Sozial- und Politikwissenschaft"],
            [9, "Medizin/Pflegewissenschaft"],
            [10, "Land- und Forstwissenschaften"],
            [11, "Mathematisch-naturwissenschaftliche Fächer"],
            [12, "Technische Wissenschaften"],
            [13, "Kunst oder Musik"],
            [14, "Sonstiges"],
        ], widget=widgets.RadioSelect
        , label="Was studieren Sie? (Wenn Sie nicht studieren, markieren Sie bitte die Antwort „Ich studiere nicht“.):")




'''
********************************************************************************************************************************************************
Overview pages of Experiment
********************************************************************************************************************************************************
'''
class C1_introduction(Page):
    @staticmethod
    def is_displayed(player):
        return True
class C2_mainDecision(Page):
    @staticmethod
    def is_displayed(player):
        return True
class C3_mechanism(Page):
    @staticmethod
    def is_displayed(player):
        return True
class C4_examples(Page):
    @staticmethod
    def is_displayed(player):
        return True
class C5_1_controlQuestions(Page):
    form_model = 'player'
    form_fields = ['control_ques_1','control_ques_2','control_ques_3','control_ques_4','control_ques_5']


    @staticmethod
    def error_message(player, values):
        #print('values is', values)
        string_to_append = dict()
            #"Bitte überprüfen Sie Ihre Angaben. Sehen Sie sich dazu die Informationen erneut an."]
        if values['control_ques_1'] != 5:
            player.control_ques_sum_of_wrong_ans += 1
            string_to_append['control_ques_1'] = 'Kontrollfrage 1 ist falsch.'

        if values['control_ques_2'] != 1:
            player.control_ques_sum_of_wrong_ans += 1
            string_to_append['control_ques_2'] = 'Kontrollfrage 2 ist falsch.'

        if values['control_ques_3'] != 25:
            player.control_ques_sum_of_wrong_ans += 1
            string_to_append['control_ques_3'] = 'Kontrollfrage 3 ist falsch.'

        if values['control_ques_4'] != "Typ B":
            player.control_ques_sum_of_wrong_ans += 1
            string_to_append['control_ques_4'] = 'Kontrollfrage 4 ist falsch.'

        if values['control_ques_5'] != 7.83:
            player.control_ques_sum_of_wrong_ans += 1
            string_to_append['control_ques_5'] = 'Kontrollfrage 5 ist falsch.'

        return string_to_append
class C5_2_bonnChoice(Page):
    form_model = 'player'
    form_fields = ['choiceUni']
    @staticmethod
    def is_displayed(player):
        return True
class C5_3_bonnMemory(Page):
    form_model = 'player'
    form_fields = ['memoryUni']
    @staticmethod
    def is_displayed(player):
        return True
class C6_contract1(Page):
    form_model = 'player'
    form_fields = ['WTP_contract1']

    @staticmethod
    def is_displayed(player):
        return True
class C6_contract2(Page):
    form_model = 'player'
    form_fields = ['WTP_contract2']

    @staticmethod
    def is_displayed(player):
        return True
class C7_tradeResult(WaitPage):
    form_model = 'player'
    form_fields = ['randomPrice', 'payoffRelevantContract', 'TradeResult']
    after_all_players_arrive = 'contract_conclusion'


    @staticmethod
    def is_displayed(player):
        return True
class C7_1_tradeResult(WaitPage):
    form_model = 'player'
    form_fields = ['randomPrice', 'payoffRelevantContract', 'TradeResult']

    after_all_players_arrive = 'contract_performance'
    @staticmethod
    def is_displayed(player):
        return True
class C7_2_tradeResult(WaitPage):
    form_model = 'player'
    form_fields = ['randomPrice', 'payoffRelevantContract', 'TradeResult']

    after_all_players_arrive = 'avgcal'
    @staticmethod
    def is_displayed(player):
        return True
class C8_contractResult(Page):

    @staticmethod
    def is_displayed(player):
        return True
class C9_contractPerform(Page):

    @staticmethod
    def is_displayed(player):
        return True
class C10_demographics(Page):
    form_model = 'player'
    form_fields = [
        'age',
        'gender',
        'geschwister',
        'previous_participation',
        'currently_employed',
        'currently_studying',
        'study_semester',
        'study_course'
    ]


    @staticmethod
    def is_displayed(player):
        return True
class C11_WaitForSavingResults(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = 'payoffCal'

    def is_displayed(player):
        return True
class C12_resultPage(Page):
    def is_displayed(player):
        return True
class C13_Final_Page(Page):
    def is_displayed(player):
        return True




page_sequence = [ C1_introduction,
                  C2_mainDecision, C3_mechanism, C4_examples, C5_1_controlQuestions,
                  C5_2_bonnChoice, C5_3_bonnMemory,
                  C6_contract1, C6_contract2,
                  C7_tradeResult, C7_1_tradeResult, C7_2_tradeResult, C8_contractResult, C9_contractPerform,
                  C10_demographics,
                  C11_WaitForSavingResults, C12_resultPage, C13_Final_Page]
