from lexer.lolcode_lexer import *
from .errors import *
from .nodes import *

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

