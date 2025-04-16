import sys
import re

# ═════════════════════════════════════════════════════════════════════════════════════════════════
# LEXER PROCESSING
# ═════════════════════════════════════════════════════════════════════════════════════════════════
# Function for tokenizing a string of characters based on a set of token patterns.
def lex(characters, token_exprs):
    pos = 0             # Current position in the input string
    tokens = []         # List to hold the tokenized output
    line_number = 1     # Start with line number 1

    # Traverse through the contents of the input
    while pos < len(characters):
        match = None # Flag to track whether a match is found for the current position

        # traverse through the list of regex patterns for tokens
        for token_expr in token_exprs:
            pattern, tag = token_expr               # Extract regex pattern and tag from token_expr; ex. ('HAI', 'Reserved')
            regex = re.compile(pattern)             # Compile the regex
            match = regex.match(characters, pos)    # Try to match the pattern at the current position
            
            # If there's a match, get the matched text
            if match:
                text = match.group(0)

                # But only add token to the list if it has a valid tag 
                if tag:
                    token = (text, tag, line_number)
                    tokens.append(token)

                # Update line count if a newline is encountered in the matched text
                line_number += text.count('\n')

                 # Exit the loop once a match is found
                break

        # If there's no match found, then there's an error
        if not match:
            sys.stderr.write("Illegal character: '%s' at %d\n" % (characters[pos], line_number))
            sys.exit(1)
        
        # If match found, move the position pointer to the end of the matched text
        else:
            pos = match.end(0)
    
    # Return the list of tokens
    return tokens


# ═════════════════════════════════════════════════════════════════════════════════════════════════
# MULT-LINE VALIDATOR
# ═════════════════════════════════════════════════════════════════════════════════════════════════
# Function to check if a certain word in a line is inside a string or not
def is_word_in_quotes(line, word):
    return bool(re.search(rf'"[^"]*\b{re.escape(word)}\b[^"]*"', line))

# Function to validate multiline comments in the input text.
# Ensures that:
# - 'OBTW' starts a block and is properly closed by 'TLDR' on a separate line.
# - 'TLDR' does not appear without a preceding 'OBTW'.
# - 'OBTW' and 'TLDR' do not coexist on the same line unless both are inside a string.
# - 'OBTW' is only preceded by whitespace/s, and 'TLDR' is only followed by whitespace/s.
def validate_multiline_comments(characters) :
    # print(characters) # For debugging

    inside_obtw = False                 # Flag to track if we're inside an OBTW block
    found_tldr_without_obtw = False     # Flag to track standalone TLDR

    # Traverse through the contents of the input
    for line_number, line in  enumerate(characters.splitlines(), 1):
        # Check if both OBTW and TLDR are on the same line
        # Raise an error if they are
        if re.search(r'\bOBTW\b', line) and re.search(r'\bTLDR\b', line):
            if not (is_word_in_quotes(line, 'OBTW') and is_word_in_quotes(line, 'TLDR')):
                sys.stderr.write(f"Error: 'OBTW' and 'TLDR' cannot coexist on the same line (line {line_number}).\n")
                sys.exit(1)

        # Validate the existence of the 'OBTW' keyword
        if re.search(r'\bOBTW\b', line):
            # Skip if 'OBTW' is inside a string
            if is_word_in_quotes(line, 'OBTW'):
                continue            

            # Skip if inside an OBTW block
            if inside_obtw:         
                continue

            # Skip if 'OBTW' is preceded by whitespace/s only
            if line.lstrip().startswith("OBTW"):
                inside_obtw = True  # Set flag to indicate we're inside an OBTW block
                continue            

            # Raise an error if 'OBTW' is preceded by anything other than whitespace/s
            sys.stderr.write(f"Error: 'OBTW' multiline comment keyword at line {line_number} can only be preceded by whitespace/s.\n")
            sys.exit(1)

        # Validate the existence of the 'TLDR' keyword
        if re.search(r'\bTLDR\b', line):
            # Skip if 'TLDR' is inside a string
            if is_word_in_quotes(line, 'TLDR') and not inside_obtw:
                continue
            
            # Skip if 'TLDR' is followed by whitespace/s only
            # But first check if it has a valid 'OBTW' pair
            if line.rstrip().endswith("TLDR"):
                if not inside_obtw:  # TLDR found without a preceding OBTW
                    found_tldr_without_obtw = True

                inside_obtw = False  # Reset the flag when exiting the block
                continue

            # Raise an error if 'OBTW' is followed by anything other than whitespace/s
            sys.stderr.write(f"Error: 'TLDR' multiline comment keyword at line {line_number} can only be followed by whitespace/s.\n")
            sys.exit(1)
    
    # Ensure that there's a closing TLDR if we left the block open
    if inside_obtw:
        sys.stderr.write(f"Error: Missing 'TLDR' to close the 'OBTW' block.\n")
        sys.exit(1)

    # Ensure that TLDR does not appear without a preceding OBTW
    if found_tldr_without_obtw:
        sys.stderr.write("Error: Found 'TLDR' without a preceding 'OBTW'.\n")
        sys.exit(1)


