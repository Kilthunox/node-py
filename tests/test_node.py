import pytest

from ..src import Node


@pytest.mark.node
class TestNode:
    def test_build_run_node(self):
        app = Node(
            "App",
            Node("FirstNode"),
            Node("SecondNode"),
        )
        app.build()
        app.run()
