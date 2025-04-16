from lexer import *

# ═════════════════════════════════════════════════════════════════════════════════════════════════
class Error:
  def __init__(self, token, details, error_name):
    self.token = token
    self.details = details
    self.error_name = error_name
  def as_string(self):
    return f"{self.error_name}: '{self.token[TOKEN_VALUE]}' at line {self.token[TOKEN_LINE_NUMBER]}\nDetails: {self.details}\n"

class InvalidSyntaxError(Error):
  def __init__(self, token, details):
    super().__init__(token, details, error_name='Invalid Syntax')

class RuntimeError(Error):
  def __init__(self, token, details):
    super().__init__(token, details, error_name='Runtime Error')

# ═════════════════════════════════════════════════════════════════════════════════════════════════
# NODES
# ═════════════════════════════════════════════════════════════════════════════════════════════════
class IntegerNode:
  def __init__(self, token):
    self.token = token

  def __repr__(self):
    return f'{self.token[TOKEN_VALUE]}'

class FloatNode:
  def __init__(self, token):
    self.token = token

  def __repr__(self):
    return f'{self.token[TOKEN_VALUE]}'
  
class BooleanNode:
  def __init__(self, token):
    self.token = token

  def __repr__(self):
    return f'{self.token[TOKEN_VALUE]}'
  
class StringNode:
  def __init__(self, token):
    self.token = (str(token[TOKEN_VALUE][1:-1]), token[TOKEN_TAG], token[TOKEN_LINE_NUMBER])

  def __repr__(self):
    return f'"{self.token[TOKEN_VALUE]}"'

class NoobNode:
  def __init__(self, line_number=None):
    self.line_number = line_number

  def __repr__(self):
    return f"NOOB"

class StringConcatNode:
  def __init__(self, operands):
    self.operands = operands

  def __repr__(self):
    return f"StringConcatenation({self.operands})"
  
class ArithmeticBinaryOpNode:
  def __init__(self, left_node, operation, right_node):
    self.operation = operation
    self.left_node = left_node
    self.right_node = right_node

  def __repr__(self):
    return f'{self.operation[TOKEN_VALUE]}({self.left_node}, {self.right_node})'

class BooleanBinaryOpNode:
  def __init__(self, left_node, operation, right_node):
    self.operation = operation
    self.left_node = left_node
    self.right_node = right_node

  def __repr__(self):
    return f'{self.operation[TOKEN_VALUE]}({self.left_node}, {self.right_node})' 

class BooleanUnaryOpNode:
  def __init__(self, operation, operand):
    self.operation = operation
    self.operand = operand

  def __repr__(self):
    return f'{self.operation[TOKEN_VALUE]}({self.operand})'
  
class BooleanTernaryOpNode:
  def __init__(self, operation, boolean_statements):
    self.operation = operation
    self.boolean_statements = boolean_statements

  def __repr__(self):
    return f"{self.operation}({self.boolean_statements})"

class ComparisonOpNode:
  def __init__(self, left_node, operation, right_node):
    self.operation = operation
    self.left_node = left_node
    self.right_node = right_node

  def __repr__(self):
    return f'{self.operation[TOKEN_VALUE]}({self.left_node}, {self.right_node})' 

class VarAccessNode:
  def __init__(self, var_name_token):
    self.var_name_token = var_name_token

  def __repr__(self):
    return f"VarAccess({self.var_name_token[TOKEN_VALUE]})"

class VarDeclarationNode:
  def __init__(self, var_name_token, value_node):
    self.var_name_token = var_name_token
    self.value_node = value_node

  def __repr__(self):
    return f"VarDeclare({self.var_name_token[TOKEN_VALUE]}, {self.value_node})"

class VarAssignmentNode:
  def __init__(self, var_to_access, value_to_assign):
    self.var_to_access = var_to_access
    self.value_to_assign = value_to_assign

  def __repr__(self):
    return f"VarAssign({self.var_to_access[TOKEN_VALUE]}, {self.value_to_assign})"

class StatementListNode:
  def __init__(self, statements):
    self.statements = statements

  def __repr__(self):
    return f"StatementList({self.statements})"

class VarDecListNode:
  def __init__(self, variable_declarations):
    self.variable_declarations = variable_declarations

  def __repr__(self):
    return f"VarDecListNode({self.variable_declarations})"

class PrintNode:
  def __init__(self, operands):
    self.operands = operands
  
  def __repr__(self):
    return f"PrintNode({self.operands})"

class TypecastNode:
  def __init__(self, source_value, desired_type):
    self.source_value = source_value
    self.desired_type = desired_type

  def __repr__(self):
    return f"{self.desired_type}({self.source_value})"

class SwitchCaseNode:
  def __init__(self, cases, cases_statements, default_case_statements):
    self.cases = cases
    self.cases_statements = cases_statements
    self.default_case_statements = default_case_statements

  def __repr__(self):
    return f"SwitchCases({self.cases_statements})"

class IfNode:
  def __init__(self, if_block_statements, else_block_statements):
    self.if_block_statements = if_block_statements
    self.else_block_statements = else_block_statements

  def __repr__(self):
    return f"IfElse({self.if_block_statements}, {self.else_block_statements})"

class LoopNode:
  def __init__(self, label, operation, variable, til_wile_expression, body_statements):
    self.label = label
    self.operation = operation
    self.variable = variable
    self.til_wile_expression = til_wile_expression
    self.body_statements = body_statements

  def __repr__(self):
    return f"Loop({self.label}, {self.operation[TOKEN_VALUE]}, {self.variable}, {self.til_wile_expression}, {self.body_statements})"

class FuncDefNode:
  def __init__(self, function_name, parameters, body_statements):
    self.function_name = function_name
    self.parameters = parameters
    self.body_statements = body_statements

  def __repr__(self):
    return f"FuncDef({self.function_name}, {self.parameters})"

class FuncCallNode:
  def __init__(self, function_name, parameters):
    self.function_name = function_name
    self.parameters = parameters

  def __repr__(self):
    return f"FuncCall({self.function_name}, {self.parameters})"

class InputNode:
  def __init__(self, variable):
    self.variable = variable

  def __repr__(self):
    return f"StoreTo({self.variable})"

class BreakNode:
  def __init__(self, break_token):
    self.break_token = break_token

  def __repr__(self):
    return f"BREAK"

class ProgramNode:
  def __init__(self, sections):
    self.sections = sections

  def __repr__(self):
    return f"ProgramNode({self.sections})"
  

