import os
import threading
import time

# Функція пошуку ключових слів у файлах
def search_in_files(file_list, keywords, results, lock):
    for file_path in file_list:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().lower()
                for word in keywords:
                    if word.lower() in content:
                        with lock:  # Блокуємо доступ, щоб уникнути колізій
                            results[word].append(file_path)
        except Exception as e:
            print(f"Помилка при обробці {file_path}: {e}")

def threaded_search(directory, keywords, num_threads=4):
    # Збираємо всі текстові файли
    files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".txt")]

    # Розподіляємо файли між потоками
    chunk_size = max(1, len(files) // num_threads)
    chunks = [files[i:i + chunk_size] for i in range(0, len(files), chunk_size)]

    # Результати пошуку
    results = {word: [] for word in keywords}
    lock = threading.Lock()
    threads = []

    start_time = time.time()

    # Створюємо та запускаємо потоки
    for chunk in chunks:
        t = threading.Thread(target=search_in_files, args=(chunk, keywords, results, lock))
        threads.append(t)
        t.start()

    # Чекаємо завершення потоків
    for t in threads:
        t.join()

    end_time = time.time()
    print(f"Час виконання (threading): {end_time - start_time:.4f} сек.")
    return results

if __name__ == "__main__":
    keywords = ["python", "data", "thread"]
    directory = "texts"
    results = threaded_search(directory, keywords)
    print("Результати пошуку:", results)