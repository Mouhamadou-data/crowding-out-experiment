from otree.api import *
import json

doc = """
Crowding-Out Experiment: Testing whether Individual Bonus incentives 
crowd out intrinsic motivation more than Piece Rate incentives.
Within-subjects design with counterbalanced treatment order.
"""


class C(BaseConstants):
    NAME_IN_URL = 'mycrowdingout'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    # Phase durations in seconds
    PRACTICE_DURATION = 60
    PHASE1_DURATION = 180  # 3 minutes
    PHASE2_DURATION = 180  # 3 minutes
    PHASE3_DURATION = 180  # 3 minutes
    PHASE4_DURATION = 180  # 3 minutes
    PHASE5_DURATION = 180  # 3 minutes

    # Payment parameters
    SHOW_UP_FEE = cu(5.00)
    PIECE_RATE = cu(0.20)
    BONUS_AMOUNT = cu(3.00)
    BONUS_TARGET = 12


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    for player in subsession.get_players():
        # Counterbalance treatment order
        if player.id_in_subsession % 2 == 1:
            player.treatment_order = 'PR_first'
        else:
            player.treatment_order = 'Bonus_first'


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Treatment assignment
    treatment_order = models.StringField()

    # Performance data (stored as JSON lists)
    practice_words = models.LongStringField(blank=True)
    phase1_words = models.LongStringField(blank=True)
    phase2_words = models.LongStringField(blank=True)
    phase3_words = models.LongStringField(blank=True)
    phase4_words = models.LongStringField(blank=True)
    phase5_words = models.LongStringField(blank=True)

    # Word counts
    practice_count = models.IntegerField(initial=0)
    phase1_count = models.IntegerField(initial=0)
    phase2_count = models.IntegerField(initial=0)
    phase3_count = models.IntegerField(initial=0)
    phase4_count = models.IntegerField(initial=0)
    phase5_count = models.IntegerField(initial=0)

    # Payments
    phase2_payment = models.CurrencyField(initial=0)
    phase4_payment = models.CurrencyField(initial=0)
    total_earnings = models.CurrencyField(initial=0)

    # Questionnaire after Phase 2
    q2_autonomy_pressure = models.IntegerField(
        label="I felt pressured to perform during the paid round",
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )
    q2_autonomy_freedom = models.IntegerField(
        label="I felt free to work at my own pace",
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )
    q2_autonomy_control = models.IntegerField(
        label="I felt controlled by the payment structure",
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )
    q2_enjoyment_interest = models.IntegerField(
        label="I found the word puzzles interesting",
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )
    q2_enjoyment_again = models.IntegerField(
        label="I would do this task again for fun",
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )
    q2_enjoyment_challenge = models.IntegerField(
        label="I enjoyed the challenge",
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )
    q2_cognitive_easy = models.IntegerField(
        label="The payment structure was easy to understand",
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )
    q2_cognitive_stress = models.IntegerField(
        label="I felt stressed about meeting the requirements",
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )

    # Questionnaire after Phase 4 (same questions)
    q4_autonomy_pressure = models.IntegerField(
        label="I felt pressured to perform during the paid round",
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )
    q4_autonomy_freedom = models.IntegerField(
        label="I felt free to work at my own pace",
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )
    q4_autonomy_control = models.IntegerField(
        label="I felt controlled by the payment structure",
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )
    q4_enjoyment_interest = models.IntegerField(
        label="I found the word puzzles interesting",
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )
    q4_enjoyment_again = models.IntegerField(
        label="I would do this task again for fun",
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )
    q4_enjoyment_challenge = models.IntegerField(
        label="I enjoyed the challenge",
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )
    q4_cognitive_easy = models.IntegerField(
        label="The payment structure was easy to understand",
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )
    q4_cognitive_stress = models.IntegerField(
        label="I felt stressed about meeting the requirements",
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )

    # Final questionnaire
    preferred_payment = models.StringField(
        label="Which payment scheme did you prefer?",
        choices=['Piece Rate (€0.20 per word)', 'Bonus (€3.00 for 12+ words)', 'No preference'],
        widget=widgets.RadioSelect
    )
    age = models.IntegerField(label="Age", min=18, max=100)
    gender = models.StringField(
        label="Gender",
        choices=['Male', 'Female', 'Non-binary', 'Prefer not to say'],
        widget=widgets.RadioSelect
    )
    major = models.StringField(label="Major/Field of Study")
    puzzle_experience = models.StringField(
        label="How often do you play word puzzles?",
        choices=['Never', 'Rarely', 'Sometimes', 'Often', 'Very often'],
        widget=widgets.RadioSelect
    )
    strategy = models.LongStringField(
        label="Did you use any specific strategy to find words? Please describe.",
        blank=True
    )


