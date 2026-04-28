import abc
import typing


class DataProcessor(abc.ABC):
    def __init__(self) -> None:
        self._storage: list[str] = []
        self._total: int = 0

    @abc.abstractmethod
    def validate(self, data: typing.Any) -> bool:
        pass

    @abc.abstractmethod
    def ingest(self, data: typing.Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        rank = self._total - len(self._storage)
        value = self._storage.pop(0)
        return (rank, value)

    def remaining(self) -> int:
        return len(self._storage)

    def total(self) -> int:
        return self._total


class NumericProcessor(DataProcessor):
    def validate(self, data: typing.Any) -> bool:
        if isinstance(data, (int, float)):
            return True
        if isinstance(data, list):
            return bool(data) and all(
                isinstance(x, (int, float)) for x in data
            )
        return False

    def ingest(
        self,
        data: typing.Union[int, float, list[typing.Union[int, float]]]
    ) -> None:
        if not self.validate(data):
            raise TypeError("Improper numeric data")
        if isinstance(data, list):
            for item in data:
                self._storage.append(str(item))
                self._total += 1
        else:
            self._storage.append(str(data))
            self._total += 1


class TextProcessor(DataProcessor):
    def validate(self, data: typing.Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list):
            return bool(data) and all(isinstance(x, str) for x in data)
        return False

    def ingest(
        self,
        data: typing.Union[str, list[str]]
    ) -> None:
        if not self.validate(data):
            raise TypeError("Improper text data")
        if isinstance(data, list):
            for item in data:
                self._storage.append(item)
                self._total += 1
        else:
            self._storage.append(data)
            self._total += 1


class LogProcessor(DataProcessor):
    def validate(self, data: typing.Any) -> bool:
        if isinstance(data, dict):
            return all(
                isinstance(k, str) and isinstance(v, str)
                for k, v in data.items()
            )
        if isinstance(data, list):
            return bool(data) and all(
                isinstance(d, dict) and all(
                    isinstance(k, str) and isinstance(v, str)
                    for k, v in d.items()
                )
                for d in data
            )
        return False

    def ingest(
        self,
        data: typing.Union[dict[str, str], list[dict[str, str]]]
    ) -> None:
        if not self.validate(data):
            raise TypeError("Improper log data")
        if isinstance(data, dict):
            entry = f"{data['log_level']}: {data['log_message']}"
            self._storage.append(entry)
            self._total += 1
        else:
            for item in data:
                entry = f"{item['log_level']}: {item['log_message']}"
                self._storage.append(entry)
                self._total += 1


class DataStream:
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)

    def process_stream(self, stream: list[typing.Any]) -> None:
        for element in stream:
            handled = False
            for proc in self._processors:
                if proc.validate(element):
                    proc.ingest(element)
                    handled = True
                    break
            if not handled:
                print(
                    f"DataStream error - "
                    f"Can't process element in stream: {element}"
                )

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self._processors:
            print("No processor found, no data")
            return
        for proc in self._processors:
            name = type(proc).__name__.replace("Processor", " Processor")
            print(
                f"{name}: total {proc.total()} items processed, "
                f"remaining {proc.remaining()} on processor"
            )


if __name__ == "__main__":
    print("=== Code Nexus - Data Stream ===")

    print("\nInitialize Data Stream...")
    ds = DataStream()
    ds.print_processors_stats()

    print("\nRegistering Numeric Processor")
    ds.register_processor(NumericProcessor())

    batch = [
        'Hello world',
        [3.14, -1, 2.71],
        [
            {
                'log_level': 'WARNING',
                'log_message': 'Telnet access! Use ssh instead'},
            {'log_level': 'INFO', 'log_message': 'User wil is connected'}
        ],
        42,
        ['Hi', 'five']
    ]
    print(f"\nSend first batch of data on stream: {batch}")
    ds.process_stream(batch)
    ds.print_processors_stats()

    print("\nRegistering other data processors")
    ds.register_processor(TextProcessor())
    ds.register_processor(LogProcessor())

    print("Send the same batch again")
    ds.process_stream(batch)
    ds.print_processors_stats()

    print(
        "\nConsume some elements from the data processors: "
        "Numeric 3, Text 2, Log 1"
    )
    num_p = ds._processors[0]
    txt_p = ds._processors[1]
    log_p = ds._processors[2]
    for _ in range(3):
        num_p.output()
    for _ in range(2):
        txt_p.output()
    log_p.output()
    ds.print_processors_stats()