# ═════════════════════════════════════════════════════════════════════════════════════════════════
# PARSE RESULT
# ═════════════════════════════════════════════════════════════════════════════════════════════════
class ParseResult:
  def __init__(self):
    self.error = None
    self.node = None
    self.advance_count = 0

  def register_advancement(self):
    self.advance_count += 1

  def register(self, res):
    self.advance_count += res.advance_count
    if res.error: self.error = res.error
    return res.node

  def success(self, node):
    self.node = node
    return self

  def failure(self, error):
    if self.error is None: self.error = error
    return self
  
# ═════════════════════════════════════════════════════════════════════════════════════════════════
# PARSER
# ═════════════════════════════════════════════════════════════════════════════════════════════════
class Parser:
  def __init__(self, tokens):
    self.tokens = tokens
    self.token_index = -1
    self.advance()

  def advance(self):
    self.token_index += 1
    if (self.token_index < len(self.tokens)):
      self.current_token = self.tokens[self.token_index]
    return self.current_token

  def parse(self):
    res = ParseResult()
    sections = []

    if (self.current_token[TOKEN_TAG] != HAI):
      return res.failure(InvalidSyntaxError(self.current_token, "Expected a 'HAI' Keyword!"))

    res.register_advancement() # Eat HAI
    self.advance()

    # Check if there's a variable section
    if self.current_token[TOKEN_TAG] == WAZZUP:
      res.register_advancement()  # Eat Wazzup
      self.advance()

      variable_declaration_section =  res.register(self.variable_section())
      if variable_declaration_section is None: return res   # Check if there's an error
      sections.append(variable_declaration_section)         # No error

    # try to parse statements
    list_of_statements = res.register(self.statement_list())
    if list_of_statements is None: return res               # Check if there's an error
    sections.append(list_of_statements)                     # No error
    
    return res.success(ProgramNode(sections))

# ═════════════════════════════════════════════════════════════════════════════════════════════════
  def variable_section(self):
    res = ParseResult()
    variable_declarations = []

    while (self.current_token[TOKEN_TAG] != BUHBYE and self.current_token != self.tokens[-1]):
      variable_declaration = res.register(self.variable_declaration())

      # Has error
      if variable_declaration is None:
        return res

      variable_declarations.append(variable_declaration)

    # Error
    if (self.current_token[TOKEN_TAG] != BUHBYE):
      return res.failure(InvalidSyntaxError(self.current_token, "Expected a 'BUHBYE' or keyword!"))
    
    # No error
    res.register_advancement()  # Eat BUHBYE
    self.advance()

    return res.success(VarDecListNode(variable_declarations))

  def variable_declaration(self):
    res = ParseResult()

    if self.current_token[TOKEN_TAG] == I_HAS_A:
      res.register_advancement()
      self.advance() # eats I has a

      if (self.current_token[TOKEN_TAG] != IDENTIFIER):
        return res.failure(InvalidSyntaxError(self.current_token, "Expected Identifier!"))

      var_name_token = self.current_token
      res.register_advancement()
      self.advance() # eats var name
      
      if (self.current_token[TOKEN_TAG] != ITZ):
        return res.success(VarDeclarationNode(var_name_token, NoobNode()))

      res.register_advancement()
      self.advance() # eats ITZ

      expression = res.register(self.expression())
      if res.error: return res

      return res.success(VarDeclarationNode(var_name_token, expression))

    return res.failure(InvalidSyntaxError(self.current_token, "Expected an 'I HAS A' or 'BUHBYE' Keyword!"))

  def variable_literal(self):
    res = ParseResult()
    token = self.current_token

    if token[TOKEN_TAG] == IDENTIFIER:
      res.register_advancement() # Eat
      self.advance()

      return res.success(VarAccessNode(token))

# ═════════════════════════════════════════════════════════════════════════════════════════════════
  def statement_list(self):
    res = ParseResult()
    statements = []

    while (self.current_token[TOKEN_TAG] != KTHXBYE and self.current_token !=self.tokens[-1]):
      statement = res.register(self.statement())

      # Has error
      if statement is None:
        return res

      statements.append(statement)

    if (self.current_token[TOKEN_TAG] != KTHXBYE):
      return res.failure(InvalidSyntaxError(self.current_token, "Expected an 'KTHXBYE' keyword!"))

    return res.success(StatementListNode(statements))

  def statement(self):
    res = ParseResult()
    
    res.node = res.register(self.assignment_statement())
    if res.error or res.node: return res    # Has an error or parsed correctly

    res.node = res.register(self.expression())
    if res.error or res.node: return res    # Has an error or parsed correctly

    res.node = res.register(self.print_statement())
    if res.error or res.node: return res    # Has an error or parsed correctly 

    res.node = res.register(self.switch_case_statement())
    if res.error or res.node: return res    # Has an error or parsed correctly 

    res.node = res.register(self.if_statement())
    if res.error or res.node: return res    # Has an error or parsed correctly 

    res.node = res.register(self.loop_statement())
    if res.error or res.node: return res    # Has an error or parsed correctly 

    res.node = res.register(self.function_definition())
    if res.error or res.node: return res    # Has an error or parsed correctly 

    res.node = res.register(self.function_call())
    if res.error or res.node: return res    # Has an error or parsed correctly 

    res.node = res.register(self.input_statement())
    if res.error or res.node: return res    # Has an error or parsed correctly 

    res.node = res.register(self.break_statement())
    if res.error or res.node: return res    # Has an error or parsed correctly   

    # Can't parse (skipped other statements)
    return res.failure(InvalidSyntaxError(self.current_token, 'Unexpected Syntax'))

# ═════════════════════════════════════════════════════════════════════════════════════════════════  
  def expression(self):
    res = ParseResult()

    if self.current_token[TOKEN_TAG] in (NUMBR, NUMBAR, YARN, TROOF, IDENTIFIER, NOOB):
      res.node = res.register(self.literal())

    elif self.current_token[TOKEN_TAG] in (PRODUKT_OF, QUOSHUNT_OF, SUM_OF, DIFF_OF, MOD_OF, BIGGR_OF, SMALLR_OF):
      res.node =  res.register(self.arithmetic_binary_operation())

    elif self.current_token[TOKEN_TAG] == SMOOSH:
      res.node = res.register(self.string_concatenation())

    elif self.current_token[TOKEN_TAG] in (BOTH_OF, EITHER_OF, WON_OF, NOT):
      res.node = res.register(self.boolean_expression())
    
    elif self.current_token[TOKEN_TAG] in (ALL_OF, ANY_OF):
      res.node = res.register(self.boolean_ternary_operation())

    elif self.current_token[TOKEN_TAG] in (BOTH_SAEM, DIFFRINT):
      res.node = res.register(self.comparison_operation())

    elif self.current_token[TOKEN_TAG] == MAEK_A:
      res.node = res.register(self.typecast())

    return res

