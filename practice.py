# =====================================================================
# CATEGORY 4: DEBUGGING EXERCISES
# Topics: syntax errors, off-by-one errors, incorrect loop bounds,
#         missing return statements
#
# Format: for each one, the BUGGY version is shown first (commented out
# so this file still runs), then the FIXED version, with a note on WHY
# it was wrong. On the real exam you'll be handed broken code directly -
# practice spotting these patterns fast.
# =====================================================================

# ---------------------------------------------------------------------
# DEBUG 1: Off-by-one error in a loop
# ---------------------------------------------------------------------
# BUGGY VERSION:
# def sum_up_to_n(n):
#     total = 0
#     for i in range(1, n):      # BUG: excludes n itself
#         total += i
#     return total
# sum_up_to_n(5) gives 10 instead of 15

def sum_up_to_n(n):
    total = 0
    for i in range(1, n + 1):  # FIX: range must go up to n+1 to include n
        total += i
    return total

print(sum_up_to_n(5))  # 15


# ---------------------------------------------------------------------
# DEBUG 2: Missing return statement
# ---------------------------------------------------------------------
# BUGGY VERSION:
# def square(n):
#     result = n * n
#     # BUG: forgot to return result, function returns None
#
# print(square(4))  # prints None

def square(n):
    result = n * n
    return result  # FIX: added the missing return

print(square(4))  # 16


# ---------------------------------------------------------------------
# DEBUG 3: Incorrect loop bounds causing IndexError
# ---------------------------------------------------------------------
# BUGGY VERSION:
# def print_pairs(arr):
#     for i in range(len(arr)):
#         print(arr[i], arr[i + 1])  # BUG: crashes on the last i,
#                                    # since i+1 goes out of range
# print_pairs([1, 2, 3])

def print_pairs(arr):
    for i in range(len(arr) - 1):  # FIX: stop one early so i+1 stays valid
        print(arr[i], arr[i + 1])

print_pairs([1, 2, 3])  # (1 2) then (2 3)


# ---------------------------------------------------------------------
# DEBUG 4: Syntax error (indentation / colon issues) + logic bug combo
# ---------------------------------------------------------------------
# BUGGY VERSION (would not even run):
# def check_positive(n)          # BUG: missing colon
#     if n > 0
#         return "Positive"      # BUG: missing colon, wrong indentation
#     else:
#     return "Non-positive"      # BUG: not indented inside else block

def check_positive(n):             # FIX: colon added
    if n > 0:                      # FIX: colon added
        return "Positive"
    else:
        return "Non-positive"      # FIX: properly indented inside else

print(check_positive(5))    # Positive
print(check_positive(-3))   # Non-positive


# ---------------------------------------------------------------------
# DEBUG 5: Wrong comparison operator (a classic "spot the bug" trap)
# ---------------------------------------------------------------------
# BUGGY VERSION:
# def is_leap_year(year):
#     if year % 4 = 0:              # BUG: assignment operator instead of ==
#         return True
#     return False

def is_leap_year(year):
    # FIX: use == for comparison, and a proper leap year rule
    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        return True
    return False

print(is_leap_year(2024))  # True
print(is_leap_year(1900))  # False (divisible by 100 but not 400)
print(is_leap_year(2000))  # True (divisible by 400)


# ---------------------------------------------------------------------
# DEBUG 6: Infinite loop from forgetting to update the loop variable
# ---------------------------------------------------------------------
# BUGGY VERSION:
# def countdown(n):
#     while n > 0:
#         print(n)
#         # BUG: forgot "n -= 1", this loops forever
# countdown(5)

def countdown(n):
    while n > 0:
        print(n)
        n -= 1  # FIX: decrement so the loop condition eventually fails

countdown(5)  # 5 4 3 2 1
