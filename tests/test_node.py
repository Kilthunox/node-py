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

    def test_extend_node(self):
        class ExtendedNode(Node):
            def build(self):
                from math import pi
                self.iniattr("pi", pi)
                self.initattr("pi2", pi**2)
                super().build()

            def run(self):
                pass
                super().run()

        app = ExtendedNode(
            "Test"
        )
        app.build()
        app.run()
