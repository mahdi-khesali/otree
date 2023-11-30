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
    NAME_IN_URL = 'stealing_game'
    PLAYERS_PER_GROUP = 6
    NUM_ROUNDS = 1


def creating_session(subsession):

    session_code = subsession.get_players()[0].session.code

    private_data_df = pd.DataFrame(
        columns=['id', 'name', 'surname', 'iban', 'bic',  'payoff_euros'])
    private_data_df.to_csv('stealinggame_private_data_df_' + session_code + '.csv')

    for player in subsession.get_players():
        #print( player)
        if subsession.session.config['treatment_order'] == 1:
            player.treatment_type = 'Baseline'

        elif subsession.session.config['treatment_order'] == 2:
            player.treatment_type = 'Mere_Voting'

        elif subsession.session.config['treatment_order'] == 3:
            player.treatment_type = 'Expressive_Voting'




def match_and_assign_roles(group):

    player_list = group.get_players()

    shuffled_player_list = random.sample(player_list, len(player_list))

    for pos in range(0, len(shuffled_player_list), 2):

        shuffled_player_list[pos].player_own_code = shuffled_player_list[pos].participant.code
        shuffled_player_list[pos + 1].player_own_code = shuffled_player_list[pos + 1].participant.code

        shuffled_player_list[pos].matched_player_code = shuffled_player_list[pos + 1].participant.code
        shuffled_player_list[pos + 1].matched_player_code = shuffled_player_list[pos].participant.code

        if shuffled_player_list[pos].count_tables_correct < shuffled_player_list[pos + 1].count_tables_correct:
            shuffled_player_list[pos].player_role = 'B'
            shuffled_player_list[pos + 1].player_role = 'A'
        elif shuffled_player_list[pos].count_tables_correct > shuffled_player_list[pos + 1].count_tables_correct:
            shuffled_player_list[pos].player_role = 'A'
            shuffled_player_list[pos + 1].player_role = 'B'
        elif shuffled_player_list[pos].count_tables_correct == shuffled_player_list[pos + 1].count_tables_correct:
            shuffled_player_list[pos].player_role, shuffled_player_list[pos + 1].player_role = random.sample(
                ['A', 'B'], 2)

def calculate_voting(group):

    count_yes = 0
    count_no = 0

    for p in group.get_players():
        if p.VOTING == 1:
            count_yes += 1
        elif p.VOTING == 2:
            count_no += 1

    for p in group.get_players():
        p.group_voting_reveal_ja = count_yes
        p.group_voting_reveal_nein = count_no

def calculate_final_points(group):

    for pA in group.get_players():
        if pA.player_role == 'A':

            assert pA.player_points == 10

            pA.player_points = pA.player_points + pA.STOLEN_AMOUNT

            pA.final_payoff_euros = np.round(pA.player_points * 0.6, 2)

            for pB in group.get_players():

                if pB.participant.code == pA.matched_player_code:
                    assert pB.player_role == 'B'

                    assert pB.player_points == 10

                    pB.player_points = pB.player_points - pA.STOLEN_AMOUNT

                    pB.final_payoff_euros = np.round(pB.player_points * 0.6, 2)



def save_results_dataframe(subsession):

    session_code = subsession.get_players()[0].session.code

    df = pd.read_csv('stealinggame_private_data_df_'+ str(session_code) + '.csv', index_col = 0)

    for player in subsession.get_players():
        player.participant.vars['payoff_euros'] = player.final_payoff_euros + 5
        df = df.append(pd.Series(player.participant.vars)[df.columns], ignore_index=True)

        player.participant.vars['name'] = 'DELETED'
        player.participant.vars['surname'] = 'DELETED'
        player.participant.vars['iban'] = 'DELETED'
        player.participant.vars['bic'] = 'DELETED'

    df.to_csv('stealinggame_private_data_df_'+ str(session_code) + '.csv')



class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass


