# 1. asyncio.create_task()      ****************************************

# This is a job, checking the a folder to see if there are any text files,
# The task will run after the specified time and after ( import schedule )
# This will work for 24 hours for an unlimited While loop ( while True )
# Asyncio will multitask here / Share task here ( schedule_job() )

import os
import schedule
from datetime import datetime
import asyncio

async def job(arg='argument'):
    file_list = os.listdir('.')
    for file_name in file_list:
        if file_name.endswith('.txt'):
            text_file_path = os.path.join('.', file_name)
            with open(text_file_path, 'r') as file:
                file_contents = file.read()
            print(f"Contents of {file_name}:")
            print(file_contents)
            os.remove(file_name)
    else:
        print("No text files found in the folder.")
        print(arg)


def schedule_job():
    loop = asyncio.get_event_loop()       # It ensures that these tasks are executed efficiently and concurrently
    task = asyncio.create_task(job())     # event loop to actually run that task
    loop.run_until_complete(task)         # This line effectively tells the event loop to execute the task and await its completion


schedule.every(1).seconds.to(5).do(schedule_job)
schedule.every(1).minutes.to(5).do(schedule_job)
schedule.every(2).hours.to(5).do(schedule_job)
schedule.every().minute.at(':20').do(schedule_job)
schedule.every().hour.at(':20').do(schedule_job)
schedule.every(5).hours.at(':20').do(schedule_job)
schedule.every().day.at('12:20:30').do(schedule_job)
schedule.every().monday.at('01:20').do(schedule_job)
schedule.every(10).seconds.until('10:20').do(schedule_job)
schedule.every(10).seconds.until(datetime(2024, 11, 21, 10, 21, 5)).do(schedule_job)

while True:
    schedule.run_pending()



# 2. asyncio.gather() and  asyncio.run()   ****************************************

import asyncio
async def foo():
    print("Foo started")
    await asyncio.sleep(2)
    print("Foo finished")
    return 42
def synchronous_function():
    print("Synchronous function started")
    return "Hello, World!"
async def main():
    result = await asyncio.gather(foo(), synchronous_function())
    print("Results:", result)
asyncio.run(main())

# or
async def worker(task_id):
    await asyncio.sleep(1)
    print(f"Task {task_id} completed")
async def main():
    tasks = [worker(1), worker(2), worker(3)]
    await asyncio.gather(*tasks)
asyncio.run(main())



# 3. asyncio.Event() ****************************************

import asyncio
async def waiter(event):
    print("Waiting for the event to be set")
    await event.wait()
    print("Event has been set!")

async def setter(event, seconds):
    await asyncio.sleep(seconds)
    print(f"Setting the event after {seconds} seconds")
    event.set()

async def main():
    event = asyncio.Event()
    task1 = asyncio.create_task(waiter(event))
    task2 = asyncio.create_task(setter(event, 3))
    await asyncio.gather(task1, task2)
asyncio.run(main())

# output : *****
# >>> Waiting for the event to be set
# >>> Setting the event after 3 seconds
# >>> Event has been set!


# 4. asyncio.Lock()     ****************************************

import asyncio

async def task_with_lock(lock):
    print("Task is trying to acquire the lock")
    async with lock:
        print("Lock acquired, performing some critical work")
        await asyncio.sleep(2)
    print("Lock released, task is done")

async def main():
    lock = asyncio.Lock()

    task1 = asyncio.create_task(task_with_lock(lock))
    task2 = asyncio.create_task(task_with_lock(lock))

    await asyncio.gather(task1, task2)

asyncio.run(main())

# Output : *****
# >>> Task is trying to acquire the lock
# >>> Lock acquired, performing some critical work
# >>> Lock released, task is done
# >>> Task is trying to acquire the lock
# >>> Lock acquired, performing some critical work
# >>> Lock released, task is done


# 5. asyncio.Queue()  ****************************************

import asyncio
async def producer(queue):
    for i in range(1, 6):
        await asyncio.sleep(1)  # Simulate some work.
        item = f"Item {i}"
        await queue.put(item)
        print(f"Produced: {item}")

async def consumer(queue):
    while True:
        item = await queue.get()
        if item is None:
            break  # End the loop if the producer is done.
        await asyncio.sleep(2)  # Simulate processing.
        print(f"Consumed: {item}")
        queue.task_done()  # Indicate that the task is done.

async def main():
    queue = asyncio.Queue()
    producer_task = asyncio.create_task(producer(queue))
    consumer_task = asyncio.create_task(consumer(queue))
    await asyncio.sleep(10)  # Run for 10 seconds.
    await producer_task
    await queue.put(None)  # Signal the consumer that there are no more items.
    await consumer_task

asyncio.run(main())

# In this example, we have two asynchronous tasks: a producer and a consumer. They use an asyncio.Queue to communicate and coordinate their actions:
# The producer task adds items to the queue. It simulates some work using await asyncio.sleep(1) and then puts items into the queue using await queue.put(item).
# The consumer task continuously retrieves items from the queue. If it receives None, it exits the loop, signaling that there are no more items to process. It simulates some processing using await asyncio.sleep(2).
# In the main coroutine, we create an asyncio.Queue and two tasks: one for the producer and one for the consumer. We run the tasks concurrently.
# After running for 10 seconds, we signal the end of the producer's work by putting None into the queue and await the completion of both tasks.
# As a result, the producer produces items and the consumer consumes them, demonstrating asynchronous communication and coordination using an asyncio.Queue. The sleep times are used for illustration, and in a real application, you would replace them with actual work.

# Output :
# >>> Produced: Item 1
# >>> Produced: Item 2
# >>> Consumed: Item 1
# >>> Produced: Item 3
# >>> Produced: Item 4
# >>> Consumed: Item 2
# >>> Produced: Item 5
# >>> Consumed: Item 3
# >>> Consumed: Item 4
# >>> Consumed: Item 5