# ═════════════════════════════════════════════════════════════════════════════════════════════════
# TOKENIZING
# ═════════════════════════════════════════════════════════════════════════════════════════════════
# Indices
TOKEN_VALUE = 0
TOKEN_TAG = 1
TOKEN_LINE_NUMBER = 2

# Keywords
HAI = 'Program Start Delimeter'
KTHXBYE = 'Program End Delimeter'
WAZZUP = 'Variable Declaration Start Delimeter'
BUHBYE = 'Variable Declaration End Delimeter'
I_HAS_A ='Variable Declaration'
ITZ = 'Variable Initialization'
R = 'Assignment Keyword'

# Arithmetic Operations
SUM_OF = 'Addition Operator'
DIFF_OF = 'Subtraction Operator'
PRODUKT_OF = 'Multiplication Operator'
QUOSHUNT_OF = 'Division Operator'
MOD_OF = 'Modulus Operator'
BIGGR_OF = 'Greater Than Operator'
SMALLR_OF = 'Less Than Operator'
BOTH_OF = 'AND Operator'
EITHER_OF = 'OR Operator'
WON_OF = 'XOR Operator'
NOT = 'NOT Operator'
ANY_OF = 'ANY Operator'
ALL_OF = 'ALL Operator'
BOTH_SAEM = 'Equality Operator'
DIFFRINT = 'Inequality Operator'
SMOOSH = 'String Concatenate Operator'
MAEK_A = 'Typecast Operator'
IS_NOW_A = 'Typecast IS NOW A Operator'

# Part of the expression for operands
AN = 'Operand Connector'
YR = 'Parameter Variable'
AN_YR = 'Additional Parameter Variable'

# Statements
VISIBLE = 'Print Statement'
VISIBLE_OPERATOR = 'Print Statement Delimiter'
GIMMEH = 'Input Statement'
O_RLY = 'Conditional Start Delimeter'
YA_RLY = 'If Clause'
MEBBE = 'Else-If Clause'
NO_WAI = 'Else Clause'
OIC = 'Conditional End Delimeter'
WTF = 'Switch-Case Start Delimeter'
OMG = 'Case Clause'
OMGWTF = 'Switch-Case End Delimeter'
IM_IN_YR = 'Loop Start Delimeter'
UPPIN = 'Increment Operator'
NERFIN = 'Decrement Operator'
TIL = 'Until Loop'
WILE = 'While Loop'
IM_OUTTA_YR = 'Loop End Delimeter'
# Functions
HOW_IZ_I = 'Function Start Delimeter'
IF_U_SAY_SO = 'Function End Delimeter'
GTFO = 'Function Return'
FOUND_YR = 'Function Return Value'
I_IZ = 'Function Call'
MKAY = 'Statement End Delimeter'

# Literals
NUMBR = 'Integer'
NUMBAR = 'Float'
TROOF = 'Boolean'
YARN = 'String'
LITERAL_TYPE = 'Literal Type'

NOOB = "NULL"

# Identifier
IDENTIFIER = 'Identifier'