class Player(BasePlayer):

    test = models.IntegerField()

    final_payoff_euros = models.FloatField()

    player_points = models.IntegerField(initial=10)

    # Treatment
    treatment_type = models.StringField()

    # Keep count of number of tables the participant has seen in total
    count_tables_seen = models.IntegerField(initial=1)
    count_tables_correct = models.IntegerField(initial=0)

    # The answer variable for the number of zeroes present in the table.
    ans = models.IntegerField()

    # Table answer variables and boolean variables for correctness
    table_answer = models.IntegerField()
    table_correct_flag = models.BooleanField()

    player_own_code = models.StringField()
    matched_player_code = models.StringField()

    player_role = models.StringField()

    VOTING = models.IntegerField(
        choices=[
            [1, 'Ja'],
            [2, 'Nein'],
        ])

    group_voting_reveal_ja = models.IntegerField()
    group_voting_reveal_nein = models.IntegerField()

    BELIEF_ELICITATION = models.IntegerField(label='Geben Sie eine Ganzzahl ein:')

    STOLEN_AMOUNT = models.IntegerField(label='Geben Sie eine Ganzzahl ein:', min=0, max=10)

    control_ques_sum_of_wrong_ans = models.IntegerField(initial=0)

    control_ques_1 = models.StringField(
        label='1. Welche Rolle wird Ihnen zugewiesen, wenn Sie mehr Tabellen lösen als der Teilnehmer, mit dem Sie gepaart sind? ',
        choices=[
            'Person A',
            'Person B'
        ], widget=widgets.RadioSelect
    )

    control_ques_2 = models.IntegerField(
        label='2. Welche Zahl geben Sie in Stufe 2 ein, wenn Sie glauben, dass Sie 7 Rätsel gelöst haben und der Teilnehmer, mit dem Sie gepaart sind, 5 Rätsel gelöst hat?',
    )

    control_ques_3 = models.IntegerField(
        label='3. Angenommen, Ihnen wurde die Rolle von Person A zugewiesen: Wie viele Punkte haben Sie am Ende des Experiments, wenn Sie dem Teilnehmer, mit dem Sie gepaart sind, 8 Punkte abnehmen?',
    )


    control_ques_4 = models.IntegerField(
    label='4. Angenommen, Ihnen wurde die Rolle von Person B zugewiesen: Wie viele Punkte haben Sie am Ende des Experiments, wenn der Teilnehmer, mit dem Sie gepaart sind, Ihnen 3 Punkte wegnimmt?',
    )

    control_ques_5 = models.StringField(
        label='5. Können Sie sich in Phase 2 für die Norm entscheiden, indem Sie "JA" anklicken, oder gegen diese Norm, indem Sie "NEIN" anklicken?',
        choices=[
            'Ja',
            'Nein'
        ], widget=widgets.RadioSelect
    )

    control_ques_6 = models.StringField(
        label='6. Wird Ihnen das Ergebnis der Abstimmung am Ende von Phase 2 bekannt gegeben?',
        choices=[
            'Ja',
            'Nein'
        ], widget=widgets.RadioSelect
    )
    '''
    control_ques_1 = models.IntegerField(
        label='1. Wie hoch ist die Anzahl der Mitglieder Ihrer Gruppe? ',
        choices=[
            [6, '6'],
            [7, '7'],
            [8, '8'],
        ], widget=widgets.RadioSelect
    )

    control_ques_2 = models.IntegerField(
        label='2. Wie viele Versuche haben Sie, um eine Tabelle zu lösen?',
        choices=[
            [2, '2'],
            [3, '3'],
            [4, '4'],
        ], widget=widgets.RadioSelect
    )

    control_ques_3 = models.IntegerField(
        label='3. Wie viele Minuten haben Sie für die Aufgabe zur Verfügung?',
        choices=[
            [9, '9'],
            [7, '7'],
            [5, '5'],
        ], widget=widgets.RadioSelect
    )

    control_ques_4 = models.IntegerField(
        label='4. Wer trifft die Entscheidung in der Entscheidungsphase? ',
        choices=[
            [1, 'Person A'],
            [2, 'Person B'],
            [3, 'Person A and Person B'],
        ], widget=widgets.RadioSelect
    )
    '''

    # Screen: Demographics
    age = models.IntegerField(initial=None, min=1, max=120, label="Wie alt sind Sie?")

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
        , label="Wie häufig haben Sie schon an Experimenten teilgenommen?")


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
                                         label="Wenn ja, in welchem Hochshulsemester befinden Sie sich? (Wenn Sie nicht studieren, geben Sie bitte „0“ ein.)")

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


