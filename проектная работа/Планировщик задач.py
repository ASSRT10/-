import threading
import time
import logging
import uuid

# Настройка логирования: вывод в файл и в консоль
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("tasks.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class PeriodicTask:
    def __init__(self, name, interval):
        self.id = str(uuid.uuid4())[:8]  # Короткий уникальный ID
        self.name = name
        self.interval = interval
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self._run, daemon=True)

    def _run(self):
        logging.info(f"Задача '{self.name}' (ID: {self.id}) запущена. Интервал: {self.interval}с")
        while not self.stop_event.is_set():
            # Ожидание интервала с проверкой флага остановки каждые 0.1с
            for _ in range(int(self.interval * 10)):
                if self.stop_event.is_set(): return
                time.sleep(0.1)
            
            logging.info(f"ВЫПОЛНЕНИЕ: {self.name} (ID: {self.id})")

    def start(self):
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        logging.info(f"Задача '{self.name}' (ID: {self.id}) остановлена.")

class Scheduler:
    def __init__(self):
        self.tasks = {}

    def add_task(self, name, interval):
        task = PeriodicTask(name, interval)
        self.tasks[task.id] = task
        task.start()
        print(f"Успешно добавлено: {name} [ID: {task.id}]")

    def remove_task(self, task_id):
        if task_id in self.tasks:
            self.tasks[task_id].stop()
            del self.tasks[task_id]
            print(f"Задача {task_id} удалена.")
        else:
            print("Ошибка: ID не найден.")

    def list_tasks(self):
        if not self.tasks:
            print("Список задач пуст.")
        for tid, t in self.tasks.items():
            print(f"ID: {tid} | Имя: {t.name} | Интервал: {t.interval} сек.")

def main():
    sched = Scheduler()
    while True:
        print("\n--- Меню планировщика ---")
        print("1. Добавить задачу\n2. Удалить задачу\n3. Список задач\n4. Выход")
        choice = input("Выберите действие: ")

        if choice == '1':
            name = input("Введите название задачи: ")
            try:
                sec = float(input("Введите интервал выполнения (сек): "))
                sched.add_task(name, sec)
            except ValueError:
                print("Ошибка: введите числовое значение.")
        elif choice == '2':
            tid = input("Введите ID задачи для удаления: ")
            sched.remove_task(tid)
        elif choice == '3':
            sched.list_tasks()
        elif choice == '4':
            print("Завершение работы...")
            break
        else:
            print("Неверный ввод.")

if __name__ == "__main__":
    main()