# PAGES

class Consent(Page):
    submit_button_text = 'I Agree'
    @staticmethod
    def is_displayed(player: Player):
        return True


class Instructions(Page):
    @staticmethod
    def is_displayed(player: Player):
        return True


class Practice(Page):
    form_model = 'player'
    form_fields = ['practice_words']
    timeout_seconds = C.PRACTICE_DURATION

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            grid_phase='practice',
            duration=C.PRACTICE_DURATION,
            phase_name='Practice Round'
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.practice_words:
            words_list = json.loads(player.practice_words)
            player.practice_count = len(words_list)


class Phase1(Page):
    form_model = 'player'
    form_fields = ['phase1_words']
    timeout_seconds = C.PHASE1_DURATION

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            grid_phase='phase1',
            duration=C.PHASE1_DURATION,
            phase_name='Phase 1: Baseline',
            is_paid=False
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.phase1_words:
            words_list = json.loads(player.phase1_words)
            player.phase1_count = len(words_list)


class Phase2Instructions(Page):
    @staticmethod
    def vars_for_template(player: Player):
        if player.treatment_order == 'PR_first':
            treatment_type = 'Piece Rate'
            payment_description = f"You will earn €0.20 for each correct word you find."
            example = "If you find 15 words, you earn 15 × €0.20 = €3.00"
        else:
            treatment_type = 'Individual Bonus'
            payment_description = f"You will earn a €{C.BONUS_AMOUNT} bonus if you find {C.BONUS_TARGET} or more words**. If you find fewer than {C.BONUS_TARGET} words, you earn €0.00 for this phase."
            example = f"If you find 12+ words: €3.00. If you find 11 or fewer: €0.00"

        return dict(
            treatment_type=treatment_type,
            payment_description=payment_description,
            example=example
        )


