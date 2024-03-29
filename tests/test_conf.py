from devcli import project_root
from devcli.config import Config


def test_it_parses_one_conf_file():
    config_file = project_root('tests/fixtures/general.toml')
    conf = Config().add_config(config_file)
    assert conf['devcli']['key'] == 'value'


def test_it_adds_configurations_of_other_files():
    conf = Config().add_config(project_root('tests/fixtures/general.toml'))
    assert conf['devcli']['key'] == 'value'
    assert conf['a_specific_configuration'] is None

    conf.add_config(project_root('tests/fixtures/specific.toml'))
    assert conf['devcli']['key'] == 'value'
    assert conf['a_specific_configuration']['key'] == 'value'


def test_it_ignores_if_asked_to_load_non_existent_file():
    conf = Config().add_config(project_root('tests/fixtures/general.toml'))
    conf.add_config('this_file_does_not_exists')
    assert conf['devcli']['key'] == 'value'


def test_it_accepts_fetch_through_path_str():
    conf = Config().add_config(project_root('tests/fixtures/general.toml'))
    assert conf['devcli.key'] == 'value'