# PAGES
'''
********************************************************************************************************************************************************
Overview pages of Experiment
********************************************************************************************************************************************************
'''


def group_by_arrival_time_method(subsession, waiting_players):
    if len(waiting_players) >= 6:
        return waiting_players[:6]


class FirstWaitPage(WaitPage):
    timer_text = 'Verbleibende Zeit:'
    group_by_arrival_time = True

    @staticmethod
    def is_displayed(player):
        return True




class Intro(Page):
    def is_displayed(player):
        return True


class MainDecision(Page):
    def is_displayed(player):
        return True

class Procedure(Page):
    def is_displayed(player):
        return True


'''
********************************************************************************************************************************************************
Control Questions
********************************************************************************************************************************************************
'''
class ControlQuestions(Page):
    form_model = 'player'
    form_fields = ['control_ques_1','control_ques_2','control_ques_3','control_ques_4']


    @staticmethod
    def error_message(player, values):
        #print('values is', values)
        string_to_append = dict()
            #"Bitte überprüfen Sie Ihre Angaben. Sehen Sie sich dazu die Informationen erneut an."]
        if values['control_ques_1'] != 'Person A':
            player.control_ques_sum_of_wrong_ans += 1
            string_to_append['control_ques_1'] = 'Kontrollfrage 1 ist falsch.'

        if values['control_ques_2'] != 2:
            player.control_ques_sum_of_wrong_ans += 1
            string_to_append['control_ques_2'] = 'Kontrollfrage 2 ist falsch.'

        if values['control_ques_3'] != 18:
            player.control_ques_sum_of_wrong_ans += 1
            string_to_append['control_ques_3'] = 'Kontrollfrage 3 ist falsch.'

        if values['control_ques_4'] != 7:
            player.control_ques_sum_of_wrong_ans += 1
            string_to_append['control_ques_4'] = 'Kontrollfrage 4 ist falsch.'

        return string_to_append


    def is_displayed(player):
        if (player.treatment_type == 'Mere_Voting') or (player.treatment_type == 'Expressive_Voting'):
            return False
        else:
            return True

    def before_next_page(player, timeout_happened):

        player.participant.vars['expiry'] = time.time() + 300

        # Number of chances remaining for the player to complete a table.
        player.participant.vars['num'] = 3

        # Initialize table 1 for participant
        player.participant.vars['table'] = np.random.choice([0, 1], size=(15, 10), p=[0.45, 0.55])

        player.participant.vars['table'] = list(list(i) for i in player.participant.vars['table'])

        #self.participant.vars['table_ans'] = 150 - self.participant.vars['table'].sum()
        player.participant.vars['table_ans'] = 150 - sum(np.array(sum(np.array(player.participant.vars['table']))))

        player.table_answer = int(deepcopy(player.participant.vars['table_ans']))

        player.participant.vars['n_table_correct'] = 0

        # Flag variables to check if player has got the tables correct in the upcoming pages.
        player.table_correct_flag = False