# End of File
EOF = 'End of File'

# Make sure that the pattern matches as a whole word, excluding it from being part of larger words.
def bound(pattern):
    return rf'(?<!\w){pattern}(?!\w)'

token_exprs = [
    (r'[ \n\t]+',                             None),   # whitespace (ignore)
    (r'BTW[^\n]*',                            None),   # single line comments (ignore)
    (r'OBTW\s*((.|\n)*?)\s*TLDR',             None),   # multi-line comments (ignore)
    (bound('HAI'),                            HAI),
    (bound('KTHXBYE'),                        KTHXBYE),
    (bound('WAZZUP'),                         WAZZUP),
    (bound('BUHBYE'),                         BUHBYE),
    (bound('I HAS A'),                        I_HAS_A),
    (bound('ITZ'),                            ITZ),
    (bound('R'),                              R),
    (bound('SUM OF'),                         SUM_OF),
    (bound('DIFF OF'),                        DIFF_OF),
    (bound('PRODUKT OF'),                     PRODUKT_OF),
    (bound('QUOSHUNT OF'),                    QUOSHUNT_OF),
    (bound('MOD OF'),                         MOD_OF),
    (bound('BIGGR OF'),                       BIGGR_OF),
    (bound('SMALLR OF'),                      SMALLR_OF),
    (bound('BOTH OF'),                        BOTH_OF),
    (bound('EITHER OF'),                      EITHER_OF),
    (bound('WON OF'),                         WON_OF),
    (bound('NOT'),                            NOT),
    (bound('ANY OF'),                         ANY_OF),
    (bound('ALL OF'),                         ALL_OF),
    (bound('AN YR'),                          AN_YR),
    (bound('AN'),                             AN),
    (bound('BOTH SAEM'),                      BOTH_SAEM),
    (bound('DIFFRINT'),                       DIFFRINT),
    (bound('SMOOSH'),                         SMOOSH),
    (bound('MAEK A'),                           MAEK_A),
    (bound('IS NOW A'),                       IS_NOW_A),
    (bound('VISIBLE'),                        VISIBLE),
    (bound('GIMMEH'),                         GIMMEH),
    (bound('O RLY\?'),                        O_RLY),
    (bound('YA RLY'),                         YA_RLY),
    (bound('MEBBE'),                          MEBBE),
    (bound('NO WAI'),                         NO_WAI),
    (bound('OIC'),                            OIC),
    (bound('WTF\?'),                          WTF),
    (bound('OMG'),                            OMG),
    (bound('OMGWTF'),                         OMGWTF),
    (bound('IM IN YR'),                       IM_IN_YR),
    (bound('UPPIN'),                          UPPIN),
    (bound('NERFIN'),                         NERFIN),
    (bound('YR'),                             YR),
    (bound('TIL'),                            TIL),
    (bound('WILE'),                           WILE),
    (bound('IM OUTTA YR'),                    IM_OUTTA_YR),
    (bound('HOW IZ I'),                       HOW_IZ_I),
    (bound('IF U SAY SO'),                    IF_U_SAY_SO),
    (bound('GTFO'),                           GTFO),
    (bound('FOUND YR'),                       FOUND_YR),
    (bound('I IZ'),                           I_IZ),
    (bound('MKAY'),                           MKAY),
    (r'\+',                                   VISIBLE_OPERATOR),
    (bound('-?[0-9]+\.[0-9]+'),               NUMBAR),          # Float
    (bound('-?[0-9]+'),                       NUMBR),           # Integer
    (bound('"[^"]*"'),                        YARN),            # String
    (bound('(WIN|FAIL)'),                     TROOF),           # Boolean
    (bound('NOOB'),                           NOOB),          # NOOB literal type
    (bound('(NUMBR|NUMBAR|YARN|TROOF)'), LITERAL_TYPE),    # Type
    (bound('[a-zA-Z][a-zA-Z0-9_]*'),          IDENTIFIER),      # Identifier
]

def lolcode_lex(characters):
    validate_multiline_comments(characters) # Validate the existence of multi-line comments
    return lex(characters, token_exprs)
