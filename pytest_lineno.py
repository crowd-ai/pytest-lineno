"""
Invoke tests by linenumber, e.g. foo/bar/baz.py::100
"""
import re
import ast

import pytest  # pylint: disable=unused-import


LINENO_RE = re.compile(r'^(.+\.py)::?(\d+$)')


class GetTargetClassOrFunction(ast.NodeVisitor):
  """
  Gets the target class or method for a given linenumber.
  """
  def __init__(self, target_lineno):
    self.target_lineno = target_lineno
    self.last_node = None
    self.target_node_path = None

  def _visit_node(self, node, parents=None):
    if self.target_node_path is not None:
      return
    parents = parents or []
    if self.last_node.lineno <= self.target_lineno <= node.lineno:
      self.target_node_path = parents + [self.last_node]
    self.last_node = node

  def visit_ClassDef(self, node):
    self.last_node = node
    self._visit_node(node)
    for cnode in ast.iter_child_nodes(node):
      if isinstance(cnode, ast.FunctionDef):
        self._visit_node(cnode, parents=[node])
    # check if target is in the last function def
    self._visit_node(ast.Pass(lineno=float('inf')), parents=[node])

  def visit_FunctionDef(self, node):
    self._visit_node(node)


def pytest_cmdline_preparse(config, args):  # pylint: disable=unused-argument
  """
  Converts linenumber args to proper pytest format, e.g file.py::Class::method
  """
  for i, arg in enumerate(args):
    m = LINENO_RE.search(arg)
    if not m:
      continue
    fpath = m.group(1)
    lineno = int(m.group(2))

    with open(fpath, 'r') as f:
      ast_mod = ast.parse(f.read())

    visitor = GetTargetClassOrFunction(lineno)
    visitor.visit(ast_mod)
    if visitor.target_node_path:
      args[i] = '::'.join([fpath] + [n.name for n in visitor.target_node_path])