# ═════════════════════════════════════════════════════════════════════════════════════════════════
  def literal(self):
    res = ParseResult()
    
    if self.current_token[TOKEN_TAG] in (NUMBR, NUMBAR):
      res.node = res.register(self.arithmetic_literal())
    
    elif self.current_token[TOKEN_TAG] == YARN:
      res.node = res.register(self.string_literal())
    
    elif self.current_token[TOKEN_TAG] == TROOF:
      res.node = res.register(self.boolean_literal())

    elif self.current_token[TOKEN_TAG] == IDENTIFIER:
      res.node = res.register(self.variable_literal())

    elif self.current_token[TOKEN_TAG] == NOOB:
      res.node = res.register(self.noob())

    return res

# ═════════════════════════════════════════════════════════════════════════════════════════════════
  def noob(self):
    res = ParseResult()
    token = self.current_token

    if token[TOKEN_TAG] == NOOB:
      res.register_advancement()  # Eat NOOB
      self.advance()

      return res.success(NoobNode(token[TOKEN_LINE_NUMBER]))

# ═════════════════════════════════════════════════════════════════════════════════════════════════
  def string_concatenation(self):
    res = ParseResult()
    operands = []

    if self.current_token[TOKEN_TAG] == SMOOSH:
      res.register_advancement()  # Eat SMOOSH
      self.advance()

      # Parse the first operand
      first_operand = res.register(self.expression())
      if res.error: return res        # Check for error
      operands.append(first_operand)  # Add to list

      while (self.current_token[TOKEN_TAG] == AN):
        res.register_advancement() # Eat 'AN'
        self.advance()

        additional_operand = res.register(self.expression())
        
        # Check for errors
        if additional_operand is None:
          return res.failure(InvalidSyntaxError(self.current_token, "Expected an additional operand!"))

        operands.append(additional_operand) # Add to list

      return res.success(StringConcatNode(operands))
    
  def string_literal(self):
    res = ParseResult()
    token = self.current_token

    if token[TOKEN_TAG] == YARN:
      res.register_advancement() # Eat
      self.advance()

      return res.success(StringNode(token))

    return res.failure(InvalidSyntaxError(token, 'Expected a string!'))

# ═════════════════════════════════════════════════════════════════════════════════════════════════  
  def arithmetic_binary_operation(self):
    res = ParseResult()
    
    # if self.current_token[TOKEN_TAG] in (PRODUKT_OF, QUOSHUNT_OF, SUM_OF, DIFF_OF, BIGGR_OF, SMALLR_OF):
    operation = self.current_token
    res.register_advancement()
    self.advance()
    
    # Parse the left operand
    left = res.register(self.arithmetic_expression())  # Recursive call to handle the left side
    if res.error: return res

    # check for 'AN' keyword 
    if self.current_token[TOKEN_TAG] != AN:
        # print(self.current_token[TOKEN_VALUE])
        return res.failure(InvalidSyntaxError(self.current_token, "Expected an 'AN' keyword!"))
        
    # Advance past the 'AN' keyword
    res.register_advancement()
    self.advance()

    # Parse the right operand which may also be an expression
    right = res.register(self.arithmetic_expression())  # Recursive call to handle right side
    if res.error: return res

    # Return an operation node with left and right operands
    return res.success(ArithmeticBinaryOpNode(left, operation, right))

  def arithmetic_expression(self):
    res = ParseResult()
    token = self.current_token

    if token[TOKEN_TAG] in (NUMBR, NUMBAR, YARN, TROOF, IDENTIFIER):
      res.node = res.register(self.literal())
    
    elif token[TOKEN_TAG] in (PRODUKT_OF, QUOSHUNT_OF, SUM_OF, MOD_OF, DIFF_OF, BIGGR_OF, SMALLR_OF):
      res.node = res.register(self.arithmetic_binary_operation())
    
    return res

  def arithmetic_literal(self):
    res = ParseResult()
    token = self.current_token

    if token[TOKEN_TAG] in (NUMBR, NUMBAR):
      res.register_advancement()
      self.advance()
      
      if token[TOKEN_TAG] == NUMBR:
        return res.success(IntegerNode(token))
      else:
        return res.success(FloatNode(token))
    
    return res.failure(InvalidSyntaxError(token, 'Expected int or float!'))

