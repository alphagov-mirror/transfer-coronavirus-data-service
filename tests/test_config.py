import os

from flask import Flask

import stubs
import config


def test_setup_talisman():
    app = Flask(__name__)
    app.app_environment = "testing"
    talisman = config.setup_talisman(app)
    assert not talisman.force_https

    app = Flask(__name__)
    app.app_environment = "staging"
    talisman = config.setup_talisman(app)
    assert talisman.force_https

    app = Flask(__name__)
    app.app_environment = "production"
    talisman = config.setup_talisman(app)
    assert talisman.force_https


def test_read_env_variables():
    app = Flask(__name__)
    config.read_env_variables(app)
    assert app.secret_key == os.getenv("APPSECRET", "secret")
    assert config.get("client_id") == os.getenv("CLIENT_ID", None)
    assert config.get("cognito_domain") == os.getenv("COGNITO_DOMAIN", None)
    assert config.get("client_secret") == os.getenv("CLIENT_SECRET", None)
    assert config.get("redirect_host") == os.getenv("REDIRECT_HOST")
    assert config.get("bucket_name") == os.getenv("BUCKET_NAME")
    assert config.get("region") == os.getenv("REGION")


def test_env_pool_id_development():
    user_pool_id = stubs.MOCK_COGNITO_USER_POOL_ID
    stubber = stubs.mock_cognito_list_pools()
    with stubber:
        assert config.env_pool_id() == user_pool_id


def test_env_pool_id_production():
    user_pool_id = stubs.MOCK_COGNITO_USER_POOL_ID
    config.set("app_environment", "production")
    stubber = stubs.mock_cognito_list_pools(env="prod")
    with stubber:
        assert config.env_pool_id() == user_pool_id


def test_list_pools():
    user_pool_id = stubs.MOCK_COGNITO_USER_POOL_ID
    stubber = stubs.mock_cognito_list_pools()

    with stubber:
        pools = config.list_pools()
        assert pools[0]["id"] == user_pool_id
        stubber.deactivate()


def test_get_cognito_pool_name():
    config.set("app_environment", "prod")
    assert config.get_cognito_pool_name() == "corona-cognito-pool-prod"
    config.set("app_environment", "production")
    assert config.get_cognito_pool_name() == "corona-cognito-pool-prod"
    config.set("app_environment", "staging")
    assert config.get_cognito_pool_name() == "corona-cognito-pool-staging"
    config.set("app_environment", "testing")
    assert config.get_cognito_pool_name() == "corona-cognito-pool-development"
