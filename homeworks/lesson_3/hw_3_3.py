"""3. Создать (не программно) текстовый файл со следующим содержимым:

One — 1
Two — 2
Three — 3
Four — 4

Необходимо написать программу, открывающую файл на чтение и считывающую построчно данные.
При этом английские числительные должны заменяться на русские.
Новый блок строк должен записываться в новый текстовый файл.

Решение покрыть тестами (опционально)."""

NUM_MAPPER = {
    "One": "Один",
    "Two": "Два",
    "Three": "Три",
    "Four": "Четыре"
}

with open("file.txt", "r") as file_for_read, open("new_file.txt", "w") as file_for_write:
    for readed_line in file_for_read:
        num, value = readed_line.split(" — ")
        res = f"{NUM_MAPPER[num]} — {value}"
        file_for_write.write(res)
