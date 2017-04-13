import pytest

from ern.slack import SlackApi


##############################################
# Instances for the SlackApi class
##############################################


@pytest.fixture(scope='function')
def slack_client():
    return SlackApi()
