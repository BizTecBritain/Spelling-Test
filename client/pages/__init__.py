__all__ = ['EndPage', 'LeaderboardPage', 'LoginPage', 'MenuPage', 'RegistrationPage', 'SpellingTestPage',
           'DifficultyPage', 'ForgotPasswordPage', 'TooManyRequestsPage', 'RegistrationVerifyPage', 'ForgotVerifyPage']
__version__ = '2.0.0'
__author__ = 'Finley Wallace - Wright'

from .end_page import EndPage
from .leaderboard_page import LeaderboardPage
from .login_page import LoginPage
from .menu_page import MenuPage
from .registration_page import RegistrationPage
from .spelling_test_page import SpellingTestPage
from .difficulty_page import DifficultyPage
from .forgot_password import ForgotPasswordPage
from .too_many_requests import TooManyRequestsPage
from .registration_verify import RegistrationVerifyPage
from .forgot_verify import ForgotVerifyPage