class ControlQuestions_with5and6(Page):
    form_model = 'player'
    form_fields = ['control_ques_1','control_ques_2','control_ques_3','control_ques_4','control_ques_5','control_ques_6']


    @staticmethod
    def error_message(player, values):
        #print('values is', values)
        string_to_append = dict()
            #"Bitte überprüfen Sie Ihre Angaben. Sehen Sie sich dazu die Informationen erneut an."]
        if values['control_ques_1'] != 'Person A':
            player.control_ques_sum_of_wrong_ans += 1
            string_to_append['control_ques_1'] = 'Kontrollfrage 1 ist falsch.'

        if values['control_ques_2'] != 2:
            player.control_ques_sum_of_wrong_ans += 1
            string_to_append['control_ques_2'] = 'Kontrollfrage 2 ist falsch.'

        if values['control_ques_3'] != 18:
            player.control_ques_sum_of_wrong_ans += 1
            string_to_append['control_ques_3'] = 'Kontrollfrage 3 ist falsch.'

        if values['control_ques_4'] != 7:
            player.control_ques_sum_of_wrong_ans += 1
            string_to_append['control_ques_4'] = 'Kontrollfrage 4 ist falsch.'

        if values['control_ques_5'] != 'Ja':
            player.control_ques_sum_of_wrong_ans += 1
            string_to_append['control_ques_5'] = 'Kontrollfrage 5 ist falsch.'

        if player.treatment_type == 'Mere_Voting':
            if values['control_ques_6'] != 'Nein':
                player.control_ques_sum_of_wrong_ans += 1
                string_to_append['control_ques_6'] = 'Kontrollfrage 6 ist falsch.'
        elif player.treatment_type == 'Expressive_Voting':
            if values['control_ques_6'] != 'Ja':
                player.control_ques_sum_of_wrong_ans += 1
                string_to_append['control_ques_6'] = 'Kontrollfrage 6 ist falsch.'

        return string_to_append


    def is_displayed(player):
        if (player.treatment_type == 'Mere_Voting') or (player.treatment_type == 'Expressive_Voting'):
            return True
        else:
            return False

    def before_next_page(player, timeout_happened):

        player.participant.vars['expiry'] = time.time() + 300

        # Number of chances remaining for the player to complete a table.
        player.participant.vars['num'] = 3

        # Initialize table 1 for participant
        player.participant.vars['table'] = np.random.choice([0, 1], size=(15, 10), p=[0.45, 0.55])

        player.participant.vars['table'] = list(list(i) for i in player.participant.vars['table'])

        #self.participant.vars['table_ans'] = 150 - self.participant.vars['table'].sum()
        player.participant.vars['table_ans'] = 150 - sum(np.array(sum(np.array(player.participant.vars['table']))))

        player.table_answer = int(deepcopy(player.participant.vars['table_ans']))

        player.participant.vars['n_table_correct'] = 0

        # Flag variables to check if player has got the tables correct in the upcoming pages.
        player.table_correct_flag = False

        player.participant.vars['table_answered_correctly_flag'] = False
        player.participant.vars['new_table_flag'] = True




'''
********************************************************************************************************************************************************
Solve multiple tables 
********************************************************************************************************************************************************
'''
class Table_Solve_infinite(Page):
    timer_text = 'Verbleibende Zeit:'
    form_model = 'player'
    form_fields = ['ans']

    def vars_for_template(player):
        return dict(tries=player.participant.vars['num'], table=list(player.participant.vars['table']), n_table_correct = player.participant.vars['n_table_correct'], n_white_zeros =range(np.random.randint(40,50,1)[0]))
        #, n_white_zeros =range(np.random.randint(40,50,1)[0])

    def get_timeout_seconds(player):
        return player.participant.vars['expiry'] - time.time()

    def is_displayed(player):
        # Display only if the timer is still running.
        return (player.participant.vars['expiry'] - time.time() > 3)

    def error_message(player, values):
        # Calculating the number of zeroes in the randomly generated table.
        #self.player.count_tables_seen += 1

        #self.participant.vars['table_ans'] = 150 - self.participant.vars['table'].sum()
        player.participant.vars['table_ans'] =  150 - sum(np.array(sum(np.array(player.participant.vars['table']))))

        player.table_answer = int(deepcopy(player.participant.vars['table_ans']))

        # Checking if the player has got the correct answer. If the answer is correct no error is returned.
        if values['ans'] == player.participant.vars['table_ans']:

            player.count_tables_correct += 1
            player.count_tables_seen +=  1
            player.participant.vars['n_table_correct'] += 1



            # Initialize table 2 for participant
            player.participant.vars['table'] = np.random.choice([0, 1], size=(15, 10), p=[0.45, 0.55])
            player.participant.vars['table'] = list(list(i) for i in player.participant.vars['table'])

            #self.participant.vars['table_ans'] = 150 - self.participant.vars['table'].sum()
            player.participant.vars['table_ans'] = 150 - sum(np.array(sum(np.array(player.participant.vars['table']))))

            player.table_answer = int(deepcopy(player.participant.vars['table_ans']))

            # Set tries = 3
            player.participant.vars['num'] = 3


            return ("Die vorherige Tabelle war RICHTIG. Eine NEUE TABELLE wurde generiert und Sie haben 3 VERSUCHE.")



        # When the player get a wrong answer, reduce the number of chances and return error message accordingly.
        elif values['ans'] != player.participant.vars['table_ans']:

            if player.participant.vars['num'] == 1:
                player.count_tables_seen += 1
                player.participant.vars['table'] = np.random.choice([0, 1], size=(15, 10), p=[0.45, 0.55])
                player.participant.vars['table'] = list(list(i) for i in player.participant.vars['table'])

                player.participant.vars['num'] = 3

                #self.participant.vars['table_ans'] = 150 - self.participant.vars['table'].sum()
                player.participant.vars['table_ans'] = 150 - sum(np.array(sum(np.array(player.participant.vars['table']))))

                player.table_answer = int(deepcopy(player.participant.vars['table_ans']))


                return (
                    "Sie haben 3 Versuche an der letzten Tabelle abgeschlossen. Eine neue Tabelle wurde generiert und Sie haben erneut 3 Versuche.")

            else:
                player.participant.vars['num'] -= 1



                return ("Die Antwort ist nicht korrekt. Bitte versuchen Sie es erneut. Sie haben noch " + str(
                    player.participant.vars['num']) + " Versuche.")