class Phase2(Page):
    form_model = 'player'
    form_fields = ['phase2_words']
    timeout_seconds = C.PHASE2_DURATION

    @staticmethod
    def vars_for_template(player: Player):
        if player.treatment_order == 'PR_first':
            treatment_name = 'Piece Rate'
        else:
            treatment_name = 'Bonus'

        return dict(
            grid_phase='phase2',
            duration=C.PHASE2_DURATION,
            phase_name=f'Phase 2: {treatment_name}',
            is_paid=True
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.phase2_words:
            words_list = json.loads(player.phase2_words)
            player.phase2_count = len(words_list)

            # Calculate payment
            if player.treatment_order == 'PR_first':
                player.phase2_payment = player.phase2_count * 0.20
            else:
                if player.phase2_count >= C.BONUS_TARGET:
                    player.phase2_payment = C.BONUS_AMOUNT
                else:
                    player.phase2_payment = cu(0)


class Questionnaire2(Page):
    form_model = 'player'
    form_fields = [
        'q2_autonomy_pressure',
        'q2_autonomy_freedom',
        'q2_autonomy_control',
        'q2_enjoyment_interest',
        'q2_enjoyment_again',
        'q2_enjoyment_challenge',
        'q2_cognitive_easy',
        'q2_cognitive_stress'
    ]

    @staticmethod
    def vars_for_template(player: Player):
        if player.treatment_order == 'PR_first':
            treatment_name = 'Piece Rate'
        else:
            treatment_name = 'Bonus'
        return dict(treatment_name=treatment_name)


class Phase3(Page):
    form_model = 'player'
    form_fields = ['phase3_words']
    timeout_seconds = C.PHASE3_DURATION

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            grid_phase='phase3',
            duration=C.PHASE3_DURATION,
            phase_name='Phase 3: No Payment',
            is_paid=False
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.phase3_words:
            words_list = json.loads(player.phase3_words)
            player.phase3_count = len(words_list)


class Phase4Instructions(Page):
    @staticmethod
    def vars_for_template(player: Player):
        # Opposite treatment from Phase 2
        if player.treatment_order == 'PR_first':
            treatment_type = 'Individual Bonus'
            payment_description = f"You will earn a €{C.BONUS_AMOUNT} bonus if you find {C.BONUS_TARGET} or more words. If you find fewer than {C.BONUS_TARGET} words, you earn €0.00 for this phase."
            example = f"If you find 12+ words: €3.00. If you find 11 or fewer: €0.00"
        else:
            treatment_type = 'Piece Rate'
            payment_description = f"You will earn €0.20 for each correct word you find."
            example = "If you find 15 words, you earn 15 × €0.20 = €3.00"

        return dict(
            treatment_type=treatment_type,
            payment_description=payment_description,
            example=example
        )


class Phase4(Page):
    form_model = 'player'
    form_fields = ['phase4_words']
    timeout_seconds = C.PHASE4_DURATION

    @staticmethod
    def vars_for_template(player: Player):
        if player.treatment_order == 'PR_first':
            treatment_name = 'Bonus'
        else:
            treatment_name = 'Piece Rate'

        return dict(
            grid_phase='phase4',
            duration=C.PHASE4_DURATION,
            phase_name=f'Phase 4: {treatment_name}',
            is_paid=True
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.phase4_words:
            words_list = json.loads(player.phase4_words)
            player.phase4_count = len(words_list)

            # Calculate payment (opposite of Phase 2)
            if player.treatment_order == 'PR_first':
                if player.phase4_count >= C.BONUS_TARGET:
                    player.phase4_payment = C.BONUS_AMOUNT
                else:
                    player.phase4_payment = cu(0)
            else:
                player.phase4_payment = player.phase4_count * 0.20


class Questionnaire4(Page):
    form_model = 'player'
    form_fields = [
        'q4_autonomy_pressure',
        'q4_autonomy_freedom',
        'q4_autonomy_control',
        'q4_enjoyment_interest',
        'q4_enjoyment_again',
        'q4_enjoyment_challenge',
        'q4_cognitive_easy',
        'q4_cognitive_stress'
    ]

    @staticmethod
    def vars_for_template(player: Player):
        if player.treatment_order == 'PR_first':
            treatment_name = 'Bonus'
        else:
            treatment_name = 'Piece Rate'
        return dict(treatment_name=treatment_name)


class Phase5(Page):
    form_model = 'player'
    form_fields = ['phase5_words']
    timeout_seconds = C.PHASE5_DURATION

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            grid_phase='phase5',
            duration=C.PHASE5_DURATION,
            phase_name='Phase 5: No Payment',
            is_paid=False
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.phase5_words:
            words_list = json.loads(player.phase5_words)
            player.phase5_count = len(words_list)


class FinalQuestionnaire(Page):
    form_model = 'player'
    form_fields = ['preferred_payment', 'age', 'gender', 'major', 'puzzle_experience', 'strategy']


class Payment(Page):
    @staticmethod
    def vars_for_template(player: Player):
        player.total_earnings = C.SHOW_UP_FEE + player.phase2_payment + player.phase4_payment
        player.payoff = player.total_earnings

        return dict(
            show_up_fee=C.SHOW_UP_FEE,
            phase2_earnings=player.phase2_payment,
            phase4_earnings=player.phase4_payment,
            total_payment=player.total_earnings
        )


page_sequence = [
    Consent,
    Instructions,
    Practice,
    Phase1,
    Phase2Instructions,
    Phase2,
    Questionnaire2,
    Phase3,
    Phase4Instructions,
    Phase4,
    Questionnaire4,
    Phase5,
    FinalQuestionnaire,
    Payment
]