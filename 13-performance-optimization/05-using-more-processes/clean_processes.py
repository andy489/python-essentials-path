from multiprocessing import Process


def clean_order(order_id):
    for _ in range(500_000_000):
        pass
    print(f"Finished cleaning order {order_id}")

if __name__ == '__main__':
    first = Process(target=clean_order, args=(10,))
    second = Process(target=clean_order, args=(20,))

    first.start()
    second.start()

    first.join()
    second.join()