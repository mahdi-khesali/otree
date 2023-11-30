from os import environ

SESSION_CONFIGS = [
dict(
        name='conventional',
        display_name="conventional",
        num_demo_participants=4,
        app_sequence=['WTPContract'],
        timeout_seconds = 600,
        treatment_order = 1,
        location = 'onlylab',
     ),
    dict(
        name='identity',
        display_name="identity",
        num_demo_participants=4,
        app_sequence=['WTPContract'],
        timeout_seconds = 600,
        treatment_order = 2,
        location = 'onlylab',
    ),
]

### Room Setup
ROOMS = [
    dict(
        name='lab',
        display_name='Lab Experiment',
        participant_label_file='_rooms/lab.txt'
    )
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.6, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = [
    'player_id',
    'name',
    'surname',
    'iban',
    'bic',
    'active',
]

SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'de'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '4799306767380'