# ═════════════════════════════════════════════════════════════════════════════════════════════════
  def boolean_expression(self):
    res = ParseResult()

    if self.current_token[TOKEN_TAG] in (BOTH_OF, EITHER_OF, WON_OF):
      res.node = res.register(self.boolean_binary_operation())
    
    elif self.current_token[TOKEN_TAG] == NOT:
      res.node = res.register(self.boolean_unary_operation())
    
    elif self.current_token[TOKEN_TAG] in (NUMBR, NUMBAR, YARN, TROOF, IDENTIFIER):
      res.node = res.register(self.literal())

    return res

  def boolean_ternary_operation(self):
    res = ParseResult()
    boolean_statements = []

    if self.current_token[TOKEN_TAG] in (ALL_OF, ANY_OF):
      operation = self.current_token
      res.register_advancement() # Eat
      self.advance()

      # Parse the first operand
      first_operand = res.register(self.boolean_expression())
      if res.error: return res # Check for error
      boolean_statements.append(first_operand) # Add to list

      while (self.current_token[TOKEN_TAG] == AN):
        res.register_advancement() # Eat 'AN'
        self.advance()

        additional_operand = res.register(self.boolean_expression())
        
        # Check for errors
        if additional_operand is None:
          return res.failure(InvalidSyntaxError(self.current_token, "Expected an additional operand!"))

        boolean_statements.append(additional_operand) # Add to list

      if (self.current_token[TOKEN_TAG] != MKAY):
        return res.failure(InvalidSyntaxError(self.current_token, "Expected an 'MKAY' keyword!"))
      
      # If there's 'MKAY', eat it
      res.register_advancement()
      self.advance()

      return res.success(BooleanTernaryOpNode(operation, boolean_statements))

  def boolean_binary_operation(self):
    res = ParseResult()

    if self.current_token[TOKEN_TAG] in (BOTH_OF, EITHER_OF, WON_OF):
      operation = self.current_token
      res.register_advancement() # Eat
      self.advance()
      print(operation)
      # Parse the left operand
      left = res.register(self.boolean_expression())
      if res.error: return res

      # Check for 'AN' keyword 
      if self.current_token[TOKEN_TAG] != AN:
          return res.failure(InvalidSyntaxError(self.current_token, "Expected an 'AN' keyword!"))
          
      # Advance past the 'AN' keyword
      res.register_advancement()
      self.advance()

      # Parse the right operand
      right = res.register(self.boolean_expression())
      if res.error: return res

      # Return an operation node with left and right operands
      return res.success(BooleanBinaryOpNode(left, operation, right))

  def boolean_unary_operation(self):
    res = ParseResult()

    if self.current_token[TOKEN_TAG] == NOT:
      operation = self.current_token
      res.register_advancement() # Eat
      self.advance()

      # Parse the operand
      operand = res.register(self.boolean_expression())
      if res.error: return res

      return res.success(BooleanUnaryOpNode(operation, operand))

  def boolean_literal(self):
    res = ParseResult()
    token = self.current_token

    if token[TOKEN_TAG] in (TROOF):
      res.register_advancement() # Eat
      self.advance()
      
      return res.success(BooleanNode(token))
    
    # Error    
    return res.failure(InvalidSyntaxError(token, 'Expected boolean!'))
  
# ═════════════════════════════════════════════════════════════════════════════════════════════════
  def comparison_operation(self):
    res = ParseResult()
    token = self.current_token

    if token[TOKEN_TAG] in (BOTH_SAEM, DIFFRINT):
      operation = self.current_token
      res.register_advancement() # Eat
      self.advance()

      # Parse the left operand
      left = res.register(self.expression())
      if res.error: return res

      # Check for 'AN' keyword 
      if self.current_token[TOKEN_TAG] != AN:
          return res.failure(InvalidSyntaxError(self.current_token, "Expected an 'AN' keyword!"))
    
      # Advance past the 'AN' keyword
      res.register_advancement()
      self.advance()

      # Parse the right operand
      # Check if there is BIGGR OF or SMALLR OF keywords
      if self.current_token[TOKEN_TAG] in (BIGGR_OF, SMALLR_OF):
        right = res.register(self.arithmetic_binary_operation())

        # There's an error
        if right is None:
          return res
      
      else:
        right = res.register(self.expression())
        if res.error: return res

      # Return an operation node with left and right operands
      return res.success(ComparisonOpNode(left, operation, right))

# ═════════════════════════════════════════════════════════════════════════════════════════════════
  def print_statement(self):
    res = ParseResult()
    operands = []

    if self.current_token[TOKEN_TAG] == VISIBLE:
      res.register_advancement()  # Eat VISIBLE
      self.advance()

      # Parse the first operand
      first_operand = res.register(self.expression())
      if res.error: return res        # Check for error
      operands.append(first_operand)  # Add to list

      while (self.current_token[TOKEN_TAG] in (VISIBLE_OPERATOR, AN)):
        res.register_advancement() # Eat '+'
        self.advance()

        additional_operand = res.register(self.expression())
        
        # Check for errors
        if additional_operand is None:
          return res.failure(InvalidSyntaxError(self.current_token, "Expected an additional operand!"))

        operands.append(additional_operand) # Add to list

      return res.success(PrintNode(operands))
  
    return res

# ═════════════════════════════════════════════════════════════════════════════════════════════════
  def typecast(self):
    res = ParseResult()

    if self.current_token[TOKEN_TAG] == MAEK_A:
      res.register_advancement()  # Eat MAEK A
      self.advance()

      # Parse the value to typecast
      source_value = res.register(self.expression()) # Don't know if var only so Ii set it to expression instead
        
      # Check for errors
      if source_value is None:
        return res.failure(InvalidSyntaxError(self.current_token, "Expected a value to typecast!"))

      if self.current_token[TOKEN_VALUE] in ("NUMBAR", "NUMBR", "YARN", "TROOF"):
        desired_type = self.current_token[TOKEN_VALUE]

        res.register_advancement()  # Desired type
        self.advance()

        return res.success(TypecastNode(source_value, desired_type))
      else:
        return res.failure(InvalidSyntaxError(self.current_token, "Expected a type to cast the value!"))

    return res

# ═════════════════════════════════════════════════════════════════════════════════════════════════
  def assignment_statement(self):
    res = ParseResult()

    if self.current_token[TOKEN_TAG] == IDENTIFIER:
      var_to_access = self.current_token

      res.register_advancement()  # Eat Variable Identifier
      self.advance()

      # Check for 'R' keyword 
      if self.current_token[TOKEN_TAG] not in (R, IS_NOW_A):
        # If there's no R or IS NOW A, then it might just be a variable access
        return res.success(VarAccessNode(var_to_access))


      # Else, continue
      if self.current_token[TOKEN_TAG] == R:
        res.register_advancement()  # Eat R
        self.advance()

        value_to_assign = res.register(self.expression())

        # Check for errors
        if value_to_assign is None:
          return res.failure(InvalidSyntaxError(self.current_token, "Expected a value to assign!"))

        return res.success(VarAssignmentNode(var_to_access, value_to_assign))
      
      # Var assignment with TYPECASTING
      elif self.current_token[TOKEN_TAG] == IS_NOW_A:
        res.register_advancement()  # Eat IS NOW A
        self.advance()

        if self.current_token[TOKEN_VALUE] not in ("NUMBAR", "NUMBR", "YARN", "TROOF"):
          return res.failure(InvalidSyntaxError(self.current_token, "Expected a type to cast the value!"))

        # Else, continue
        desired_type = self.current_token[TOKEN_VALUE]

        res.register_advancement()  # Eat the desired type
        self.advance()

        return res.success(VarAssignmentNode(var_to_access, TypecastNode(VarAccessNode(var_to_access), desired_type)))

    return res

