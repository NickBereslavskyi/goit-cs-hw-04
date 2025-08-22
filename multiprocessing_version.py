import os
import time
import multiprocessing

# Функція пошуку у файлах
def search_in_files(file_list, keywords, queue):
    local_results = {word: [] for word in keywords}
    for file_path in file_list:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().lower()
                for word in keywords:
                    if word.lower() in content:
                        local_results[word].append(file_path)
        except Exception as e:
            print(f"Помилка при обробці {file_path}: {e}")
    queue.put(local_results)

def multiprocess_search(directory, keywords, num_processes=4):
    files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".txt")]

    # Розподіл файлів
    chunk_size = max(1, len(files) // num_processes)
    chunks = [files[i:i + chunk_size] for i in range(0, len(files), chunk_size)]

    queue = multiprocessing.Queue()
    processes = []

    start_time = time.time()

    # Створюємо процеси
    for chunk in chunks:
        p = multiprocessing.Process(target=search_in_files, args=(chunk, keywords, queue))
        processes.append(p)
        p.start()

    # Чекаємо завершення
    for p in processes:
        p.join()

    # Збираємо результати
    results = {word: [] for word in keywords}
    while not queue.empty():
        local_results = queue.get()
        for word, files in local_results.items():
            results[word].extend(files)

    end_time = time.time()
    print(f"Час виконання (multiprocessing): {end_time - start_time:.4f} сек.")
    return results

if __name__ == "__main__":
    keywords = ["python", "data", "thread"]
    directory = "texts"
    results = multiprocess_search(directory, keywords)
    print("Результати пошуку:", results)