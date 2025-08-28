from functions.write_file import write_file

result1 = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
print("Result for lorem.txt")
print(result1)

result2 = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
print("Result for pkg/morelorem.txt")
print(result2)

result3 = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
print("Result for /tmp/temp.txt")
print(result3)