# ═════════════════════════════════════════════════════════════════════════════════════════════════
  # TODO: GIMMEH
  def input_statement(self):
    res = ParseResult()

    if self.current_token[TOKEN_TAG] == GIMMEH:
      res.register_advancement() # Eat Gimmeh
      self.advance()

      # Error
      if self.current_token[TOKEN_TAG] != IDENTIFIER:
        return res.failure(InvalidSyntaxError(self.current_token, "Expected a variable to store input!"))
      
      variable = res.register(self.variable_literal())
      if variable is None: return res # Error

      # Get user input
      user_input_value = str(input("Enter a value: "))
      user_input_value = " " + user_input_value + " "
      user_input = StringNode((user_input_value, None, self.current_token[TOKEN_LINE_NUMBER]))
      return res.success(VarAssignmentNode(variable.var_name_token, user_input))

    return res

# ═════════════════════════════════════════════════════════════════════════════════════════════════
  # TODO: GTFO
  def break_statement(self):
    res = ParseResult()

    if self.current_token[TOKEN_TAG] == GTFO:
      break_token = self.current_token
      res.register_advancement() # Eat GTFO
      self.advance()
      
      return res.success(BreakNode(break_token))

    return res

# ═════════════════════════════════════════════════════════════════════════════════════════════════
  def if_statement(self):
    res = ParseResult()
    if_block_statements = []
    else_block_statements = []
    if self.current_token[TOKEN_TAG] == O_RLY:
      res.register_advancement() # Eat O RLY?
      self.advance()

      # Error
      if self.current_token[TOKEN_TAG] != YA_RLY:
        return res.failure(InvalidSyntaxError(self.current_token, "Expected an 'YA RLY' keyword!"))

      res.register_advancement() # Eat YA RLY
      self.advance()

      while self.current_token[TOKEN_TAG] not in (NO_WAI, OIC, KTHXBYE):
        statement = res.register(self.statement())

        # Has error
        if statement is None:
          return res

        if_block_statements.append(statement)

      # No Else
      if self.current_token[TOKEN_TAG] != NO_WAI:
        # Check for OIC
        if self.current_token[TOKEN_TAG] == OIC:
          res.register_advancement() # Eat OIC
          self.advance()
          return res.success(IfNode(if_block_statements, else_block_statements))
        
        # Error
        return res.failure(InvalidSyntaxError(self.current_token, "Expected a 'NO WAI' keyword!"))
        
      
      res.register_advancement() # Eat NO WAI
      self.advance()

      while self.current_token[TOKEN_TAG] not in (OIC, KTHXBYE):
        statement = res.register(self.statement())

        # Has error
        if statement is None:
          return res

        else_block_statements.append(statement)
      
      # Error
      if self.current_token[TOKEN_TAG] != OIC:
        return res.failure(InvalidSyntaxError(self.current_token, "Expected a 'NO WAI' keyword!"))
      
      res.register_advancement() # Eat OIC
      self.advance()
      
      return res.success(IfNode(if_block_statements, else_block_statements))
    return res



# ═════════════════════════════════════════════════════════════════════════════════════════════════
  def switch_case_statement(self):
    res = ParseResult()
    cases = []
    cases_statements = []
    default_case_statements = []

    if self.current_token[TOKEN_TAG] == WTF:
      res.register_advancement() # Eat WTF
      self.advance()
      
      # Error
      if self.current_token[TOKEN_TAG] != OMG:
        return res.failure(InvalidSyntaxError(self.current_token, "Expected an 'OMG' keyword!"))

      while self.current_token[TOKEN_TAG] == OMG:
        statements = []

        res.register_advancement() # Eat OMG
        self.advance()

        # Error
        if self.current_token[TOKEN_TAG] not in (NUMBR, NUMBAR, YARN, TROOF, IDENTIFIER, NOOB):
          return res.failure(InvalidSyntaxError(self.current_token, "Expected a literal for switch case!"))

        # Eat 
        case_condition = res.register(self.literal())

        # Has error
        if case_condition is None:
          return res

        while self.current_token[TOKEN_TAG] not in (OMG, OMGWTF, OIC, KTHXBYE):
          statement = res.register(self.statement())

          # Has error
          if statement is None:
            return res

          statements.append(statement)
        # Loop end
      
        cases.append(case_condition)
        cases_statements.append(statements)
      # Loop end

      if self.current_token[TOKEN_TAG] != OMGWTF:
        return res.failure(InvalidSyntaxError(self.current_token, "Expected a default case for switch case!"))

      # Eat OMGWTF
      res.register_advancement()
      self.advance()

      # add switch case
      while self.current_token[TOKEN_TAG] not in (OIC, KTHXBYE):
        statement = res.register(self.statement())

        # Has error
        if statement is None:
          return res

        default_case_statements.append(statement)

      if self.current_token[TOKEN_TAG] != OIC:
        return res.failure(InvalidSyntaxError(self.current_token, "Expected an 'OIC' keyword!"))

      # Eat OIC
      res.register_advancement()
      self.advance()

      return res.success(SwitchCaseNode(cases, cases_statements, default_case_statements))

    return res

# ═════════════════════════════════════════════════════════════════════════════════════════════════
  def loop_statement(self):
    res = ParseResult()
    label = None
    operation = None
    variable = None
    til_wile_expression = None
    body_statements = []

    if self.current_token[TOKEN_TAG] == IM_IN_YR:
      res.register_advancement() # Eat IM IN YR
      self.advance()

      if self.current_token[TOKEN_TAG] != IDENTIFIER:
        return res.failure(InvalidSyntaxError(self.current_token, "Expected a label for the loop!"))
      
      label = self.current_token[TOKEN_VALUE]
      res.register_advancement() # Eat label
      self.advance()


      if self.current_token[TOKEN_TAG] not in (UPPIN, NERFIN):
        return res.failure(InvalidSyntaxError(self.current_token, "Expected an operation for the loop condition!"))
      
      # Else, no error
      operation = self.current_token
      res.register_advancement() # Eat UPPIN or NERFIN
      self.advance()

      if self.current_token[TOKEN_TAG] != YR:
        return res.failure(InvalidSyntaxError(self.current_token, "Expected a 'YR' keyword for the loop!"))
      
      # Else, no error
      res.register_advancement() # Eat YR
      self.advance()

      # Var
      if self.current_token[TOKEN_TAG] != IDENTIFIER:
        return res.failure(InvalidSyntaxError(self.current_token, "Expected a variable for the loop!"))

      # variable = res.register(self.variable_literal())

      # # Has error
      # if variable is None:
      #   return res    
      variable = self.current_token
      res.register_advancement() # Eat variable
      self.advance()


      # TIL/WILE
      if self.current_token[TOKEN_TAG] in (TIL, WILE):
        res.register_advancement() # Eat TIL or WILE
        self.advance()

        til_wile_expression = res.register(self.expression())

        # Has error
        if til_wile_expression is None:
          return res
        
      # Loop body
      while self.current_token[TOKEN_TAG] not in (IM_OUTTA_YR, KTHXBYE):
        statement = res.register(self.statement())

        # Has error
        if statement is None:
          return res

        body_statements.append(statement)
      
      # Loop out
      if self.current_token[TOKEN_TAG] != IM_OUTTA_YR:
        return res.failure(InvalidSyntaxError(self.current_token, "Expected an 'IM OUTTA YR' keyword!"))

      # Eat IM OUTTA YR
      res.register_advancement()
      self.advance()

      
      if self.current_token[TOKEN_TAG] != IDENTIFIER:
        return res.failure(InvalidSyntaxError(self.current_token, "Expected a label to exit the loop!"))

      out_label = self.current_token[TOKEN_VALUE]
      res.register_advancement() # Eat label
      self.advance()

      print(label, out_label)
      if label != out_label:
        return res.failure(InvalidSyntaxError(self.current_token, "Expected a similar label to exit the loop!"))
      
      
      return res.success(LoopNode(label, operation, variable, til_wile_expression, body_statements))
    
    return res

