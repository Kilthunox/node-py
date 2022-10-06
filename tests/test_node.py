import pytest

from ..monota import Node


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
                self.initattr("pi", pi)
                self.initattr("pi2", pi**2)
                super().build()

            def run(self):
                self(
                    self.get_name(),
                )
                pass
                super().run()

        app = ExtendedNode(
            "Test"
        )
        app.build()
        app.run()

    def test_add_child_node(self):
        app = Node("parent")
        app("rename_test_2", Node("child"))
        app["child/destruct"]()
        assert "child" not in app.get_view()
        app.build()
        app.run()
