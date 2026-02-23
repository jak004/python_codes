# test_string_operations.py

import string_operations

# Test the functions
test_string = "Hello World"

print(f"Original string: {test_string}")
print(f"Reversed string: {string_operations.reverse_string(test_string)}")
print(f"Number of vowels: {string_operations.count_vowels(test_string)}")
print(f"Is palindrome? {string_operations.is_palindrome(test_string)}")

# Additional test cases
print("\nAdditional tests:")
print(f"Reversed 'radar': {string_operations.reverse_string('radar')}")
print(f"Vowels in 'python': {string_operations.count_vowels('python')}")
print(f"Is 'radar' a palindrome? {string_operations.is_palindrome('radar')}")