# ═════════════════════════════════════════════════════════════════════════════════════════════════
  def function_definition(self):
    res = ParseResult()
    function_name = None
    parameters = []
    body_statements = []

    if self.current_token[TOKEN_TAG] == HOW_IZ_I:
      res.register_advancement() # Eat HOW IZ I
      self.advance()

      # Identifier
      if self.current_token[TOKEN_TAG] != IDENTIFIER:
        return res.failure(InvalidSyntaxError(self.current_token, "Expected a valid function name!"))
      
      function_name = self.current_token
      res.register_advancement() # Eat function name
      self.advance()

      # Check if there are parameters
      if self.current_token[TOKEN_TAG] == YR:
        res.register_advancement() # Eat YR
        self.advance()

        first_param = res.register(self.expression())
        if first_param is None: return res # Has error

        parameters.append(first_param)

        # Check for other params if there are any
        while self.current_token[TOKEN_TAG] == AN_YR:
          res.register_advancement() # Eat AN YR
          self.advance()

          additional_param = res.register(self.expression())
          if additional_param is None: return res # Has error

          parameters.append(additional_param)

      # function body
      while self.current_token[TOKEN_TAG] not in (FOUND_YR, IF_U_SAY_SO, KTHXBYE):
        statement = res.register(self.statement())
        if statement is None: return res # Has error

        body_statements.append(statement)

      if self.current_token[TOKEN_TAG] == FOUND_YR:
        res.register_advancement() # Eat FOUND YR
        self.advance()

        return_expression  = res.register(self.expression())
        if return_expression is None: return res # Has error

        body_statements.append(return_expression)

      if self.current_token[TOKEN_TAG] != IF_U_SAY_SO:
        return res.failure(InvalidSyntaxError(self.current_token, "Expected an 'IF U SAY SO' keyword!"))
      
      res.register_advancement() # Eat IF U SAY SO
      self.advance()

      return res.success(FuncDefNode(function_name, parameters, body_statements))

    return res

# ═════════════════════════════════════════════════════════════════════════════════════════════════
  def function_call(self):
    res = ParseResult()
    function_name = None
    parameters = []

    if self.current_token[TOKEN_TAG] == I_IZ:
      res.register_advancement() # Eat I IZ
      self.advance()

      # Identifier
      if self.current_token[TOKEN_TAG] != IDENTIFIER:
        return res.failure(InvalidSyntaxError(self.current_token, "Expected a valid function name!"))
      
      function_name = res.register(self.expression())
      if function_name is None: return res

      # Check if there are parameters
      if self.current_token[TOKEN_TAG] == YR:
        res.register_advancement() # Eat YR
        self.advance()

        first_param = res.register(self.expression())
        if first_param is None: return res # Has error

        parameters.append(first_param)

        # Check for other params if there are any
        while self.current_token[TOKEN_TAG] == AN_YR:
          res.register_advancement() # Eat AN YR
          self.advance()

          additional_param = res.register(self.expression())
          if additional_param is None: return res # Has error

          parameters.append(additional_param)

      # function body
      if self.current_token[TOKEN_TAG] != MKAY:
        return res.failure(InvalidSyntaxError(self.current_token, "Expected an 'MKAY' keyword!"))
      
      res.register_advancement() # Eat MKAY
      self.advance()

      return res.success(FuncCallNode(function_name, parameters))

    return res

# ═════════════════════════════════════════════════════════════════════════════════════════════════
# RUNTIME RESULT
# ═════════════════════════════════════════════════════════════════════════════════════════════════
class RTResult:
  def __init__(self):
    self.value = None
    self.error = None
  
  def register(self, res):
    if res.error: self.error = res.error
    return res.value
  
  def success(self, value):
    self.value = value
    return self
  
  def failure(self, error):
    self.error = error
    return self

# ═════════════════════════════════════════════════════════════════════════════════════════════════
# VALUES
# ═════════════════════════════════════════════════════════════════════════════════════════════════


