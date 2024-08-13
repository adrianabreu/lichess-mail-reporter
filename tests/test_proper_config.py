import pytest
from pydantic import ValidationError
from lichess_mail_reporter.config import Settings


@pytest.fixture
def mock_toml_file(mocker):
    mocker.patch(
        "builtins.open",
        mocker.mock_open(
            read_data=b"""
        username = "test_user"
        sender_name = "Test Sender"
        sender_mail = "sender@example.com"
        recipients = ["recipient1@example.com", "recipient2@example.com"]
        template_uid = "template_123"
        mail_token = "secret_token"
    """
        ),
    )


def test_settings_load(mock_toml_file):
    settings = Settings()

    assert settings.username == "test_user"
    assert settings.sender_name == "Test Sender"
    assert settings.sender_mail == "sender@example.com"
    assert settings.recipients == ["recipient1@example.com", "recipient2@example.com"]
    assert settings.template_uid == "template_123"
    assert settings.mail_token == "secret_token"


def test_settings_validation_error(mocker):
    mocker.patch(
        "builtins.open",
        mocker.mock_open(
            read_data=b"""
        username = "test_user"
        sender_name = "Test Sender"
        sender_mail = "invalid_email"
        recipients = ["recipient1@example.com", "recipient2@example.com"]
        template_uid = "template_123"
        mail_token = "secret_token"
    """
        ),
    )

    with pytest.raises(ValidationError):
        Settings()


def test_settings_missing_field(mocker):
    mocker.patch(
        "builtins.open",
        mocker.mock_open(
            read_data=b"""
        username = "test_user"
        sender_name = "Test Sender"
        sender_mail = "sender@example.com"
        recipients = ["recipient1@example.com", "recipient2@example.com"]
        template_uid = "template_123"
    """
        ),
    )

    with pytest.raises(ValidationError):
        Settings()
