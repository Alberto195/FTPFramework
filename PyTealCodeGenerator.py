import ast


class AnnotationTransformer(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        scope_annotation = next((a for a in node.decorator_list if a.id.startswith("X")), None)
        if scope_annotation:
            node.scope = scope_annotation.id
        else:
            node.scope = "XAll"
        return node

    def visit_AnnAssign(self, node):
        scope_annotation = next((a for a in node.annotation.values if a.id.startswith("X")), None)
        if scope_annotation:
            node.scope = scope_annotation.id
        else:
            node.scope = "XAll"
        return node


class PyTealCodeGenerator(ast.NodeVisitor):
    def __init__(self):
        self.code = ""
        self.current_scope = "XAll"

    def visit_FunctionDef(self, node):
        self.current_scope = node.scope

    def visit_AnnAssign(self, node):
        self.current_scope = node.scope

    def visit_Module(self, node):
        for stmt in node.body:
            self.visit(stmt)

    def visit_Assign(self, node):
        if isinstance(node.value, ast.Num):
            var_name = node.targets[0].id
            value = node.value.n
            if self.current_scope == "XAll" or self.current_scope == "XOnServer":
                self.code += f"{var_name} = {value}\n"
            if self.current_scope == "XAll" or self.current_scope == "XOnChain":
                pass

        if isinstance(node.value, ast.Str):
            var_name = node.targets[0].id
            value = node.value.n
            if self.current_scope == "XAll" or self.current_scope == "XOnServer":
                self.code += f"{var_name} = {value}\n"
            if self.current_scope == "XAll" or self.current_scope == "XOnChain":
                pass

    def generate_code(self, node):
        self.visit(node)
        return self.code


def parse_and_generate_code(input_code):
    tree = ast.parse(input_code)
    annotated_tree = AnnotationTransformer().visit(tree)
    code_generator = PyTealCodeGenerator()
    return code_generator.generate_code(annotated_tree)