# ═════════════════════════════════════════════════════════════════════════════════════════════════
# SUPER CLASS
class Value:
  def __init__(self, line_number=None):
    self.line_number = line_number
    self.set_context()

  def set_context(self, context=None):
    self.context = context
    return self

  # Typecasting method (to be implemented in subclasses)
  def typecast(self, target_class):
    raise NotImplementedError("Subclasses must implement this method")

  # Explicit Typecasting method (to be implemented in subclasses)
  def explicit_typecast(self, target_class, to_float=False): # To float is for typecasting Flot->Int or Int->FLoat
    raise NotImplementedError("Subclasses must implement this method")

  # ═════════════════════════════════════════════════════════════════════════════════════════════════
  # Number Arithmetic operations (ensure result is always a Number)
  def added_by(self, other):
    # Typecast both operands to Number before performing the addition
    self, error = self.typecast(Number) 
    if error: return None, error

    other, error = other.typecast(Number)
    if error: return None, error

    result = self.value + other.value

    return Number(result).set_context(self.context), None

  def subtracted_by(self, other):
    # Typecast both operands to Number before performing the subtraction
    self, error = self.typecast(Number) 
    if error: return None, error

    other, error = other.typecast(Number)
    if error: return None, error

    result = self.value - other.value

    return Number(result).set_context(self.context), None

  def multiplied_by(self, other):
    # Typecast both operands to Number before performing the multiplication
    self, error = self.typecast(Number) 
    if error: return None, error

    other, error = other.typecast(Number)
    if error: return None, error

    result = self.value * other.value

    return Number(result).set_context(self.context), None

  def divided_by(self, other):
    # Typecast both operands to Number before performing the division
    self, error = self.typecast(Number) 
    if error: return None, error

    other, error = other.typecast(Number)
    if error: return None, error

    if other.value == 0:
      return None, RuntimeError(
        ('Result is Zero', None, other.line_number), 'Division by Zero'
      )
    
    result = self.value / other.value

    return Number(result).set_context(self.context), None
  
  def modulo(self, other):
    # Typecast both operands to Number before performing the modulo
    self, error = self.typecast(Number) 
    if error: return None, error

    other, error = other.typecast(Number)
    if error: return None, error

    result = self.value % other.value

    return Number(result).set_context(self.context), None

  def maximum(self, other):
    # Typecast both operands to Number before performing the division
    self, error = self.typecast(Number)
    if error: return None, error

    other, error = other.typecast(Number)
    if error: return None, error

    result = max(self.value, other.value)

    return Number(result).set_context(self.context) , None

  def minimum(self, other):
    # Typecast both operands to Number before performing the division
    self, error = self.typecast(Number)
    if error: return None, error

    other, error = other.typecast(Number)
    if error: return None, error

    result = min(self.value, other.value)

    return Number(result).set_context(self.context) , None
  
  # ═════════════════════════════════════════════════════════════════════════════════════════════════
  # Boolean Logical Operations
  def and_logic(self, other):
    # Typecast both operands to Boolean before performing the and operation
    self, error = self.typecast(Boolean)
    if error: return None, error

    other, error = other.typecast(Boolean)
    if error: return None, error

    result = self.value and other.value

    return Boolean(result).set_context(self.context) , None

  def or_logic(self, other):
    # Typecast both operands to Boolean before performing the or operation
    self, error = self.typecast(Boolean)
    if error: return None, error

    other, error = other.typecast(Boolean)
    if error: return None, error

    result = self.value or other.value    

    return Boolean(result).set_context(self.context) , None

  def xor_logic(self, other):
    # Typecast both operands to Boolean before performing the xor operation
    self, error = self.typecast(Boolean) 
    if error: return None, error

    other, error = other.typecast(Boolean)
    if error: return None, error

    result = (self.value or other.value) and not (self.value and other.value) 

    return Boolean(result).set_context(self.context) , None

  def not_logic(self):
    # Typecast the operand to Boolean before performing the not operation
    self, error = self.typecast(Boolean) 
    if error: return None, error

    result = not self.value  

    return Boolean(result).set_context(self.context) , None

  # ═════════════════════════════════════════════════════════════════════════════════════════════════
  # Comparison
  def is_equal(self, other):
    # Typecast the second operand to the data type of the first operand before checking if they're equal
    other, error = other.typecast(self.__class__)
    if error: return None, error

    result = self.value == other.value

    return Boolean(result).set_context(self.context) , None

  def is_not_equal(self, other):
    # Typecast the second operand to the data type of the first operand before checking if they're not equal
    other, error = other.typecast(self.__class__)
    if error: return None, error

    result = self.value != other.value

    return Boolean(result).set_context(self.context) , None

  def __repr__(self):
    return str(self.value)  

# ═════════════════════════════════════════════════════════════════════════════════════════════════
class Break(Value):
  def __init__(self, value, line_number=None):
    self.value = value
    self.line_number = line_number
    self.set_context()
    super().__init__(line_number)

  def set_context(self, context=None):
    self.context = context
    return self

  # Typecasting method (to be implemented in subclasses)
  def typecast(self, target_class): pass

  # Explicit Typecasting method (to be implemented in subclasses)
  def explicit_typecast(self, target_class, to_float=False): pass

# ═════════════════════════════════════════════════════════════════════════════════════════════════
class Noob(Value):
  def __init__(self, line_number=None):
    self.value = None
    self.line_number = line_number
    super().__init__(line_number)

  def typecast(self, target_class):
    # No need to typecast for Noob-to-Noob
    if target_class == self.__class__:
      return self , None

    elif target_class == Boolean:
      return Boolean(self.value).set_context(self.context) , None
    
    # Error
    return None, RuntimeError(
        ('Typecast error', None, self.line_number), f"Can't Typecast {self.__class__.__name__}: {self.value}  to {target_class.__name__}"
      )

  # Explicit typecasting of NOOBs is allowed and results to empty/zero values depending on the type.
  def explicit_typecast(self, target_class, to_float=False):
    # No need to typecast for Noob-to-Noob
    if target_class == self.__class__:
      return self , None

    elif target_class == Boolean:
      return Boolean(self.value).set_context(self.context) , None
    
    elif target_class == String:
      return String("").set_context(self.context) , None

    elif target_class == Number:
      return Number(0).set_context(self.context) , None

    # Error
    return None, RuntimeError(
        ('Typecast error', None, self.line_number), f"Can't Typecast {self.__class__.__name__}: {self.value}  to {target_class.__name__}"
      )

  def __repr__(self):
    return str('NOOB')   

class String(Value):
  def __init__(self, value, line_number=None):
    self.value = value
    self.line_number = line_number
    super().__init__(line_number)

  def typecast(self, target_class):
    # No need to typecast for String-to-String
    if target_class == self.__class__:
      return self , None

    elif target_class == Boolean:
      return Boolean(self.value).set_context(self.context) , None
    
    elif target_class == Number:
      if Number.is_integer(self.value):
        return Number(int(self.value)).set_context(self.context) , None
      elif Number.is_float(self.value):
        # Truncate up to 2 decimal places
        return Number(float(self.value)).set_context(self.context) , None
      # else:
      #   # 0 if empty, 1 if not (delete this, was not mentioned in project specs)
      #   return Number(int(bool(self.value))).set_context(self.context) , None

    # Error
    return None, RuntimeError(
        ('Typecast error', None, self.line_number), f"Can't Typecast {self.__class__.__name__}: {self.value}  to {target_class.__name__}"
      )

  # No change with implicit typecasting
  def explicit_typecast(self, target_class, to_float=False):
    return self.typecast(target_class)

  def __repr__(self):
    return str(self.value) 

