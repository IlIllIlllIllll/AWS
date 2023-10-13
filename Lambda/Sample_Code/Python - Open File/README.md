Python - Open File

#Read File
```python
with open(file_name, 'r') as file:
    file_content = file.read()
```
#Write File
```python
with open(file_name, 'w') as file:
    file.write("<text>") #줄바꿈 할 시 (f"{<Text>}\n")
```

#Cover File
```python
with open(file_name, 'a') as file:
    file.write(f"{<text>}\n") #줄바꿈 할 시 (f"{<Text>}\n")
```

> Write File - https://wikidocs.net/26