'''
********************************************************************************************************************************************************
End of Part1
********************************************************************************************************************************************************
'''

class Part1_End(Page):
    def is_displayed(player):
        return True


'''
********************************************************************************************************************************************************
End of Part1: Matching
********************************************************************************************************************************************************
'''

class MyWaitPage(WaitPage):
    body_text = 'Bitte warten Sie, bis das Experiment weitergeht.'

    after_all_players_arrive = 'match_and_assign_roles'


    def is_displayed(player: Player):
        return True


class Abstimmung(Page):
    form_model = 'player'
    form_fields = ['VOTING']

    def is_displayed(player):
        if (player.treatment_type == 'Mere_Voting') or (player.treatment_type == 'Expressive_Voting'):
            return True


class WaitBeforeRevealingVote(WaitPage):
    body_text = 'Bitte warten Sie, bis das Experiment weitergeht.'

    after_all_players_arrive = 'calculate_voting'

    def is_displayed(player):
        if (player.treatment_type == 'Expressive_Voting'):
            return True

class Reveal_Voting(Page):

    def is_displayed(player):
        if (player.treatment_type == 'Expressive_Voting'):
            return True

class Reveal_Role(Page):
    def is_displayed(player):
        return True


class BeliefElicitation(Page):
    form_model = 'player'
    form_fields = ['BELIEF_ELICITATION']

    def is_displayed(player):
        if player.player_role == 'A':
            return True
        elif player.player_role == 'B':
            return False



class Steal(Page):
    form_model = 'player'
    form_fields = ['STOLEN_AMOUNT']

    def is_displayed(player):
        if player.player_role == 'A':
            return True
        elif player.player_role == 'B':
            return False


class WaitForStealingGame(WaitPage):
    after_all_players_arrive = 'calculate_final_points'

    def is_displayed(player):
        return True

class Demographics(Page):
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

    def is_displayed(player):
        return True

class Results(Page):

    def vars_for_template(player: Player):
        if player.player_role == 'A':
            return dict(stolen_amount = player.STOLEN_AMOUNT)
        if player.player_role == 'B':
            return dict(stolen_amount = 10 - player.player_points)

    def is_displayed(player):
        return True


class WaitForSavingResults(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = 'save_results_dataframe'

    def is_displayed(player):
        return True

class Final_Page(Page):
    def is_displayed(player):
        return True




page_sequence = [ FirstWaitPage, Intro, MainDecision, Procedure, ControlQuestions, ControlQuestions_with5and6, Table_Solve_infinite,  MyWaitPage,
                  Abstimmung,  WaitBeforeRevealingVote, Reveal_Voting, Reveal_Role,
                 BeliefElicitation, Steal, WaitForStealingGame, Demographics,WaitForSavingResults, Results, Final_Page]