class Number(Value):
  def __init__(self, value, line_number=None):
    self.value = value
    self.line_number = line_number
    super().__init__(line_number)

  def typecast(self, target_class):
    # No need to typecast for Number-to-Number
    if target_class == self.__class__:
      return self , None

    elif target_class == Boolean:
      return Boolean(self.value != 0).set_context(self.context) , None
    
    elif target_class == String:
      if Number.is_integer(self.value):
        return String(str(self.value)).set_context(self.context) , None
      elif Number.is_float(self.value):
        return String(str(int(self.value * 100) / 100)).set_context(self.context) , None  # if Float, Truncate up to two decimal places
    
    # Error
    return None, RuntimeError(
        ('Typecast error', None, self.line_number), f"Can't Typecast {self.__class__.__name__}: {self.value}  to {target_class.__name__}"
      )
  
  def explicit_typecast(self, target_class, to_float=False):
    # Casting NUMBARs to NUMBR will truncate the decimal portion of the NUMBAR.
    # Casting NUMBRs to NUMBAR will just convert the value into a floating point.The value should be retained.
    if target_class == self.__class__:
      if Number.is_integer(self.value) and to_float == False:
        return self , None # No need to change anything if Int already
      
      # Integer -> Float
      elif Number.is_integer(self.value) and to_float == True:
        return Number(float(self.value)).set_context(self.context) , None
      
      # Float -> Integer
      elif Number.is_float(self.value) and to_float == True:
        return Number(int(self.value)).set_context(self.context) , None

    elif target_class == Boolean:
      return Boolean(self.value != 0).set_context(self.context) , None
    
    elif target_class == String:
      if Number.is_integer(self.value):
        return String(str(self.value)).set_context(self.context) , None
      elif Number.is_float(self.value):
        return String(str(int(self.value * 100) / 100)).set_context(self.context) , None  # if Float, Truncate up to two decimal places
    
    # Error
    return None, RuntimeError(
        ('Typecast error', None, self.line_number), f"Can't Typecast {self.__class__.__name__}: {self.value}  to {target_class.__name__}"
      )

  def is_integer(value_to_check):
    return bool(re.match(r'^-?\d+$', str(value_to_check)))  

  def is_float(value_to_check):
    return bool(re.match(r'^-?\d*\.\d*$', str(value_to_check)))

  def __repr__(self):
    return str(self.value)

class Boolean(Value):
  def __init__(self, value_representation, line_number=None):
    self.line_number = line_number
    self.value = None
    
    if value_representation == 'WIN':
      self.value = True
    elif value_representation == 'FAIL':
      self.value = False
    else:
      # TYPECAST if needed
      self.value = bool(value_representation)

    super().__init__(line_number)

  def typecast(self, target_class):
    # No need to typecast for Boolean-to-Boolean
    if target_class == self.__class__:
      return self , None

    elif target_class == Number:
      return Number(1 if self.value else 0).set_context(self.context) , None

    elif target_class == String:
      return String(self.get_value_representation()), None

    # Error
    return None, RuntimeError(
        ('Typecast error', None, self.line_number), f"Can't Typecast {self.__class__.__name__}: {self.value}  to {target_class.__name__}"
      )

  # Casting WIN to a numerical type results in 1 or 1.0.
  def explicit_typecast(self, target_class, to_float=False):
    # No need to typecast for Boolean-to-Boolean
    if target_class == self.__class__:
      return self , None

    elif target_class == Number:
      if to_float == False:
        return Number(1 if self.value else 0).set_context(self.context) , None
      else:
        return Number(1.0 if self.value else 0).set_context(self.context) , None

    elif target_class == String:
      return String(self.get_value_representation()), None

    # Error
    return None, RuntimeError(
        ('Typecast error', None, self.line_number), f"Can't Typecast {self.__class__.__name__}: {self.value}  to {target_class.__name__}"
      ) 
  
  def get_value_representation(self):
    return 'WIN' if self.value else 'FAIL'

  def __repr__(self):
    return str(self.get_value_representation())

class Function(Value):
  def __init__(self, function_name, parameters, body_statements):
    self.function_name = function_name
    self.parameters = parameters
    self.body_statements = body_statements
    super().__init__()

  def execute(self, passed_parameters):
    
    res = RTResult()
    interpreter = Interpreter()
    new_context = Context(self.function_name, parent=self.context)
    new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)

    if len(passed_parameters) > len(self.parameters):
      return res.failure(RuntimeError(
        ("Function", "Function", None),
        f"{len(passed_parameters) - len(self.parameters)} too many parameters passed into {self}"
      ))
    
    if len(passed_parameters) < len(self.parameters):
      return res.failure(RuntimeError(
        self.pos_start, self.pos_end,
        f"{len(self.parameters) - len(passed_parameters)} too few parameters passed into {self}"
      ))
    
    for i in range(len(passed_parameters)):
      param_name = self.parameters[i]
      param_name
      param_value = passed_parameters[i]

      param_value.set_context(new_context)
      new_context.symbol_table.set(param_name, param_value)
      
    value = None
    for statement in self.body_statements:
      value = res.register(interpreter.visit(statement, new_context))
      if res.error: return res

      if isinstance(value, Break):
        value = Noob()
        break

    return res.success(value)

  def typecast(self, target_class): return True
  def explicit_typecast(self, target_class, to_float=False): return True

  def __repr__(self):
    return f"<function {self.function_name}>"
#######################################
# CONTEXT
#######################################
class Context:
  def __init__(self, display_name, parent=None, parent_entry_pos=None):
    self.display_name = display_name
    self.parent = parent
    self.parent_entry_pos = parent_entry_pos
    self.symbol_table = None

#######################################
# SYMBOL_TABLE
#######################################
class SymbolTable:
  def __init__(self, parent=None):
    self.symbols = {}
    self.parent = parent # For functions (definitions/calls)
  
  def get(self, name):
    value = self.symbols.get(name, None)
    if value == None and self.parent:
      return self.parent.get(name)
    return value

  def found(self, name):
    if name in self.symbols: return True
    return False

  def set(self, name, value):
    self.symbols[name] = value

  def remove(self, name):
    del self.symbols[name]

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

