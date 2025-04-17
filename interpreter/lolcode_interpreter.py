from lexer.lolcode_lexer import *
from .runtime import *
from .values import *
from parser.nodes import *

#######################################
# INTERPRETER
#######################################
class Interpreter:
  def visit(self, node, context):
    method_name = f'visit_{type(node).__name__}'
    method = getattr(self, method_name, self.no_visit_method)
    return method(node, context)
  
  def no_visit_method(self, node, context):
    raise Exception(f'No visit_{type(node).__name__} method defined')
  
  def visit_IntegerNode(self, node, context):
    # print("Found integer node")
    return RTResult().success(
      Number(int(node.token[TOKEN_VALUE]), node.token[TOKEN_LINE_NUMBER])
    )
  
  def visit_FloatNode(self, node, context):
    # print("Found float node")
    return RTResult().success(
      Number(float(node.token[TOKEN_VALUE]), node.token[TOKEN_LINE_NUMBER])
    )
  
  def visit_BooleanNode(self, node, context):
    # print("Found boolean node")
    return RTResult().success(
      Boolean(node.token[TOKEN_VALUE], node.token[TOKEN_LINE_NUMBER])
    )
  
  def visit_StringNode(self, node, context):
    # print("Found string node")
    return RTResult().success(
      String(node.token[TOKEN_VALUE], node.token[TOKEN_LINE_NUMBER])
    )
  
  def visit_NoobNode(self, node, context):
    return RTResult().success(
      Noob(node.line_number)
    )    
  
  def visit_ArithmeticBinaryOpNode(self, node, context):
    # print("Found ar bin op node")
    res = RTResult()
    left = res.register(self.visit(node.left_node, context))
    if res.error: return res
    right = res.register(self.visit(node.right_node, context))
    if res.error: return res

    if node.operation[TOKEN_TAG] == SUM_OF:
      result, error = left.added_by(right)

    elif node.operation[TOKEN_TAG] == DIFF_OF:
      result, error = left.subtracted_by(right)
    
    elif node.operation[TOKEN_TAG] == PRODUKT_OF:
      result, error = left.multiplied_by(right) 

    elif node.operation[TOKEN_TAG] == QUOSHUNT_OF:
      result, error = left.divided_by(right)

    elif node.operation[TOKEN_TAG] == MOD_OF:
      result, error = left.modulo(right)
    
    elif node.operation[TOKEN_TAG] == BIGGR_OF:
      result, error = left.maximum(right)
    
    elif node.operation[TOKEN_TAG] == SMALLR_OF:
      result, error = left.minimum(right)

    if (error):
      return res.failure(error)
    else:
      # context.symbol_table.set('IT', result)
      return res.success(result)

  def visit_BooleanBinaryOpNode(self, node, context):
    # print("Found bool bin op node")
    res = RTResult()
    left = res.register(self.visit(node.left_node, context))
    if res.error: return res
    right = res.register(self.visit(node.right_node, context))
    if res.error: return res

    if node.operation[TOKEN_TAG] == BOTH_OF:
      result, error = left.and_logic(right)

    elif node.operation[TOKEN_TAG] == EITHER_OF:
      result, error = left.or_logic(right)
    
    elif node.operation[TOKEN_TAG] == WON_OF:
      result, error = left.xor_logic(right) 

    if (error): return res.failure(error)
    else: return res.success(result)

  def visit_BooleanUnaryOpNode(self, node, context):
    res = RTResult()
    operand_ = res.register(self.visit(node.operand, context))
    if res.error: return res

    if (node.operation[TOKEN_TAG] == NOT):
      result, error = operand_.not_logic()

    if (error): return res.failure(error)
    else: return res.success(result)

  def visit_BooleanTernaryOpNode(self, node, context):
    res = RTResult()
    value = None
    boolean_results = []
    for boolean_statement in node.boolean_statements:
      boolean_result = res.register(self.visit(boolean_statement, context))
      if res.error: return res
      boolean_results.append(boolean_result)
    
    if node.operation[TOKEN_TAG] == ALL_OF:
      value = Boolean(all(boolean_results))
    elif node.operation[TOKEN_TAG] == ANY_OF:
      value = Boolean(any(boolean_results))

    return res.success(value)

  def visit_ComparisonOpNode(self, node, context):
    # print("Found comparison op node")
    res = RTResult()
    left = res.register(self.visit(node.left_node, context))
    if res.error: return res
    right = res.register(self.visit(node.right_node, context))
    if res.error: return res

    if node.operation[TOKEN_TAG] == BOTH_SAEM:
      result, error = left.is_equal(right)

    elif node.operation[TOKEN_TAG] == DIFFRINT:
      result, error = left.is_not_equal(right)

    if (error): return res.failure(error)
    else: return res.success(result)

  def visit_StringConcatNode(self, node, context):
    res = RTResult()
    string_value = ""

    for operand in node.operands:
      operand_value = res.register(self.visit(operand, context))
      if res.error: return res

      # Perform typecasting
      # Old
      # operand_value, error = operand_value.typecast(String)
      # if error:
      #   res.error = error
      #   return res

      string_value += str(operand_value.value)
    
    return res.success(string_value)

  def visit_VarAccessNode(self, node, context):
    res = RTResult()
    var_name = node.var_name_token[TOKEN_VALUE]

    if not context.symbol_table.found(var_name):
      return res.failure(RuntimeError(node.var_name_token, f"'{var_name} is not defined!'"))
    
    value = context.symbol_table.get(var_name)
    return res.success(value)

  def visit_VarDeclarationNode(self, node, context):
    res = RTResult()
    var_name = node.var_name_token[TOKEN_VALUE]

    # Not needed because of NOOB class
    # if node.value_node is None: 
    #   context.symbol_table.set(var_name, None)
    #   return res.success(None)

    value = res.register(self.visit(node.value_node, context))
    if res.error: return res

    context.symbol_table.set(var_name, value)
    return res.success(value)

  def visit_VarAssignmentNode(self, node, context):
    res = RTResult()
    
    var_to_access = node.var_to_access[TOKEN_VALUE]
    value_to_assign = res.register(self.visit(node.value_to_assign, context))

    if not context.symbol_table.found(var_to_access):
      return res.failure(RuntimeError(node.var_name_token, f"'{var_to_access} is not defined!'"))

    context.symbol_table.set(var_to_access, value_to_assign)
    return res.success(value_to_assign)

  def visit_StatementListNode(self, node, context):
    res = RTResult()
    for statement in node.statements:
      implicit_value = res.register(self.visit(statement, context))
      if res.error: return res
      context.symbol_table.set('IT', implicit_value)  # update the IT variable
    return res.success(None)
  
  def visit_VarDecListNode(self, node, context):
    res = RTResult()
    for variable_declaration in node.variable_declarations:
        variable = res.register(self.visit(variable_declaration, context))
        if res.error: return res
    return res.success(None)

  def visit_PrintNode(self, node, context):
    res = RTResult()
    print_value = ""

    for operand in node.operands:
      operand_value = res.register(self.visit(operand, context))
      if res.error: return res
      print_value += str(operand_value)
    
    print(print_value)

    return res.success(print_value)

  def visit_TypecastNode(self, node, context):
    res = RTResult()

    source_value = res.register(self.visit(node.source_value, context))
    if res.error: return res

    desired_type = node.desired_type

    if desired_type == "NUMBR":       # Int
      converted_value, error = source_value.explicit_typecast(Number)
    elif desired_type == "NUMBAR":    # Float
      converted_value, error = source_value.explicit_typecast(Number, True)
    elif desired_type == "TROOF":    # Float
      converted_value, error = source_value.explicit_typecast(Boolean)  
    elif desired_type == "YARN":    # Float
      converted_value, error = source_value.explicit_typecast(Boolean)  

    if error: return res.failure(error)

    return res.success(converted_value)

  def visit_SwitchCaseNode(self, node, context):
    res = RTResult()
    is_there_a_true_case = False
    basis = context.symbol_table.get('IT')

    for i in range(len(node.cases)):
      case_value = res.register(self.visit(node.cases[i], context))
      if res.error: return res

      condition, error = basis.is_equal(case_value)
      if error: return res.failure(error)
      
      # print(condition, condition.value==True)

      if (condition.value):
        for statement in node.cases_statements[i]:
          statement_value = res.register(self.visit(statement, context))
          if res.error: return res

          if isinstance(statement_value, Break):
            is_there_a_true_case = True
            break

        # loop end
        is_there_a_true_case = True
        break
    
    if is_there_a_true_case == False:
      for statement in node.default_case_statements:
        statement_value = res.register(self.visit(statement, context))
        if res.error: return res

    return res.success(basis)

  def visit_IfNode(self, node, context):
    res = RTResult()
    basis = context.symbol_table.get('IT')

    basis_value, error = basis.typecast(Boolean)
    if error: return res.failure(error)

    if (basis_value.value):
      for statement in node.if_block_statements:
        statement_value = res.register(self.visit(statement, context))
        if res.error: return res
    else:
      for statement in node.else_block_statements:
        statement_value = res.register(self.visit(statement, context))
        if res.error: return res

    return res.success(basis)
  
  def visit_LoopNode(self, node, context):
    res = RTResult()

    label = node.label
    operation = node.operation
    variable = node.variable
    til_wile_expression = node.til_wile_expression
    body_statements = node.body_statements

    termination_condition = None

    is_running = True
    while is_running:
      # termination_condition = None
      if (til_wile_expression != None):
        termination_condition = res.register(self.visit(til_wile_expression, context))
        if res.error: return res

      if (termination_condition is not None and termination_condition.value):
        break

      for statement in body_statements:
        statement_value = res.register(self.visit(statement, context))
        if res.error: return res

        if isinstance(statement_value, Break):
          is_running = False
          break
      
      # Incrementor/Decrementor
      iterator = res.register(self.visit(VarAccessNode(variable), context))
      if iterator is None: return res
      if operation[TOKEN_TAG] == UPPIN:
        iterator.value += 1
      else:
        iterator.value -= 1
      
      res.register(self.visit(VarAssignmentNode(variable, IntegerNode((iterator.value, None, variable[TOKEN_LINE_NUMBER]))), context))

    return res.success(label)

  def visit_FuncDefNode(self, node, context):
    res = RTResult()
    return_value = None

    function_name = node.function_name[TOKEN_VALUE]
    params = []

    # if there's any
    for param in node.parameters:
      param_name = param.var_name_token[TOKEN_VALUE]
      params.append(param_name)

    body_statements = node.body_statements
    
    function_value = Function(function_name, params, body_statements).set_context(context)
    
    context.symbol_table.set(function_name, function_value)
    return res.success(function_value)

  def visit_FuncCallNode(self, node, context):
    res = RTResult()
    return_value = Noob()
    parameters_to_pass = []

    function_name = node.function_name
    parameters = node.parameters

    function_to_call = res.register(self.visit(function_name, context))
    if res.error: return res

    for param in parameters:
      par = res.register(self.visit(param, context))
      if res.error: return res

      parameters_to_pass.append(par)

    return_value = function_to_call.execute(parameters_to_pass)
    return res.success(return_value.value)

  def visit_InputNode(self, node, context):
    res = RTResult()
    variable = node.variable

    if context.symbol_table.found(variable.var_name_token[TOKEN_VALUE]):
      user_input = String(input("Enter input: "))
      value = res.register(self.visit(VarAssignmentNode(variable.var_name_token, user_input), context))
    else:
      res.failure(RuntimeError(
        ('Var Access Error', None, variable.var_name_token[TOKEN_LINE_NUMBER]), "Can't find var"
      ))

    return res.success(value)

  def visit_BreakNode(self, node, context):
    res = RTResult()
    break_token = node.break_token
    return_value = Break(break_token[TOKEN_VALUE]).set_context(context)
    return res.success(return_value)

  def visit_ProgramNode(self, node, context):
    res = RTResult()
    for section in node.sections:
        section_ = res.register(self.visit(section, context))
        if res.error: return res
    return res.success(None)

