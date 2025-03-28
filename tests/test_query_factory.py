from unittest.mock import MagicMock, patch

import pytest

from openstackquery.query_factory import QueryFactory


@pytest.fixture(name="run_build_query_deps_test_case")
def run_build_query_deps_test_case_fixture():
    """Fixture for running build_query_deps"""

    # ignore too-many-arguments warnings
    # pylint: disable=R0913,R0917
    @patch("openstackquery.query_factory.QueryBuilder")
    @patch("openstackquery.query_factory.QueryOutput")
    @patch("openstackquery.query_factory.QueryParser")
    @patch("openstackquery.query_factory.QueryExecutor")
    @patch("openstackquery.query_factory.QueryChainer")
    @patch("openstackquery.query_factory.QueryComponents")
    def _run_build_query_deps_test_case(
        mock_query_components,
        mock_chainer,
        mock_executor,
        mock_parser,
        mock_output,
        mock_builder,
    ):
        """
        Tests build_query deps works with different inputs - namely
        if provided forwarded outputs or not
        """
        mock_mapping_cls = MagicMock()
        res = QueryFactory.build_query_deps(mock_mapping_cls)

        mock_mapping_cls.get_prop_mapping.assert_called_once()
        mock_prop_mapping = mock_mapping_cls.get_prop_mapping.return_value

        mock_output.assert_called_once_with(mock_prop_mapping)
        mock_parser.assert_called_once_with(mock_prop_mapping)
        mock_builder.assert_called_once_with(
            prop_enum_cls=mock_prop_mapping,
            client_side_handler=mock_mapping_cls.get_client_side_handler.return_value,
            server_side_handler=mock_mapping_cls.get_server_side_handler.return_value,
        )
        mock_chainer.assert_called_once_with(
            chain_mappings=mock_mapping_cls.get_chain_mappings.return_value
        )

        mock_executor.assert_called_once_with(
            prop_enum_cls=mock_prop_mapping,
            runner_cls=mock_mapping_cls.get_runner_mapping.return_value,
        )

        mock_query_components.assert_called_once_with(
            mock_output.return_value,
            mock_parser.return_value,
            mock_builder.return_value,
            mock_executor.return_value,
            mock_chainer.return_value,
        )
        assert res == mock_query_components.return_value

    return _run_build_query_deps_test_case


def test_build_query_deps(run_build_query_deps_test_case):
    """
    Test that function build_query_deps works - with no forwarded outputs
    should build all query blocks and return QueryComponent dataclass using them
    """
    run_build_query_deps_test_case()
