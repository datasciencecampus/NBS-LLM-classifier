from __future__ import annotations

import json

from nbs_llm_classifier.config import load_config


def test_load_config_resolves_defaults_relative_to_config_file(tmp_path):
    config_path = tmp_path / "config.json"
    config_path.write_text("{}", encoding="utf-8")

    config = load_config(config_path)

    assert config.root_dir == tmp_path.resolve()
    assert config.model_name == "sentence-transformers/all-MiniLM-L6-v2"
    assert config.n_results == 15
    assert config.progress_verbosity == "normal"
    assert config.paths.raw_dir == (tmp_path / "data/input").resolve()
    assert (
        config.paths.query_isco_file
        == (tmp_path / "data/query/query_isco.csv").resolve()
    )
    assert (
        config.paths.search_results_isco_file
        == (tmp_path / "outputs/search_results_isco.csv").resolve()
    )
    assert (
        config.paths.search_results_isic_file
        == (tmp_path / "outputs/search_results_isic.csv").resolve()
    )


def test_load_config_applies_overrides_and_normalises_progress(tmp_path):
    config_path = tmp_path / "config.json"
    config_path.write_text(
        json.dumps(
            {
                "model_name": "custom-model",
                "n_results": "5",
                "progress_verbosity": "VERBOSE",
                "paths": {
                    "raw_dir": "custom/input",
                    "search_results_isco_file": "custom/isco.csv",
                },
            }
        ),
        encoding="utf-8",
    )

    config = load_config(config_path)

    assert config.model_name == "custom-model"
    assert config.n_results == 5
    assert config.progress_verbosity == "verbose"
    assert config.paths.raw_dir == (tmp_path / "custom/input").resolve()
    assert (
        config.paths.search_results_isco_file
        == (tmp_path / "custom/isco.csv").resolve()
    )
    assert (
        config.paths.search_results_isic_file
        == (tmp_path / "outputs/search_results_isic.csv").resolve()
    )
