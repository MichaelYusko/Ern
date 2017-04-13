from ern.slack import SlackApi
import pytest

##############################################
# Instances for the SlackApi class
##############################################


@pytest.fixture(scope='function')
def slack_client():
    return SlackApi()
